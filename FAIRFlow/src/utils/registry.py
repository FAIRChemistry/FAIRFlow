"""
A registry for scenario classes, allowing dynamic import and instantiation.
"""
SCENARIO_REGISTRY = {}

import logging

logger = logging.getLogger(__name__)

def register_scenario(cls):
    """
    Decorator to register a scenario class in the SCENARIO_REGISTRY.
    The class name is converted from PascalCase to snake_case for the registry key.
    """
    from .registry import SCENARIO_REGISTRY
    if not hasattr(cls, '__name__'):
        logger.error(f"Class {cls} does not have a __name__ attribute.")
        raise ValueError("Class must have a __name__ attribute to be registered.")
    SCENARIO_REGISTRY[pascal_to_snake(cls)] = cls
    return cls

def pascal_to_snake(cls):
    """Convert a PascalCase string to snake_case."""
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
