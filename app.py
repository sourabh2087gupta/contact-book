import streamlit as st
from database import (
    init_db, add_db_contact, get_all_contacts,
    search_db_contact, update_db_contact, delete_db_contact
)
from utils import is_valid_phone, is_valid_email, convert_to_csv

st.set_page_config(page_title="Smart Contact Hub", page_icon="⚡", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_db()

# --- Crisp Inline SVG Icons ---
SVG_HERO = '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_USERS = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_HEART = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'
SVG_GRAD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
SVG_BRIEFCASE = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>'
SVG_PHONE = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_MAIL = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

# --- Hero Header ---
st.markdown(f"""
    <div class="hero-card">
        <div class="hero-icon-wrap">{SVG_HERO}</div>
        <div class="main-title">Smart Contact Hub</div>
        <p class="sub-text">Next-Gen Personal CRM &amp; Connection Manager</p>
    </div>
""", unsafe_allow_html=True)

CATEGORIES = ["Family", "Friends", "College", "Work", "General"]
all_contacts = get_all_contacts("All")

# --- Live Dashboard Stats Row ---
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-blue">{SVG_USERS}</div><div><div class="stat-num">{len(all_contacts)}</div><div class="stat-label">Total Contacts</div></div></div>', unsafe_allow_html=True)
with s2:
    fam_count = len([c for c in all_contacts if c[3] in ["Family", "Friends"]])
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-pink">{SVG_HEART}</div><div><div class="stat-num">{fam_count}</div><div class="stat-label">Close Circle</div></div></div>', unsafe_allow_html=True)
with s3:
    col_count = len([c for c in all_contacts if c[3] == "College"])
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-purple">{SVG_GRAD}</div><div><div class="stat-num">{col_count}</div><div class="stat-label">College Network</div></div></div>', unsafe_allow_html=True)
with s4:
    work_count = len([c for c in all_contacts if c[3] == "Work"])
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-amber">{SVG_BRIEFCASE}</div><div><div class="stat-num">{work_count}</div><div class="stat-label">Work &amp; Pro</div></div></div>', unsafe_allow_html=True)

# --- Sleek Material Icon Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    ":material/person_add: Add New",
    ":material/contacts: Directory & Export",
    ":material/search: Live Search",
    ":material/edit_square: Edit Details",
    ":material/delete_sweep: Remove"
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
                    <div class="meta-row">
                        <span class="meta-item">{SVG_PHONE} {phone}</span>
                        <span class="meta-item">{SVG_MAIL} {email_display}</span>
                    </div>
                </div>
            </div>
            <div>
                <span class="badge badge-{cat}">{cat}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# TAB 1: ADD CONTACT
with tab1:
    st.markdown("#### :material/add_circle: Create New Connection")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Rohan Sharma")
            email = st.text_input("Email Address", placeholder="rohan@example.com")
        with col2:
            phone = st.text_input("Phone Number (10 digits)", placeholder="9876543210")
            category = st.selectbox("Category Tag", CATEGORIES)

        st.write("")
        submit = st.form_submit_button(":material/rocket_launch: Save to Directory", use_container_width=True)

        if submit:
            if not name.strip() or not phone.strip():
                st.warning("Name and Phone Number are required.")
            elif not is_valid_phone(phone):
                st.error("Invalid Phone Number! Enter a valid 10-digit number.")
            elif not is_valid_email(email):
                st.error("Invalid Email format!")
            else:
                if add_db_contact(name.strip(), phone.strip(), email.strip(), category):
                    st.balloons()
                    st.success(f"'{name}' added under {category}!")
                    st.rerun()
                else:
                    st.error(f"Contact '{name}' already exists!")

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
                label=":material/download: Export CSV",
                data=csv_data,
                file_name="contacts_export.csv",
                mime="text/csv",
                use_container_width=True
            )

    if not contacts:
        st.info("No contacts found in this category. Add some from the first tab!")
    else:
        grid_col1, grid_col2 = st.columns(2)
        for idx, (c_name, c_phone, c_email, c_cat) in enumerate(contacts):
            with (grid_col1 if idx % 2 == 0 else grid_col2):
                render_contact_card(c_name, c_phone, c_email, c_cat)

# TAB 3: SMART SEARCH
with tab3:
    st.markdown("#### :material/manage_search: Instant Search")
    query = st.text_input("Type any letter of Name or digits of Phone Number:", placeholder="Search here...").strip()

    if query:
        results = search_db_contact(query)
        if results:
            st.success(f"Found {len(results)} matching connection(s)")
            for c_name, c_phone, c_email, c_cat in results:
                render_contact_card(c_name, c_phone, c_email, c_cat)
        else:
            st.error("No matching contacts found.")

# TAB 4: EDIT CONTACT
with tab4:
    st.markdown("#### :material/tune: Update Contact Info")
    if not all_contacts:
        st.info("No contacts available to edit.")
    else:
        contact_names = [c[0] for c in all_contacts]
        selected_name = st.selectbox("Select Person to Update:", contact_names)
        current_data = [c for c in all_contacts if c[0] == selected_name][0]

        with st.form("edit_form"):
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                new_phone = st.text_input("Phone Number", value=current_data[1])
                new_email = st.text_input("Email Address", value=current_data[2])
            with e_col2:
                cat_index = CATEGORIES.index(current_data[3]) if current_data[3] in CATEGORIES else 4
                new_cat = st.selectbox("Category Tag", CATEGORIES, index=cat_index)

            update_btn = st.form_submit_button(":material/sync: Save Changes", use_container_width=True)
            if update_btn:
                if not is_valid_phone(new_phone):
                    st.error("Invalid Phone Number!")
                elif not is_valid_email(new_email):
                    st.error("Invalid Email format!")
                else:
                    update_db_contact(selected_name, new_phone.strip(), new_email.strip(), new_cat)
                    st.success(f"'{selected_name}' updated successfully!")
                    st.rerun()

# TAB 5: DELETE CONTACT
with tab5:
    st.markdown("#### :material/person_remove: Remove Connection")
    if not all_contacts:
        st.info("No contacts available to delete.")
    else:
        del_name = st.selectbox("Select contact to permanently remove:", [c[0] for c in all_contacts])
        if st.button(":material/delete_forever: Delete Permanently", use_container_width=True):
            if delete_db_contact(del_name):
                st.success(f"'{del_name}' removed!")
                st.rerun()