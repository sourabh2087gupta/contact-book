import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = 'contacts.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create base table if it doesn't exist (legacy support)
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()

    # Safely migrate existing database by adding new columns if they are missing
    columns_to_add = {
        "address": "TEXT DEFAULT ''",
        "category": "TEXT DEFAULT 'General'",
        "notes": "TEXT DEFAULT ''",
        "is_favorite": "INTEGER DEFAULT 0",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    c.execute("PRAGMA table_info(contacts)")
    existing_columns = [col[1] for col in c.fetchall()]

    for col_name, col_def in columns_to_add.items():
        if col_name not in existing_columns:
            try:
                c.execute(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_def}")
            except Exception as e:
                pass # Column already exists
    conn.commit()
    conn.close()

def add_contact(name, phone, email, address, category, notes, is_favorite):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO contacts (name, phone, email, address, category, notes, is_favorite)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, address, category, notes, int(is_favorite)))
    conn.commit()
    conn.close()

def get_all_contacts():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM contacts ORDER BY name ASC", conn)
    conn.close()
    return df

def update_contact(contact_id, name, phone, email, address, category, notes, is_favorite):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE contacts 
        SET name=?, phone=?, email=?, address=?, category=?, notes=?, is_favorite=?
        WHERE id=?
    ''', (name, phone, email, address, category, notes, int(is_favorite), contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()

def toggle_favorite(contact_id, current_status):
    conn = get_connection()
    c = conn.cursor()
    new_status = 0 if current_status == 1 else 1
    c.execute("UPDATE contacts SET is_favorite=? WHERE id=?", (new_status, contact_id))
    conn.commit()
    conn.close()

def clear_all_contacts():
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()