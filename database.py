import sqlite3
from datetime import datetime

DB_FILE = "contacts.db"

def _get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT UNIQUE,
            phone TEXT,
            email TEXT,
            category TEXT DEFAULT 'General',
            is_favorite INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT '',
            last_contacted TEXT DEFAULT ''
        )
    ''')

    # Safe backward-compatible migrations for existing databases
    migrations = [
        "ALTER TABLE contacts ADD COLUMN category TEXT DEFAULT 'General'",
        "ALTER TABLE contacts ADD COLUMN is_favorite INTEGER DEFAULT 0",
        "ALTER TABLE contacts ADD COLUMN notes TEXT DEFAULT ''",
        "ALTER TABLE contacts ADD COLUMN created_at TEXT DEFAULT ''",
        "ALTER TABLE contacts ADD COLUMN last_contacted TEXT DEFAULT ''"
    ]
    for query in migrations:
        try:
            cursor.execute(query)
        except sqlite3.OperationalError:
            pass

    # Backfill created_at for legacy rows
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE contacts SET created_at = ? WHERE created_at IS NULL OR created_at = ''", (today,))
    conn.commit()
    conn.close()

def add_db_contact(name, phone, email, category="General", is_favorite=0, notes=""):
    conn = _get_conn()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d")
    try:
        cursor.execute(
            """
            INSERT INTO contacts (name, phone, email, category, is_favorite, notes, created_at, last_contacted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, phone, email, category, int(is_favorite), notes, created_at, "")
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_contacts(category_filter="All", favorites_only=False):
    conn = _get_conn()
    cursor = conn.cursor()
    query = "SELECT * FROM contacts WHERE 1=1"
    params = []

    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    if favorites_only:
        query += " AND is_favorite = 1"

    query += " ORDER BY is_favorite DESC, name ASC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def toggle_favorite(name, current_status):
    conn = _get_conn()
    cursor = conn.cursor()
    new_status = 0 if current_status else 1
    cursor.execute("UPDATE contacts SET is_favorite = ? WHERE name = ?", (new_status, name))
    conn.commit()
    conn.close()

def log_last_contacted(name):
    conn = _get_conn()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE contacts SET last_contacted = ? WHERE name = ?", (now_str, name))
    conn.commit()
    conn.close()

def update_db_contact(name, new_phone, new_email, new_category, new_notes, is_favorite):
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE contacts
        SET phone = ?, email = ?, category = ?, notes = ?, is_favorite = ?
        WHERE name = ?
        """,
        (new_phone, new_email, new_category, new_notes, int(is_favorite), name)
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_db_contact(name):
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted