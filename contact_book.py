import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = "contacts.db"

# --- Page Config ---
st.set_page_config(page_title="Smart Contact Book", page_icon="📒", layout="centered")

# --- Database Setup & Functions ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (name TEXT UNIQUE, phone TEXT, email TEXT)''')
    conn.commit()
    conn.close()

def add_db_contact(name, phone, email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_contacts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return data

def search_db_contact(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts WHERE name = ?", (name,))
    data = cursor.fetchone()
    conn.close()
    return data

def delete_db_contact(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

init_db()

# --- Modern Custom CSS ---
st.markdown("""
    <style>
    .main-title { font-size: 46px; background: -webkit-linear-gradient(#FF4B4B, #FF8040); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; margin-bottom: 5px;}
    .sub-text { text-align: center; color: #888888; font-size: 16px; margin-bottom: 30px; font-style: italic;}
    div[data-testid="stMetricValue"] { font-size: 30px; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- Web UI Setup ---
st.markdown('<div class="main-title">📒 Smart Contact Book</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Manage your connections beautifully</div>', unsafe_allow_html=True)

# App-like layout using Tabs instead of Sidebar
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Contact", "📋 View All", "🔍 Search", "🗑️ Delete"])

with tab1:
    st.subheader("Add a New Connection")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name", placeholder="e.g. Rahul Sharma")
        with col2:
            phone = st.text_input("📞 Phone Number", placeholder="+91 9876543210")
        
        email = st.text_input("✉️ Email Address", placeholder="rahul@example.com")
        submit = st.form_submit_button("Save Contact ✨", use_container_width=True)
        
        if submit:
            if name.strip() and phone.strip():
                success = add_db_contact(name.strip(), phone.strip(), email.strip())
                if success:
                    st.toast(f"Contact '{name}' saved! 🎉", icon="✅")
                else:
                    st.error(f"⚠️ Contact '{name}' already exists!")
            else:
                st.warning("⚠️ Please enter at least Name and Phone Number.")

with tab2:
    st.subheader("Your Connections")
    contacts = get_all_contacts()
    
    if not contacts:
        st.info("No contacts found. Time to add some! 🚀")
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric(label="Total Contacts", value=len(contacts))
        with col2:
            df = pd.DataFrame(contacts, columns=["Name", "Phone", "Email"])
            st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Find a Contact")
    search_name = st.text_input("Enter exact name to search:", placeholder="Type name here...").strip()
    
    if st.button("Search 🔎", use_container_width=True):
        if search_name:
            contact = search_db_contact(search_name)
            if contact:
                st.toast("Match Found!", icon="🎯")
                st.success(f"**👤 Name:** {contact[0]} | **📞 Phone:** {contact[1]} | **✉️ Email:** {contact[2]}")
            else:
                st.error(f"Contact '{search_name}' not found. 😔")

with tab4:
    st.subheader("Remove a Contact")
    del_name = st.text_input("Enter exact name to delete:", placeholder="Type name here...").strip()
    
    if st.button("Delete Contact 🚨", type="primary", use_container_width=True):
        if del_name:
            success = delete_db_contact(del_name)
            if success:
                st.toast(f"Contact '{del_name}' deleted! 🗑️", icon="✅")
            else:
                st.error("Contact not found. 🛑")