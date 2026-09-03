import streamlit as st
import sqlite3

DB_FILE = "contacts.db"

# --- Database Setup & Functions ---
def init_db():
    """Creates the contacts table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT UNIQUE,
            phone TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_db_contact(name, phone, email):
    """Inserts a new contact into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # IntegrityError happens if the name already exists (since it's UNIQUE)
        return False
    finally:
        conn.close()

def get_all_contacts():
    """Retrieves all contacts from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return data

def search_db_contact(name):
    """Searches for a single contact by name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts WHERE name = ?", (name,))
    data = cursor.fetchone()
    conn.close()
    return data

def delete_db_contact(name):
    """Deletes a contact by name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# Initialize DB when app starts
init_db()

# --- Web UI Setup ---
st.title("📖 My SQL Contact Book")

# Sidebar for Navigation
menu = ["Add Contact", "View All", "Search", "Delete"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Add Contact":
    st.header("Add a New Contact")
    name = st.text_input("Name").strip()
    phone = st.text_input("Phone Number").strip()
    email = st.text_input("Email Address").strip()
    
    if st.button("Save Contact"):
        if name and phone:
            success = add_db_contact(name, phone, email)
            if success:
                st.success(f"Contact '{name}' added successfully!")
            else:
                st.error(f"Contact '{name}' already exists!")
        else:
            st.warning("Please enter at least Name and Phone Number.")

elif choice == "View All":
    st.header("Your Contacts")
    contacts = get_all_contacts()
    if not contacts:
        st.info("No contacts found. Add some first!")
    else:
        for c_name, c_phone, c_email in contacts:
            st.write(f"**{c_name}** | 📞 {c_phone} | ✉️ {c_email}")
            st.divider()

elif choice == "Search":
    st.header("Search Contact")
    search_name = st.text_input("Enter name to search:").strip()
    if st.button("Search"):
        if search_name:
            contact = search_db_contact(search_name)
            if contact:
                st.success(f"**Found:** {contact[0]}")
                st.write(f"📞 Phone: {contact[1]}")
                st.write(f"✉️ Email: {contact[2]}")
            else:
                st.error(f"Contact '{search_name}' not found.")

elif choice == "Delete":
    st.header("Delete a Contact")
    del_name = st.text_input("Enter name to delete:").strip()
    if st.button("Delete"):
        if del_name:
            success = delete_db_contact(del_name)
            if success:
                st.success(f"Contact '{del_name}' deleted!")
            else:
                st.error("Contact not found.")