import pytest
from src.core.security import strip_pii, hash_phone_number
from src.ingest.dedup import FingerprintService

def test_pii_stripping():
    text = "Call me at +91-9876543210 regarding my ration."
    clean = strip_pii(text)
    assert "[REDACTED_PHONE]" in clean
    assert "+91" not in clean

def test_phone_hashing():
    p1 = "9876543210"
    p2 = "98765-43210"
    assert hash_phone_number(p1) == hash_phone_number(p2)

def test_simhash_similarity():
    t1 = "Government ration shop closed for 3 days"
    t2 = "Government ration shop closed since 3 days"
    
    h1 = FingerprintService.compute_simhash(t1)
    h2 = FingerprintService.compute_simhash(t2)
    
    assert FingerprintService.is_duplicate_simhash(h1, h2)
