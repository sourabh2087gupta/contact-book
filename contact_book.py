import streamlit as st
import sqlite3

DB_FILE = "contacts.db"

# --- Page Config (Tab Title & Icon) ---
st.set_page_config(page_title="Smart Contact Book", page_icon="📒", layout="centered")

# --- Database Setup & Functions (SAME AS BEFORE) ---
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

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main-title { font-size: 42px; color: #FF4B4B; text-align: center; font-weight: bold; margin-bottom: 0px;}
    .sub-text { text-align: center; color: #888888; font-size: 18px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- Web UI Setup ---
st.markdown('<div class="main-title">📒 Smart Contact Book</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Manage your connections beautifully</div>', unsafe_allow_html=True)

# Sidebar with better styling
st.sidebar.title("Navigation 🧭")
menu = ["➕ Add Contact", "📋 View All", "🔍 Search", "🗑️ Delete"]
choice = st.sidebar.radio("Go to:", menu)

if choice == "➕ Add Contact":
    st.subheader("Add a New Connection")
    # Form keeps the UI clean and only submits when button is pressed
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2) # Side-by-side inputs
        with col1:
            name = st.text_input("👤 Full Name")
        with col2:
            phone = st.text_input("📞 Phone Number")
        
        email = st.text_input("✉️ Email Address")
        
        # use_container_width makes the button full width
        submit = st.form_submit_button("Save Contact ✨", use_container_width=True)
        
        if submit:
            if name.strip() and phone.strip():
                success = add_db_contact(name.strip(), phone.strip(), email.strip())
                if success:
                    st.success(f"🎉 Contact '{name}' added successfully!")
                else:
                    st.error(f"⚠️ Contact '{name}' already exists!")
            else:
                st.warning("⚠️ Please enter at least Name and Phone Number.")

elif choice == "📋 View All":
    st.subheader("Your Connections")
    contacts = get_all_contacts()
    
    if not contacts:
        st.info("No contacts found. Time to add some! 🚀")
    else:
        # Show total number of contacts
        st.metric(label="Total Contacts", value=len(contacts))
        st.write("---")
        
        # Display contacts in neat expandable cards
        for c_name, c_phone, c_email in contacts:
            with st.expander(f"👤 **{c_name}**"):
                st.write(f"📞 **Phone:** {c_phone}")
                st.write(f"✉️ **Email:** {c_email}")

elif choice == "🔍 Search":
    st.subheader("Find a Contact")
    search_name = st.text_input("Enter exact name to search:").strip()
    
    if st.button("Search 🔎", use_container_width=True):
        if search_name:
            contact = search_db_contact(search_name)
            if contact:
                st.success("Contact Found! 🎉")
                # Info box for a highlighted view
                st.info(f"**👤 Name:** {contact[0]}\n\n**📞 Phone:** {contact[1]}\n\n**✉️ Email:** {contact[2]}")
            else:
                st.error(f"Contact '{search_name}' not found. 😔")

elif choice == "🗑️ Delete":
    st.subheader("Remove a Contact")
    del_name = st.text_input("Enter exact name to delete:").strip()
    
    # type="primary" makes the delete button red/highlighted
    if st.button("Delete Contact 🚨", type="primary", use_container_width=True):
        if del_name:
            success = delete_db_contact(del_name)
            if success:
                st.success(f"Contact '{del_name}' deleted permanently! 🗑️")
            else:
                st.error("Contact not found. 🛑")