import re
import csv
import socket
import io
from difflib import SequenceMatcher
import qrcode

def is_valid_phone(phone):
    """Checks if phone number is 10 digits (allows optional +91)."""
    pattern = r"^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$|^\d{10}$"
    return bool(re.match(pattern, phone.strip()))

def is_valid_email(email):
    """Checks if email format is valid (empty email is allowed)."""
    if not email.strip():
        return True
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def format_whatsapp_url(phone):
    """Formats phone number into a clean wa.me link."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        digits = "91" + digits
    return f"https://wa.me/{digits}"

def convert_to_csv(contacts):
    """Converts list of contact dicts into CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Phone", "Email", "Category", "Favorite", "Notes", "Created At", "Last Contacted"])
    for c in contacts:
        writer.writerow([
            c["name"], c["phone"], c["email"], c["category"],
            "Yes" if c["is_favorite"] else "No",
            c["notes"], c["created_at"], c["last_contacted"]
        ])
    return output.getvalue()

def generate_vcard_qr(contact):
    """Generates a scannable vCard 3.0 QR code PNG in memory."""
    vcard = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{contact['name']}\n"
        f"TEL;TYPE=CELL:{contact['phone']}\n"
        f"EMAIL:{contact['email']}\n"
        f"CATEGORIES:{contact['category']}\n"
        f"NOTE:{contact['notes']}\n"
        "END:VCARD"
    )
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(vcard)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e1b4b", back_color="#ffffff")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def fuzzy_search_contacts(contacts, query, threshold=0.55):
    """Supports partial matches and typo-tolerant fuzzy matching."""
    q = query.strip().lower()
    if not q:
        return []

    scored = []
    for c in contacts:
        name_l = c["name"].lower()
        phone_l = c["phone"].lower()
        notes_l = (c["notes"] or "").lower()

        if q in name_l or q in phone_l or q in notes_l:
            scored.append((1.0, c))
            continue

        name_ratio = SequenceMatcher(None, q, name_l).ratio()
        word_ratios = [SequenceMatcher(None, q, w).ratio() for w in name_l.split()]
        best_ratio = max([name_ratio] + word_ratios)

        if best_ratio >= threshold:
            scored.append((best_ratio, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored]

def find_duplicates(contacts):
    """Detects identical phone numbers and highly similar contact names."""
    alerts = []
    n = len(contacts)
    for i in range(n):
        for j in range(i + 1, n):
            c1, c2 = contacts[i], contacts[j]
            p1 = re.sub(r"\D", "", c1["phone"])[-10:]
            p2 = re.sub(r"\D", "", c2["phone"])[-10:]

            reasons = []
            if p1 and p1 == p2:
                reasons.append("Identical Phone Number")

            name_sim = SequenceMatcher(None, c1["name"].lower(), c2["name"].lower()).ratio()
            if name_sim >= 0.80:
                reasons.append(f"Similar Name ({int(name_sim * 100)}% match)")

            if reasons:
                alerts.append({
                    "contact_a": c1["name"],
                    "contact_b": c2["name"],
                    "reason": " & ".join(reasons)
                })
    return alerts

def get_local_ip():
    """Gets your laptop's local Wi-Fi IP address for phone scanning."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_url_qr(url):
    """Generates a scannable QR code PNG for any URL."""
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e1b4b", back_color="#ffffff")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()