import re
import csv
import io

def is_valid_phone(phone):
    """Checks if phone number is 10 digits (allows optional +91)."""
    pattern = r"^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$|^\d{10}$"
    return bool(re.match(pattern, phone.strip()))

def is_valid_email(email):
    """Checks if email format is valid (empty email is allowed as optional)."""
    if not email.strip():
        return True
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def convert_to_csv(contacts):
    """Converts contact list into CSV string for downloading."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Phone", "Email", "Category"])
    for row in contacts:
        writer.writerow(row)
    return output.getvalue()