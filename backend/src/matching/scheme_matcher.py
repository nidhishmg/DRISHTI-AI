from rapidfuzz import process, fuzz
from typing import List, Dict, Optional
from ..core.model_registry import ModelRegistry, AbstractModel

@ModelRegistry.register("scheme_matcher")
class SchemeMatcher(AbstractModel):
    def __init__(self):
        # In a real app, load this from DB or Config
        self.known_schemes = [
            "Pradhan Mantri Awas Yojana",
            "Mahatma Gandhi National Rural Employment Guarantee Act",
            "PM Kisan Samman Nidhi",
            "Ayushman Bharat",
            "Swachh Bharat Mission",
            "Jal Jeevan Mission"
        ]
        
        self.aliases = {
            "PMAY": "Pradhan Mantri Awas Yojana",
            "MNREGA": "Mahatma Gandhi National Rural Employment Guarantee Act",
            "MGNREGA": "Mahatma Gandhi National Rural Employment Guarantee Act",
            "PM Kisan": "PM Kisan Samman Nidhi"
        }

    def predict(self, text: str) -> dict:
        """
        Identify scheme mentions in text using fuzzy matching.
        """
        # 1. Direct Alias Lookup (Fastest)
        found_schemes = {}
        for word in text.split():
            clean_word = word.strip(".,!?").upper()
            if clean_word in self.aliases:
                target = self.aliases[clean_word]
                found_schemes[target] = 100.0

        # 2. Fuzzy Match against Known Schemes
        # Extract best match from the whole string (simple approach) or sliding window
        # Here we just check if any scheme is plausibly mentioned
        
        # Using extraction based on scheme list
        results = process.extract(
            text, 
            self.known_schemes, 
            scorer=fuzz.partial_ratio, 
            limit=3,
            score_cutoff=70
        )
        
        for scheme_name, score, _ in results:
            if scheme_name not in found_schemes or score > found_schemes[scheme_name]:
                found_schemes[scheme_name] = score

        # Format output
        matches = []
        for scheme, score in found_schemes.items():
            matches.append({
                "scheme_name": scheme,
                "confidence_score": score,
                "is_confident": score > 85
            })
            
        return {"matches": matches}
