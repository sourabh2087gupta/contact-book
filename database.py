import sqlite3

DB_FILE = "contacts.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT UNIQUE,
            phone TEXT,
            email TEXT,
            category TEXT DEFAULT 'General'
        )
    ''')
    # Agar purani table mein category column nahi hai toh automatically add kar dega
    try:
        cursor.execute("ALTER TABLE contacts ADD COLUMN category TEXT DEFAULT 'General'")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def add_db_contact(name, phone, email, category="General"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO contacts (name, phone, email, category) VALUES (?, ?, ?, ?)",
            (name, phone, email, category)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_contacts(category_filter="All"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if category_filter == "All":
        cursor.execute("SELECT name, phone, email, category FROM contacts ORDER BY name ASC")
    else:
        cursor.execute(
            "SELECT name, phone, email, category FROM contacts WHERE category = ? ORDER BY name ASC",
            (category_filter,)
        )
    data = cursor.fetchall()
    conn.close()
    return data

def search_db_contact(query):
    """Partial search using SQL LIKE."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, phone, email, category FROM contacts WHERE name LIKE ? OR phone LIKE ?",
        (f"%{query}%", f"%{query}%")
    )
    data = cursor.fetchall()
    conn.close()
    return data

def update_db_contact(name, new_phone, new_email, new_category):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET phone = ?, email = ?, category = ? WHERE name = ?",
        (new_phone, new_email, new_category, name)
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_db_contact(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted