import re

def get_initials(name):
    """Generates 1-2 letter initials for the avatar."""
    if not name: return "?"
    parts = str(name).strip().split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    return parts[0][0].upper()

def smart_categorize(email, notes):
    """AI-Level Smart Feature: Auto-suggests category based on context."""
    text = f"{str(email)} {str(notes)}".lower()
    
    if any(k in text for k in ['.edu', 'university', 'college', 'mca', 'bca']):
        return "Education"
    if any(k in text for k in ['manager', 'client', 'meeting', 'project', 'dev']):
        return "Work"
    if any(k in text for k in ['mom', 'dad', 'brother', 'sister', 'family']):
        return "Family"
    return "General"

def detect_duplicates(df):
    """Smart Insights: Detects similar contacts."""
    if df.empty: return []
    duplicates = []
    
    # Phone duplicates
    phone_counts = df['phone'].value_counts()
    for phone in phone_counts[phone_counts > 1].index:
        if phone.strip(): duplicates.append(f"📞 Duplicate Phone: {phone}")
            
    # Email duplicates
    email_counts = df[df['email'] != '']['email'].value_counts()
    for email in email_counts[email_counts > 1].index:
        if email.strip(): duplicates.append(f"✉️ Duplicate Email: {email}")
            
    return duplicates

def validate_phone(phone):
    pattern = re.compile(r'^[\+\d\s\-]{7,20}$')
    return bool(pattern.match(str(phone)))

def validate_email(email):
    if not email: return True
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    return bool(pattern.match(str(email)))