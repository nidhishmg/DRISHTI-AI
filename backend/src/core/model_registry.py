from typing import Any, Dict, Type
from ..config.settings import get_settings

settings = get_settings()

class ModelRegistry:
    _registry: Dict[str, Type] = {}
    _instances: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a model class."""
        def decorator(model_class: Type):
            cls._registry[name] = model_class
            return model_class
        return decorator

    @classmethod
    def get_model(cls, name: str, **kwargs) -> Any:
        """
        Get an instance of a registered model.
        Lazy loads the model on first request.
        """
        if name not in cls._registry:
            raise ValueError(f"Model '{name}' not found in registry.")
        
        # Singleton-ish pattern for heavy models
        # For stateful models, we might want new instances
        if name not in cls._instances:
            print(f"Loading model: {name}")
            cls._instances[name] = cls._registry[name](**kwargs)
            
        return cls._instances[name]

    @classmethod
    def list_models(cls):
        return list(cls._registry.keys())

# Example usage interface
class AbstractModel:
    def predict(self, input_data: Any) -> Any:
        raise NotImplementedError
