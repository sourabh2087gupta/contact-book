import streamlit as st
import pandas as pd
import plotly.express as px
import database as db
import utils

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Smart Contact Manager", page_icon="👥", layout="wide")

# Initialize Database dynamically
db.init_db()

# ==========================================
# CUSTOM CSS FOR MODERN UI
# ==========================================
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #1f77b4; }
    .metric-label { font-size: 1rem; color: #555; }
    .contact-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: white;
    }
    html[data-theme="dark"] .metric-card { background-color: #262730; }
    html[data-theme="dark"] .metric-label { color: #ccc; }
    html[data-theme="dark"] .contact-card { background-color: #1e1e1e; border-color: #333; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("👥 Smart Contacts")
st.sidebar.markdown("MCA Project by Sourabh Gupta")
menu = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "➕ Add Contact", 
    "👥 All Contacts", 
    "⭐ Favorites", 
    "🔍 Search & Assistant", 
    "📊 Analytics", 
    "⚙️ Settings"
])

# Load data globally for use across tabs
df_contacts = db.get_all_contacts()

# ==========================================
# 1. DASHBOARD
# ==========================================
if menu == "🏠 Dashboard":
    st.title("Welcome to Smart Contact Manager")
    st.markdown("Organize, search, and manage your contacts efficiently.")
    
    if not df_contacts.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df_contacts)}</div><div class="metric-label">Total Contacts</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df_contacts[df_contacts["is_favorite"] == 1])}</div><div class="metric-label">Favorites ⭐</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{df_contacts["category"].nunique()}</div><div class="metric-label">Categories</div></div>', unsafe_allow_html=True)
        with col4:
            recent_count = min(5, len(df_contacts))
            st.markdown(f'<div class="metric-card"><div class="metric-value">{recent_count}</div><div class="metric-label">Recently Added</div></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Recent Contacts")
        st.dataframe(df_contacts.tail(5)[['name', 'phone', 'email', 'category']], use_container_width=True, hide_index=True)
    else:
        st.info("Your contact book is empty. Go to 'Add Contact' to get started!")

# ==========================================
# 2. ADD CONTACT
# ==========================================
elif menu == "➕ Add Contact":
    st.title("➕ Add New Contact")
    
    with st.form("add_contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *")
            email = st.text_input("Email Address")
        with col2:
            category = st.selectbox("Category", ["General", "Work", "Family", "Friends", "Education", "Organization"])
            address = st.text_input("Location / Address")
            is_fav = st.checkbox("Mark as Favorite ⭐")
            
        notes = st.text_area("Notes")
        submit = st.form_submit_button("💾 Save Contact", type="primary")
        
        if submit:
            if not name or not phone:
                st.error("Name and Phone Number are required!")
            elif not utils.validate_phone(phone):
                st.error("Invalid phone number format.")
            elif email and not utils.validate_email(email):
                st.error("Invalid email format.")
            elif phone in df_contacts['phone'].values:
                st.warning("A contact with this phone number already exists!")
            else:
                db.add_contact(name, phone, email, address, category, notes, is_fav)
                st.success(f"Contact '{name}' added successfully!")
                st.rerun()

# ==========================================
# 3. ALL CONTACTS & PROFILE
# ==========================================
elif menu == "👥 All Contacts":
    st.title("👥 All Contacts")
    
    if df_contacts.empty:
        st.info("No contacts found.")
    else:
        # Action selection
        contact_names = df_contacts['name'].tolist()
        selected_name = st.selectbox("Select a contact to view/edit profile:", ["-- Select Contact --"] + contact_names)
        
        if selected_name != "-- Select Contact --":
            contact_data = df_contacts[df_contacts['name'] == selected_name].iloc[0]
            
            st.markdown("---")
            col_prof1, col_prof2 = st.columns([2, 1])
            
            with col_prof1:
                st.subheader(f"👤 {contact_data['name']} {'⭐' if contact_data['is_favorite'] else ''}")
                st.markdown(f"**📞 Phone:** {contact_data['phone']}")
                st.markdown(f"**📧 Email:** {contact_data['email'] if contact_data['email'] else 'N/A'}")
                st.markdown(f"**📍 Address:** {contact_data['address'] if contact_data['address'] else 'N/A'}")
                st.markdown(f"**🏷️ Category:** {contact_data['category']}")
                st.markdown(f"**📝 Notes:** {contact_data['notes'] if contact_data['notes'] else 'None'}")
                
            with col_prof2:
                # Actions
                if st.button("Toggle Favorite ⭐", use_container_width=True):
                    db.toggle_favorite(int(contact_data['id']), int(contact_data['is_favorite']))
                    st.rerun()
                
                with st.expander("✏️ Edit Contact"):
                    with st.form(f"edit_{contact_data['id']}"):
                        e_name = st.text_input("Name", contact_data['name'])
                        e_phone = st.text_input("Phone", contact_data['phone'])
                        e_email = st.text_input("Email", contact_data['email'])
                        e_address = st.text_input("Address", contact_data['address'])
                        cats = ["General", "Work", "Family", "Friends", "Education", "Organization"]
                        e_cat = st.selectbox("Category", cats, index=cats.index(contact_data['category']) if contact_data['category'] in cats else 0)
                        e_notes = st.text_area("Notes", contact_data['notes'])
                        if st.form_submit_button("Update"):
                            db.update_contact(int(contact_data['id']), e_name, e_phone, e_email, e_address, e_cat, e_notes, int(contact_data['is_favorite']))
                            st.success("Updated successfully!")
                            st.rerun()
                
                if st.button("🗑️ Delete Contact", type="primary", use_container_width=True):
                    db.delete_contact(int(contact_data['id']))
                    st.success("Contact deleted.")
                    st.rerun()

        st.write("---")
        st.dataframe(df_contacts[['name', 'phone', 'email', 'category']], use_container_width=True, hide_index=True)

# ==========================================
# 4. FAVORITES
# ==========================================
elif menu == "⭐ Favorites":
    st.title("⭐ Favorite Contacts")
    fav_df = df_contacts[df_contacts['is_favorite'] == 1]
    
    if fav_df.empty:
        st.info("You haven't marked any contacts as favorites yet.")
    else:
        for _, row in fav_df.iterrows():
            st.markdown(f"""
            <div class="contact-card">
                <h4>{row['name']} ⭐</h4>
                <p>📞 {row['phone']} &nbsp;&nbsp; | &nbsp;&nbsp; 📧 {row['email']}</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 5. SEARCH & SMART ASSISTANT
# ==========================================
elif menu == "🔍 Search & Assistant":
    st.title("🔍 Search & Smart Assistant")
    
    search_query = st.text_input("Search by Name, Phone, or Email...", "")
    
    if search_query:
        mask = (df_contacts['name'].str.contains(search_query, case=False, na=False)) | \
               (df_contacts['phone'].str.contains(search_query, case=False, na=False)) | \
               (df_contacts['email'].str.contains(search_query, case=False, na=False))
        results = df_contacts[mask]
        
        if results.empty:
            st.warning("No contacts found matching your search.")
        else:
            st.success(f"Found {len(results)} matches:")
            st.dataframe(results[['name', 'phone', 'email', 'category']], use_container_width=True, hide_index=True)
            
    st.write("---")
    st.subheader("🤖 Smart Assistant")
    st.info("The AI Assistant analyzes your data to find anomalies and suggest improvements.")
    
    if st.button("Analyze Database"):
        duplicates = utils.detect_duplicates(df_contacts)
        if duplicates:
            st.error("⚠️ Data Issues Found:")
            for dup in duplicates:
                st.write(f"- {dup}")
        else:
            st.success("✅ Your contact list is clean! No duplicate phones or emails detected.")

# ==========================================
# 6. ANALYTICS
# ==========================================
elif menu == "📊 Analytics":
    st.title("📊 Contact Analytics")
    
    if df_contacts.empty:
        st.warning("Not enough data to display analytics.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            # Pie Chart: Categories
            cat_counts = df_contacts['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig_cat = px.pie(cat_counts, names='Category', values='Count', title="Contacts by Category", hole=0.4)
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with col2:
            # Bar Chart: Favorites vs Regular
            fav_counts = df_contacts['is_favorite'].value_counts().reset_index()
            fav_counts['is_favorite'] = fav_counts['is_favorite'].map({0: 'Regular', 1: 'Favorite'})
            fav_counts.columns = ['Status', 'Count']
            fig_fav = px.bar(fav_counts, x='Status', y='Count', title="Favorites Breakdown", color='Status')
            st.plotly_chart(fig_fav, use_container_width=True)

# ==========================================
# 7. SETTINGS
# ==========================================
elif menu == "⚙️ Settings":
    st.title("⚙️ Settings & Data Management")
    
    st.subheader("Export Data")
    if not df_contacts.empty:
        csv = df_contacts.to_csv(index=False)
        st.download_button("📥 Download Contacts as CSV", data=csv, file_name="contacts_backup.csv", mime="text/csv")
    else:
        st.info("No data available to export.")
        
    st.write("---")
    st.subheader("Danger Zone")
    with st.expander("🗑️ Reset Database"):
        st.warning("This will permanently delete all your contacts. This action cannot be undone.")
        confirm = st.text_input("Type 'DELETE' to confirm:")
        if st.button("Clear All Data", type="primary"):
            if confirm == "DELETE":
                db.clear_all_contacts()
                st.success("Database has been reset successfully.")
                st.rerun()
            else:
                st.error("Confirmation text did not match.")