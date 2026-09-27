import re

def smart_categorize(email, notes, phone):
    """
    AI-Level Enhancement: Rule-based automatic categorization based on available data.
    """
    email = str(email).lower()
    notes = str(notes).lower()
    
    if any(domain in email for domain in ['.edu', 'university', 'college', 'school']):
        return "Education"
    if any(keyword in notes for keyword in ['manager', 'client', 'meeting', 'project', 'boss']):
        return "Work"
    if any(domain in email for domain in ['.gov', '.org']):
        return "Organization"
    if any(keyword in notes for keyword in ['mom', 'dad', 'brother', 'sister', 'uncle', 'aunt', 'wife', 'husband']):
        return "Family"
    
    return "General"

def detect_duplicates(df):
    """
    Detects contacts sharing the exact same phone number or email.
    """
    if df.empty:
        return []
    
    duplicates = []
    
    # Check for duplicate phones
    phone_counts = df['phone'].value_counts()
    dup_phones = phone_counts[phone_counts > 1].index.tolist()
    
    # Check for duplicate emails (ignore empty)
    email_counts = df[df['email'] != '']['email'].value_counts()
    dup_emails = email_counts[email_counts > 1].index.tolist()
    
    for phone in dup_phones:
        if phone.strip():
            duplicates.append(f"Duplicate Phone detected: {phone}")
            
    for email in dup_emails:
        if email.strip():
            duplicates.append(f"Duplicate Email detected: {email}")
            
    return duplicates

def validate_phone(phone):
    # Basic validation: allows +, -, spaces, and digits. Must be at least 7 chars.
    pattern = re.compile(r'^[\+\d\s\-]{7,20}$')
    return bool(pattern.match(str(phone)))

def validate_email(email):
    if not email: # Optional field
        return True
    pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    return bool(pattern.match(str(email)))