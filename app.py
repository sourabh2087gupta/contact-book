import math
from collections import Counter
import plotly.graph_objects as go
import streamlit as st
from database import (
    init_db, add_db_contact, get_all_contacts,
    toggle_favorite, log_last_contacted,
    update_db_contact, delete_db_contact
)
from utils import (
    is_valid_phone, is_valid_email, format_whatsapp_url,
    convert_to_csv, generate_vcard_qr,
    fuzzy_search_contacts, find_duplicates,
    get_local_ip, generate_url_qr
)

st.set_page_config(page_title="Smart Contact Hub", page_icon=":material/hub:", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_db()

CATEGORIES = ["Family", "Friends", "College", "Work", "General"]

# ==========================================
# MOBILE QUICK-ADD MODE (When scanned by phone)
# ==========================================
if st.query_params.get("mode") == "mobile_add":
    st.markdown("""
<div class="hero-card">
<div class="main-title" style="font-size: 28px;">Quick Add Contact</div>
<p class="sub-text">Submit details here to sync directly to Smart Contact Hub</p>
</div>
""", unsafe_allow_html=True)

    with st.form("mobile_add_form", clear_on_submit=True):
        m_name = st.text_input("Full Name", placeholder="e.g. Rohan Sharma")
        m_phone = st.text_input("Phone Number (10 digits)", placeholder="9876543210")
        m_email = st.text_input("Email Address (Optional)", placeholder="rohan@example.com")
        m_cat = st.selectbox("Category", CATEGORIES)
        m_notes = st.text_area("Notes (Optional)", placeholder="Met at college / event...", height=70)
        m_submit = st.form_submit_button("Send to System", icon=":material/send:", use_container_width=True)

        if m_submit:
            if not m_name.strip() or not m_phone.strip():
                st.warning("Name and Phone Number are required.")
            elif not is_valid_phone(m_phone):
                st.error("Invalid Phone Number! Enter a valid 10-digit number.")
            elif not is_valid_email(m_email):
                st.error("Invalid Email format!")
            else:
                if add_db_contact(m_name.strip(), m_phone.strip(), m_email.strip(), m_cat, 0, m_notes.strip()):
                    st.success(f"'{m_name}' synced to your system!")
                    st.balloons()
                else:
                    st.error(f"Contact '{m_name}' already exists!")
    st.stop()

# ==========================================
# DESKTOP DASHBOARD MODE
# ==========================================
SVG_HERO = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_USERS = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_STAR = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
SVG_STAR_SM = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#fbbf24" stroke="#fbbf24" stroke-width="1.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
SVG_GRAD = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
SVG_RADAR = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
SVG_PHONE = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_MAIL = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

# --- Hero Header ---
st.markdown(f"""
<div class="hero-card">
<div class="hero-icon-wrap">{SVG_HERO}</div>
<div class="main-title">Smart Contact Hub</div>
<p class="sub-text">Personal CRM with QR vCards, Phone Sync &amp; Network Analytics</p>
</div>
""", unsafe_allow_html=True)

all_contacts = get_all_contacts("All")
duplicates = find_duplicates(all_contacts)

# --- Live Stats Bar ---
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-blue">{SVG_USERS}</div><div><div class="stat-num">{len(all_contacts)}</div><div class="stat-label">Total Contacts</div></div></div>', unsafe_allow_html=True)
with s2:
    vip_count = sum(1 for c in all_contacts if c["is_favorite"])
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-amber">{SVG_STAR}</div><div><div class="stat-num">{vip_count}</div><div class="stat-label">VIP Favorites</div></div></div>', unsafe_allow_html=True)
with s3:
    net_count = sum(1 for c in all_contacts if c["category"] in ["College", "Work"])
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-purple">{SVG_GRAD}</div><div><div class="stat-num">{net_count}</div><div class="stat-label">Pro &amp; College</div></div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="stat-box"><div class="stat-icon icon-pink">{SVG_RADAR}</div><div><div class="stat-num">{len(duplicates)}</div><div class="stat-label">Duplicate Alerts</div></div></div>', unsafe_allow_html=True)

# --- Top Navigation Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    ":material/person_add: Add New",
    ":material/contacts: Directory",
    ":material/search: Smart Search",
    ":material/insights: Insights",
    ":material/edit_square: Edit",
    ":material/delete_sweep: Remove"
])

def render_contact_card(contact, key_prefix="dir"):
    name = contact["name"]
    phone = contact["phone"]
    email = contact["email"]
    cat = contact["category"]
    is_fav = contact["is_favorite"]
    notes = contact["notes"]
    last_c = contact["last_contacted"]

    initial = name[0].upper() if name else "?"
    email_display = email if email else "No email linked"
    vip_class = "vip-card" if is_fav else ""
    vip_star = SVG_STAR_SM if is_fav else ""

    wa_url = format_whatsapp_url(phone)
    mail_html = f'<a class="smart-link link-mail" href="mailto:{email}">Email</a>' if email else ""
    note_html = f'<div class="note-pill">{notes}</div>' if notes else ""
    last_html = f'<span class="meta-item">Last contacted: {last_c}</span>' if last_c else ""

    # Zero-indentation HTML prevents Markdown from rendering it as a code block
    card_html = (
        f'<div class="contact-card {vip_class}">'
        f'<div class="card-top">'
        f'<div class="contact-left">'
        f'<div class="avatar">{initial}</div>'
        f'<div class="contact-info">'
        f'<h4>{name} {vip_star}</h4>'
        f'<div class="meta-row">'
        f'<span class="meta-item">{SVG_PHONE} {phone}</span>'
        f'<span class="meta-item">{SVG_MAIL} {email_display}</span>'
        f'{last_html}'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<span class="badge badge-{cat}">{cat}</span>'
        f'</div>'
        f'{note_html}'
        f'<div class="action-links">'
        f'<a class="smart-link link-wa" href="{wa_url}" target="_blank">WhatsApp</a>'
        f'{mail_html}'
        f'</div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # Interactive Smart Action Row
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        star_icon = ":material/star:" if is_fav else ":material/star_outline:"
        if st.button("VIP", icon=star_icon, key=f"{key_prefix}_fav_{name}", use_container_width=True):
            toggle_favorite(name, is_fav)
            st.rerun()
    with a2:
        with st.popover("QR vCard", icon=":material/qr_code_2:", use_container_width=True):
            qr_bytes = generate_vcard_qr(contact)
            st.image(qr_bytes, caption=f"Scan to save {name}", use_container_width=True)
    with a3:
        with st.popover("Copy", icon=":material/content_copy:", use_container_width=True):
            st.code(f"{name}\nPhone: {phone}\nEmail: {email_display}", language="text")
    with a4:
        if st.button("Pinged", icon=":material/check_circle:", key=f"{key_prefix}_ping_{name}", use_container_width=True):
            log_last_contacted(name)
            st.rerun()
    st.write("")

# TAB 1: ADD CONTACT (2 Columns: Manual Form + Phone QR Sync)
with tab1:
    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        st.markdown("#### :material/add_circle: Create New Connection")
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name", placeholder="e.g. Rohan Sharma")
                email = st.text_input("Email Address", placeholder="rohan@example.com")
            with c2:
                phone = st.text_input("Phone Number (10 digits)", placeholder="9876543210")
                category = st.selectbox("Category Tag", CATEGORIES)

            notes = st.text_area("Follow-up Notes (Optional)", placeholder="Met at hackathon, follow up about AI project...", height=80)
            is_fav = st.checkbox("Mark as VIP / Favorite (Pinned to top)")

            submit = st.form_submit_button("Save to Directory", icon=":material/rocket_launch:", use_container_width=True)
            if submit:
                if not name.strip() or not phone.strip():
                    st.warning("Name and Phone Number are required.")
                elif not is_valid_phone(phone):
                    st.error("Invalid Phone Number! Enter a valid 10-digit number.")
                elif not is_valid_email(email):
                    st.error("Invalid Email format!")
                else:
                    if add_db_contact(name.strip(), phone.strip(), email.strip(), category, is_fav, notes.strip()):
                        st.success(f"'{name}' added under {category}!")
                        st.rerun()
                    else:
                        st.error(f"Contact '{name}' already exists!")

    with right_col:
        st.markdown("#### :material/qr_code_scanner: Add via Phone")
        local_ip = get_local_ip()
        mobile_url = f"http://{local_ip}:8501/?mode=mobile_add"
        qr_img = generate_url_qr(mobile_url)

        st.image(qr_img, caption="Scan with your phone camera (same Wi-Fi)", use_container_width=True)
        st.code(mobile_url, language="text")
        if st.button("Refresh Synced Contacts", icon=":material/refresh:", use_container_width=True):
            st.rerun()

# TAB 2: DIRECTORY & EXPORT
with tab2:
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        cat_filter = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
    with f2:
        st.write("")
        st.write("")
        fav_only = st.toggle("VIP Favorites Only")
    with f3:
        st.write("")
        st.write("")
        contacts = get_all_contacts(cat_filter, fav_only)
        if contacts:
            st.download_button(
                label="Export CSV",
                icon=":material/download:",
                data=convert_to_csv(contacts),
                file_name="contacts_export.csv",
                mime="text/csv",
                use_container_width=True
            )

    if not contacts:
        st.info("No contacts match your current filter.")
    else:
        g1, g2 = st.columns(2)
        for idx, c in enumerate(contacts):
            with (g1 if idx % 2 == 0 else g2):
                render_contact_card(c, key_prefix="dir")

# TAB 3: FUZZY SEARCH & DUPLICATE RADAR
with tab3:
    st.markdown("#### :material/manage_search: Smart Fuzzy Search")
    query = st.text_input("Search by name, phone, or notes (typo-tolerant):", placeholder="e.g. 'Rohn' finds 'Rohan'").strip()
    if query:
        results = fuzzy_search_contacts(all_contacts, query)
        if results:
            st.success(f"Found {len(results)} matching connection(s)")
            for c in results:
                render_contact_card(c, key_prefix="search")
        else:
            st.error("No matching contacts found.")

    st.divider()
    st.markdown("#### :material/radar: Duplicate Radar")
    if not duplicates:
        st.success("Your directory is clean—no duplicate phone numbers or near-identical names detected.")
    else:
        for d in duplicates:
            st.markdown(
                f'<div class="radar-alert"><strong>Potential Duplicate:</strong> {d["contact_a"]} &amp; {d["contact_b"]} &mdash; {d["reason"]}</div>',
                unsafe_allow_html=True
            )

# TAB 4: INTERACTIVE NETWORK INSIGHTS
with tab4:
    st.markdown("#### :material/insights: Network Analytics")
    if not all_contacts:
        st.info("Add a few contacts to unlock interactive network charts.")
    else:
        ch1, ch2 = st.columns(2)

        with ch1:
            cat_counts = Counter(c["category"] for c in all_contacts)
            fig_donut = go.Figure(data=[go.Pie(
                labels=list(cat_counts.keys()),
                values=list(cat_counts.values()),
                hole=0.55,
                marker=dict(colors=["#38bdf8", "#818cf8", "#f472b6", "#fbbf24", "#34d399"])
            )])
            fig_donut.update_layout(
                title="Category Distribution",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", legend_title_text=""
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with ch2:
            date_counts = Counter(c["created_at"] for c in all_contacts)
            sorted_dates = sorted(date_counts.keys())
            cumulative, running = [], 0
            for d in sorted_dates:
                running += date_counts[d]
                cumulative.append(running)

            fig_line = go.Figure(data=[go.Scatter(
                x=sorted_dates, y=cumulative,
                mode="lines+markers", fill="tozeroy",
                line=dict(color="#a855f7", width=3),
                fillcolor="rgba(168, 85, 247, 0.2)"
            )])
            fig_line.update_layout(
                title="Network Growth Over Time",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", xaxis_title="Date", yaxis_title="Total Contacts"
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # Interactive Hub-and-Spoke Connection Network Graph
        edge_x, edge_y = [], []
        node_x, node_y, node_text, node_color, node_size = [0], [0], ["You (Hub)"], ["#ec4899"], [28]

        cats_present = list(cat_counts.keys())
        for ci, cat in enumerate(cats_present):
            angle = (2 * math.pi * ci) / max(len(cats_present), 1)
            cx, cy = 2.2 * math.cos(angle), 2.2 * math.sin(angle)
            edge_x += [0, cx, None]
            edge_y += [0, cy, None]
            node_x.append(cx)
            node_y.append(cy)
            node_text.append(f"Category: {cat}")
            node_color.append("#818cf8")
            node_size.append(20)

            cat_members = [c["name"] for c in all_contacts if c["category"] == cat]
            for mi, member in enumerate(cat_members):
                m_angle = angle + ((mi - (len(cat_members) - 1) / 2) * 0.35)
                mx, my = 4.0 * math.cos(m_angle), 4.0 * math.sin(m_angle)
                edge_x += [cx, mx, None]
                edge_y += [cy, my, None]
                node_x.append(mx)
                node_y.append(my)
                node_text.append(member)
                node_color.append("#38bdf8")
                node_size.append(13)

        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(
            x=edge_x, y=edge_y, mode="lines",
            line=dict(width=1.2, color="rgba(148, 163, 184, 0.35)"), hoverinfo="none"
        ))
        fig_net.add_trace(go.Scatter(
            x=node_x, y=node_y, mode="markers+text", text=node_text,
            textposition="top center", textfont=dict(color="#e2e8f0", size=11),
            marker=dict(size=node_size, color=node_color, line=dict(width=1.5, color="#ffffff")),
            hoverinfo="text"
        ))
        fig_net.update_layout(
            title="Interactive Connection Network Graph",
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=460
        )
        st.plotly_chart(fig_net, use_container_width=True)

# TAB 5: EDIT CONTACT
with tab5:
    st.markdown("#### :material/tune: Update Contact Info")
    if not all_contacts:
        st.info("No contacts available to edit.")
    else:
        selected_name = st.selectbox("Select Person to Update", [c["name"] for c in all_contacts])
        curr = next(c for c in all_contacts if c["name"] == selected_name)

        with st.form("edit_form"):
            e1, e2 = st.columns(2)
            with e1:
                new_phone = st.text_input("Phone Number", value=curr["phone"])
                new_email = st.text_input("Email Address", value=curr["email"])
            with e2:
                cat_idx = CATEGORIES.index(curr["category"]) if curr["category"] in CATEGORIES else 4
                new_cat = st.selectbox("Category Tag", CATEGORIES, index=cat_idx)
                new_fav = st.checkbox("VIP / Favorite", value=bool(curr["is_favorite"]))

            new_notes = st.text_area("Follow-up Notes", value=curr["notes"], height=80)
            if st.form_submit_button("Save Changes", icon=":material/sync:", use_container_width=True):
                if not is_valid_phone(new_phone):
                    st.error("Invalid Phone Number!")
                elif not is_valid_email(new_email):
                    st.error("Invalid Email format!")
                else:
                    update_db_contact(selected_name, new_phone.strip(), new_email.strip(), new_cat, new_notes.strip(), new_fav)
                    st.success(f"'{selected_name}' updated!")
                    st.rerun()

# TAB 6: DELETE CONTACT
with tab6:
    st.markdown("#### :material/person_remove: Remove Connection")
    if not all_contacts:
        st.info("No contacts available to delete.")
    else:
        del_name = st.selectbox("Select contact to permanently remove", [c["name"] for c in all_contacts])
        if st.button("Delete Permanently", icon=":material/delete_forever:", use_container_width=True):
            if delete_db_contact(del_name):
                st.success(f"'{del_name}' removed!")
                st.rerun()