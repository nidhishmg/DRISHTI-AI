import re
import hashlib
from typing import Dict, Any, Optional

class PIIRedactor:
    def __init__(self):
        # Basic patterns (Mock for demo)
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            # Indian Aadhaar (Mock 12 digit)
            "aadhaar": r'\b\d{4}\s\d{4}\s\d{4}\b'
        }
        self.salt = "somesalt" # In prod, rotate from Vault

    def redact_text(self, text: str) -> str:
        for name, pattern in self.patterns.items():
            text = re.sub(pattern, f"[REDACTED-{name.upper()}]", text)
        return text

    def tokenize(self, value: str) -> str:
        """Deterministic tokenization for analytics without revealing raw value."""
        return hashlib.sha256((value + self.salt).encode()).hexdigest()

    def process_document(self, doc: Dict[str, Any], fields_to_scrub: list = ["text", "description"]) -> Dict[str, Any]:
        """Scrub specified fields in a document."""
        new_doc = doc.copy()
        for field in fields_to_scrub:
            if field in new_doc and isinstance(new_doc[field], str):
                new_doc[field] = self.redact_text(new_doc[field])
        return new_doc
