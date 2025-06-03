SCENARIO_REGISTRY = {}

def register_scenario(cls):
    from .registry import SCENARIO_REGISTRY
    SCENARIO_REGISTRY[cls.__name__] = cls
    return cls