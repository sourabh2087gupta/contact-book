import streamlit as st
import json
import os

FILE_NAME = "contacts.json"

# --- Functions ---
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

# --- Web UI Setup ---
st.title(" My Contact Book")
contacts = load_contacts()

# Sidebar for Navigation
menu = ["Add Contact", "View All", "Search", "Delete"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Add Contact":
    st.header("Add a New Contact")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    
    if st.button("Save Contact"):
        if name in contacts:
            st.error(f"Contact '{name}' already exists!")
        elif name and phone:
            contacts[name] = {"Phone": phone, "Email": email}
            save_contacts(contacts)
            st.success(f"Contact '{name}' added successfully!")
        else:
            st.warning("Please enter at least Name and Phone Number.")

elif choice == "View All":
    st.header("Your Contacts")
    if not contacts:
        st.info("No contacts found. Add some first!")
    else:
        for name, details in contacts.items():
            st.write(f"**{name}** |  {details['Phone']} |  {details['Email']}")
            st.divider()

elif choice == "Search":
    st.header("Search Contact")
    search_name = st.text_input("Enter name to search:")
    if st.button("Search"):
        if search_name in contacts:
            details = contacts[search_name]
            st.success(f"**Found:** {search_name}")
            st.write(f" Phone: {details['Phone']}")
            st.write(f" Email: {details['Email']}")
        else:
            st.error(f"Contact '{search_name}' not found.")

elif choice == "Delete":
    st.header("Delete a Contact")
    del_name = st.text_input("Enter name to delete:")
    if st.button("Delete"):
        if del_name in contacts:
            del contacts[del_name]
            save_contacts(contacts)
            st.success(f"Contact '{del_name}' deleted!")
        else:
            st.error("Contact not found.")