import streamlit as st
import pandas as pd
import plotly.express as px
import database as db
import utils

# ==========================================
# PAGE CONFIGURATION (Must be first)
# ==========================================
st.set_page_config(page_title="Smart Contact Manager", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

# Load Custom CSS
# ==========================================
# CUSTOM CSS (Direct Injection)
# ==========================================
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Premium Metric Cards */
    .metric-container {
        background: rgba(30, 30, 36, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 242, 254, 0.15);
        border: 1px solid rgba(0, 242, 254, 0.3);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* Contact Cards */
    .contact-card {
        background: #1e1e24; /* Fallback color */
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .contact-card:hover {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.4);
        transform: translateY(-3px);
    }
    .avatar-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .contact-name {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0;
        color: #e0e0e0;
    }
    .contact-cat {
        font-size: 0.8rem;
        padding: 3px 10px;
        background: rgba(0, 242, 254, 0.1);
        color: #4facfe;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Button Styling */
    div.stButton > button {
        border-radius: 8px !important;
        transition: all 0.3s !important;
    }
    div.stButton > button:hover {
        border-color: #00f2fe !important;
        color: #00f2fe !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize DB
db.init_db()
df_contacts = db.get_all_contacts()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### ✨ Smart Network")
    st.markdown("<p style='color: #888; font-size: 0.85rem;'>MCA Project • Sourabh Gupta</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = st.radio("Navigation", [
        "⌂ Dashboard", 
        "👥 All Contacts", 
        "➕ Add Contact", 
        "⭐ Favorites", 
        "🔎 Smart Search", 
        "📊 Analytics"
    ], label_visibility="collapsed")
    
    st.write("---")
    st.markdown("🟢 **System Status:** Online")
    st.markdown(f"📦 **Database:** {len(df_contacts)} records")

# ==========================================
# 1. DASHBOARD
# ==========================================
if menu == "⌂ Dashboard":
    st.markdown("<h1>Good morning, Sourabh 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; font-size: 1.1rem;'>Organize your connections. Find anyone instantly.</p>", unsafe_allow_html=True)
    st.write("") # spacing
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{len(df_contacts)}</div>
            <div class="metric-label">Total Contacts</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        fav_count = len(df_contacts[df_contacts["is_favorite"] == 1]) if not df_contacts.empty else 0
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{fav_count}</div>
            <div class="metric-label">Favorites ⭐</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        cat_count = df_contacts["category"].nunique() if not df_contacts.empty else 0
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{cat_count}</div>
            <div class="metric-label">Categories</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">✨</div>
            <div class="metric-label">Smart Active</div>
        </div>
        ''', unsafe_allow_html=True)

    st.write("---")
    if df_contacts.empty:
        st.info("👥 No contacts yet. Start building your smart network!")
        if st.button("➕ Add Your First Contact", type="primary"):
            st.toast("Navigate to 'Add Contact' in the sidebar!")

# ==========================================
# 2. ALL CONTACTS (BEAUTIFUL GRID)
# ==========================================
elif menu == "👥 All Contacts":
    st.header("👥 Your Network")
    
    if df_contacts.empty:
        st.warning("Your contact book is empty.")
    else:
        # Create a responsive 3-column grid
        cols = st.columns(3)
        for index, row in df_contacts.iterrows():
            col = cols[index % 3] # Distribute cards across columns
            
            with col:
                initials = utils.get_initials(row['name'])
                fav_icon = "⭐" if row['is_favorite'] else ""
                
                # HTML Card
                st.markdown(f'''
                <div class="contact-card">
                    <div class="avatar-row">
                        <div class="avatar">{initials}</div>
                        <div>
                            <p class="contact-name">{row['name']} {fav_icon}</p>
                            <span class="contact-cat">{row['category']}</span>
                        </div>
                    </div>
                    <div class="contact-detail">📞 {row['phone']}</div>
                    <div class="contact-detail">✉️ {row['email'] if row['email'] else 'N/A'}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Action Buttons inside Streamlit (placed right below the HTML card)
                b1, b2, b3 = st.columns([1,1,1])
                with b1:
                    if st.button("⭐", key=f"fav_{row['id']}", help="Toggle Favorite"):
                        db.toggle_favorite(row['id'], row['is_favorite'])
                        st.rerun()
                with b2:
                    with st.popover("✏️"):
                        st.markdown("**Edit Contact**")
                        e_name = st.text_input("Name", row['name'], key=f"en_{row['id']}")
                        e_phone = st.text_input("Phone", row['phone'], key=f"ep_{row['id']}")
                        if st.button("Save", key=f"es_{row['id']}", type="primary"):
                            db.update_contact(row['id'], e_name, e_phone, row['email'], row['address'], row['category'], row['notes'], row['is_favorite'])
                            st.toast(f"✅ {e_name} updated successfully!")
                            st.rerun()
                with b3:
                    if st.button("🗑️", key=f"del_{row['id']}", help="Delete"):
                        db.delete_contact(row['id'])
                        st.toast(f"🗑️ Contact deleted.")
                        st.rerun()

# ==========================================
# 3. ADD CONTACT (PREMIUM FORM)
# ==========================================
elif menu == "➕ Add Contact":
    st.header("Create New Contact")
    st.markdown("<p style='color: #888;'>Add someone to your personal network.</p>", unsafe_allow_html=True)
    
    with st.container():
        with st.form("add_contact_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="e.g. John Doe")
                phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                email = st.text_input("Email Address", placeholder="john@example.com")
            with col2:
                notes = st.text_area("Notes", placeholder="Met at the college hackathon...", height=115)
                address = st.text_input("Location / Address", placeholder="Delhi, India")
            
            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                # Smart Suggestion Trigger
                suggested_cat = "General"
                cats = ["General", "Work", "Family", "Friends", "Education", "Organization"]
                category = st.selectbox("Category", cats)
            with c2:
                st.write("")
                st.write("")
                is_fav = st.checkbox("⭐ Add to Favorites")
                
            st.write("---")
            submit = st.form_submit_button("✨ Create Contact", type="primary", use_container_width=True)
            
            if submit:
                if not name or not phone:
                    st.error("Name and Phone Number are required!")
                elif not utils.validate_phone(phone):
                    st.error("Invalid phone number format.")
                elif phone in df_contacts['phone'].values:
                    st.error("A contact with this phone number already exists!")
                else:
                    # Apply Smart Category if user left it as General but notes imply otherwise
                    final_cat = category
                    if category == "General" and (email or notes):
                        final_cat = utils.smart_categorize(email, notes)
                        
                    db.add_contact(name, phone, email, address, final_cat, notes, is_fav)
                    st.toast(f"✅ {name} added to {final_cat} successfully!")
                    st.rerun()

# ==========================================
# 4. FAVORITES
# ==========================================
elif menu == "⭐ Favorites":
    st.header("⭐ Favorite Connections")
    fav_df = df_contacts[df_contacts['is_favorite'] == 1]
    
    if fav_df.empty:
        st.info("⭐ No favorite contacts yet. Mark contacts as favorites to access them quickly here.")
    else:
        cols = st.columns(3)
        for index, row in fav_df.iterrows():
            with cols[index % 3]:
                st.markdown(f'''
                <div class="contact-card" style="border-color: rgba(255, 215, 0, 0.3);">
                    <div class="avatar-row">
                        <div class="avatar" style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);">{utils.get_initials(row['name'])}</div>
                        <div>
                            <p class="contact-name">{row['name']}</p>
                            <span class="contact-cat">{row['category']}</span>
                        </div>
                    </div>
                    <div class="contact-detail">📞 {row['phone']}</div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button("Remove ⭐", key=f"rem_{row['id']}", use_container_width=True):
                    db.toggle_favorite(row['id'], 1)
                    st.rerun()

# ==========================================
# 5. SMART SEARCH & INSIGHTS
# ==========================================
elif menu == "🔎 Smart Search":
    st.header("🔎 Search & Insights")
    
    search_query = st.text_input("Search contacts by name, email or phone...", placeholder="Type to search...", label_visibility="collapsed")
    
    if search_query:
        mask = (df_contacts['name'].str.contains(search_query, case=False, na=False)) | \
               (df_contacts['phone'].str.contains(search_query, case=False, na=False)) | \
               (df_contacts['email'].str.contains(search_query, case=False, na=False))
        results = df_contacts[mask]
        
        st.markdown(f"**{len(results)} contacts found**")
        st.dataframe(results[['name', 'phone', 'email', 'category']], use_container_width=True, hide_index=True)
    
    st.write("---")
    st.subheader("🤖 Smart Contact Insights")
    st.markdown("AI-driven duplicate detection to keep your network clean.")
    
    if st.button("Run Network Scan", type="primary"):
        with st.spinner("Scanning database..."):
            duplicates = utils.detect_duplicates(df_contacts)
            if duplicates:
                for dup in duplicates:
                    st.error(dup)
            else:
                st.success("✅ Your network is perfectly clean! No duplicates found.")

# ==========================================
# 6. ANALYTICS
# ==========================================
elif menu == "📊 Analytics":
    st.header("📊 Network Analytics")
    
    if df_contacts.empty:
        st.warning("Not enough data to generate analytics.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            cat_counts = df_contacts['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            fig1 = px.pie(cat_counts, names='Category', values='Count', hole=0.5, 
                          color_discrete_sequence=px.colors.sequential.Teal)
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            st.write("")
            st.write("")
            st.markdown("### Export Data")
            st.markdown("Download your entire network securely as a CSV file.")
            csv = df_contacts.to_csv(index=False)
            st.download_button("📥 Download Backup (.csv)", data=csv, file_name="smart_contacts_backup.csv", mime="text/csv", type="primary")