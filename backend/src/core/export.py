import hashlib
import json
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List

class ChainOfCustody:
    def __init__(self):
        self.chain = []
        self.last_hash = "0000"

    def add_entry(self, action: str, actor: str, artifact_id: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "actor": actor,
            "artifact_id": artifact_id,
            "previous_hash": self.last_hash
        }
        # Calculate hash of this entry
        entry_str = json.dumps(entry, sort_keys=True)
        self.last_hash = hashlib.sha256(entry_str.encode()).hexdigest()
        entry["hash"] = self.last_hash
        self.chain.append(entry)
        return entry

class SecureExportManager:
    def __init__(self):
        self.custody_log = ChainOfCustody()

    def generate_watermarked_content(self, content: str, user: str) -> str:
        """
        Mock PDF generation with watermark.
        In prod: Use reportlab to draw string watermark.
        """
        watermark = f"CONFIDENTIAL - {user} - {datetime.utcnow().isoformat()}"
        
        # Mocking PDF structure
        header = f"%PDF-1.4\n%Watermark: {watermark}\n"
        body = f"Content:\n{content}\n"
        footer = f"\n%EndDocument\n%ChainHash: {self.custody_log.last_hash}"
        
        return header + body + footer

    def create_encrypted_package(self, data: Dict[str, Any], password: str) -> bytes:
        """
        Mock creating an encrypted zip/pdf.
        In prod: Use pypdf or pycryptodome.
        """
        # Log export action
        self.custody_log.add_entry("EXPORT", "system", str(data.get("id", "unknown")))
        
        content = json.dumps(data, indent=2)
        safe_content = self.generate_watermarked_content(content, "admin_user")
        
        # Mock encryption (just XOR or encoding for demo)
        return safe_content.encode("utf-8")
