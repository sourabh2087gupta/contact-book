import streamlit as st
from database import (
    init_db, add_db_contact, get_all_contacts,
    search_db_contact, update_db_contact, delete_db_contact
)
from utils import is_valid_phone, is_valid_email, convert_to_csv

st.set_page_config(page_title="Smart Contact Book", page_icon="⚡", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_db()

# --- Hero Header ---
st.markdown("""
    <div class="hero-card">
        <div class="main-title">⚡ Smart Contact Hub</div>
        <p class="sub-text">Next-Gen Personal CRM & Connection Manager</p>
    </div>
""", unsafe_allow_html=True)

CATEGORIES = ["Family", "Friends", "College", "Work", "General"]
all_contacts = get_all_contacts("All")

# --- Live Dashboard Stats Row ---
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{len(all_contacts)}</div><div class="stat-label">Total Contacts</div></div>', unsafe_allow_html=True)
with s2:
    fam_count = len([c for c in all_contacts if c[3] in ["Family", "Friends"]])
    st.markdown(f'<div class="stat-box"><div class="stat-num">{fam_count}</div><div class="stat-label">Close Circle</div></div>', unsafe_allow_html=True)
with s3:
    col_count = len([c for c in all_contacts if c[3] == "College"])
    st.markdown(f'<div class="stat-box"><div class="stat-num">{col_count}</div><div class="stat-label">College Network</div></div>', unsafe_allow_html=True)
with s4:
    work_count = len([c for c in all_contacts if c[3] == "Work"])
    st.markdown(f'<div class="stat-box"><div class="stat-num">{work_count}</div><div class="stat-label">Work & Pro</div></div>', unsafe_allow_html=True)

# --- Modern Top Navigation Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add New", "📋 Directory & Export", "🔍 Live Search", "✏️ Edit Details", "🗑️ Remove"
])

def render_contact_card(name, phone, email, cat):
    initial = name[0].upper() if name else "?"
    email_display = email if email else "No email linked"
    st.markdown(f"""
        <div class="contact-card">
            <div class="contact-left">
                <div class="avatar">{initial}</div>
                <div class="contact-info">
                    <h4>{name}</h4>
                    <p>📞 {phone} &nbsp;&nbsp;|&nbsp;&nbsp; ✉️ {email_display}</p>
                </div>
            </div>
            <div>
                <span class="badge badge-{cat}">{cat}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# TAB 1: ADD CONTACT
with tab1:
    st.markdown("### ✨ Create New Connection")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name", placeholder="e.g. Rohan Sharma")
            email = st.text_input("✉️ Email Address", placeholder="rohan@example.com")
        with col2:
            phone = st.text_input("📞 Phone Number (10 digits)", placeholder="9876543210")
            category = st.selectbox("🏷️ Category", CATEGORIES)

        st.write("")
        submit = st.form_submit_button("🚀 Save to Directory", use_container_width=True)

        if submit:
            if not name.strip() or not phone.strip():
                st.warning("⚠️ Name and Phone Number are required.")
            elif not is_valid_phone(phone):
                st.error("⚠️ Invalid Phone Number! Enter a valid 10-digit number.")
            elif not is_valid_email(email):
                st.error("⚠️ Invalid Email format!")
            else:
                if add_db_contact(name.strip(), phone.strip(), email.strip(), category):
                    st.balloons()
                    st.success(f"🎉 '{name}' added under {category}!")
                    st.rerun()
                else:
                    st.error(f"⚠️ Contact '{name}' already exists!")

# TAB 2: VIEW & EXPORT
with tab2:
    f_col1, f_col2 = st.columns([3, 1])
    with f_col1:
        cat_filter = st.selectbox("Filter by Category:", ["All"] + CATEGORIES)
    with f_col2:
        st.write("")
        st.write("")
        contacts = get_all_contacts(cat_filter)
        if contacts:
            csv_data = convert_to_csv(contacts)
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name="contacts_export.csv",
                mime="text/csv",
                use_container_width=True
            )

    if not contacts:
        st.info("No contacts found in this category. Add some from the first tab! 🚀")
    else:
        grid_col1, grid_col2 = st.columns(2)
        for idx, (c_name, c_phone, c_email, c_cat) in enumerate(contacts):
            with (grid_col1 if idx % 2 == 0 else grid_col2):
                render_contact_card(c_name, c_phone, c_email, c_cat)

# TAB 3: SMART SEARCH
with tab3:
    st.markdown("### 🔎 Instant Search")
    query = st.text_input("Type any letter of Name or digits of Phone Number:", placeholder="Search here...").strip()

    if query:
        results = search_db_contact(query)
        if results:
            st.success(f"Found {len(results)} matching connection(s)")
            for c_name, c_phone, c_email, c_cat in results:
                render_contact_card(c_name, c_phone, c_email, c_cat)
        else:
            st.error("No matching contacts found. 😔")

# TAB 4: EDIT CONTACT
with tab4:
    st.markdown("### ✏️ Update Contact Info")
    if not all_contacts:
        st.info("No contacts available to edit.")
    else:
        contact_names = [c[0] for c in all_contacts]
        selected_name = st.selectbox("Select Person to Update:", contact_names)
        current_data = [c for c in all_contacts if c[0] == selected_name][0]

        with st.form("edit_form"):
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                new_phone = st.text_input("📞 Phone Number", value=current_data[1])
                new_email = st.text_input("✉️ Email Address", value=current_data[2])
            with e_col2:
                cat_index = CATEGORIES.index(current_data[3]) if current_data[3] in CATEGORIES else 4
                new_cat = st.selectbox("🏷️ Category", CATEGORIES, index=cat_index)

            update_btn = st.form_submit_button("🔄 Save Changes", use_container_width=True)
            if update_btn:
                if not is_valid_phone(new_phone):
                    st.error("⚠️ Invalid Phone Number!")
                elif not is_valid_email(new_email):
                    st.error("⚠️ Invalid Email format!")
                else:
                    update_db_contact(selected_name, new_phone.strip(), new_email.strip(), new_cat)
                    st.success(f"✅ '{selected_name}' updated successfully!")
                    st.rerun()

# TAB 5: DELETE CONTACT
with tab5:
    st.markdown("### 🗑️ Remove Connection")
    if not all_contacts:
        st.info("No contacts available to delete.")
    else:
        del_name = st.selectbox("Select contact to permanently remove:", [c[0] for c in all_contacts])
        if st.button("🚨 Delete Permanently", use_container_width=True):
            if delete_db_contact(del_name):
                st.success(f"🗑️ '{del_name}' removed!")
                st.rerun()