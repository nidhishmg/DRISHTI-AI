import pytest
from unittest.mock import MagicMock, patch
import logging

# Import modules to test
from backend.src.core.model_registry import ModelRegistry
from backend.src.process.orchestrator import PipelineOrchestrator
from backend.src.matching.scheme_matcher import SchemeMatcher

# Stubbing dependencies that might not be installed in the test env without full setup
# (e.g. if running in a minimal CI container without the big models)

@pytest.fixture
def mock_settings():
    with patch("backend.src.config.settings.get_settings") as mock:
        mock.return_value.ENABLE_STREAM_PROCESSING = True
        yield mock

class TestMLPipeline:
    
    def test_model_registry(self):
        """Test that models can be registered and retrieved."""
        @ModelRegistry.register("test_model")
        class TestModel:
            def __init__(self):
                pass
            def predict(self, x):
                return x
        
        model = ModelRegistry.get_model("test_model")
        assert model is not None
        assert model.predict("foo") == "foo"

    def test_scheme_matcher(self):
        """Test fuzzy scheme matching."""
        matcher = SchemeMatcher()
        
        # Test exact alias
        res = matcher.predict("Funds not received for PMAY scheme")
        found = [m['scheme_name'] for m in res['matches']]
        assert "Pradhan Mantri Awas Yojana" in found
        
        # Test fuzzy match
        # Using a mock for rapidfuzz if needed, but assuming library is present
        # If rapidfuzz is missing, this might fail, so we wrap
        try:
            res_fuzzy = matcher.predict("mnrega payment stuck")
            found_fuzzy = [m['scheme_name'] for m in res_fuzzy['matches']]
            assert "Mahatma Gandhi National Rural Employment Guarantee Act" in found_fuzzy
        except ImportError:
            pytest.skip("RapidFuzz not installed")

    @pytest.mark.asyncio
    async def test_orchestrator_flow(self):
        """Test the orchestration flow with mocked models."""
        
        # Mock the heavier models to avoid loading 2GB+ files
        mock_audio = MagicMock()
        mock_audio.predict.return_value = {"text": "complaint text", "language": "en"}
        
        mock_extract = MagicMock()
        mock_extract.predict.return_value = {
            "entities": [], 
            "redacted_text": "complaint text",
            "pii_detected": []
        }
        
        # Patch the registry get_model to return mocks
        with patch.object(ModelRegistry, 'get_model') as mock_get:
            def side_effect(name):
                if name == "whisper": return mock_audio
                if name == "entity_extractor": return mock_extract
                if name == "scheme_matcher": return SchemeMatcher() # Lightweight enough
                return MagicMock()
            
            mock_get.side_effect = side_effect
            
            orchestrator = PipelineOrchestrator()
            result = await orchestrator.process_complaint_stream("dummy.mp3", {"trace_id": "123"})
            
            assert result["status"] == "processed"
            mock_audio.predict.assert_called_once()
            mock_extract.predict.assert_called_once()
