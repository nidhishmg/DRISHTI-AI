import hashlib
import os
import re
from typing import Optional

# Salt should ideally be loaded from a secure secret manager
SALT = os.getenv("PHONE_HASH_SALT", "default_salt_change_me_in_prod")

def hash_phone_number(phone: str) -> str:
    """
    Hash a phone number using SHA-256 and a salt.
    Input should be E.164 format if possible.
    """
    if not phone:
        return ""
    
    # Basic normalization (remove spaces, dashes) - expecting better validation upstream
    clean_phone = re.sub(r'[\s\-]', '', phone)
    
    payload = f"{clean_phone}{SALT}".encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

def strip_pii(text: str) -> str:
    """
    Remove basic PII (names, phone numbers, identifiers) from text.
    This is a basic regex-based implementation.
    """
    if not text:
        return ""
        
    # Redact Phone Numbers (India & Intl patterns)
    # Matches +91-xxxxx-xxxxx or 10 digit numbers
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\d{10}|\d{5}[-.\s]?\d{5})'
    text = re.sub(phone_pattern, '[REDACTED_PHONE]', text)
    
    # Redact Aadhaar-like numbers (12 digits)
    aadhaar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    text = re.sub(aadhaar_pattern, '[REDACTED_UID]', text)
    
    # Redact PAN-like strings (5 letters, 4 digits, 1 letter)
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    text = re.sub(pan_pattern, '[REDACTED_PAN]', text)
    
    return text
