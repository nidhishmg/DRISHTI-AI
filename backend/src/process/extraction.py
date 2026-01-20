import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from ..core.model_registry import ModelRegistry, AbstractModel
from ..config.settings import get_settings

settings = get_settings()

@ModelRegistry.register("entity_extractor")
class SpacyEntityExtractor(AbstractModel):
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load(settings.NER_MODEL)
        except OSError:
            # Fallback or auto-download might be risky in prod, better to error or warn
            print(f"Warning: Model {settings.NER_MODEL} not found. Ensure it is downloaded.")
            self.nlp = spacy.blank("en") # Stub

        # PII Engines
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def predict(self, text: str) -> dict:
        """
        Extract named entities and redact PII.
        """
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
            
        # PII Redaction
        pii_results = self.analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "AADHAAR"], language='en')
        anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=pii_results)
        
        return {
            "entities": entities,
            "redacted_text": anonymized_result.text,
            "pii_detected": [r.entity_type for r in pii_results]
        }
