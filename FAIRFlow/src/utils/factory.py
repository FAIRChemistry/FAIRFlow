import importlib
from FAIRFlow.src.utils.registry import SCENARIO_REGISTRY

import logging

logger = logging.getLogger(__name__)

def import_scenario_module(scenario_name: str, stage: str):
    """Import a scenario module by name, e.g., 'faraday_efficiency'."""
    module_path = f"FAIRFlow.src.scenarios.{scenario_name}.{stage}"
    try:
        scenario_module = importlib.import_module(module_path)
    except ImportError as e:
        logger.error(f"Failed to import scenario module '{module_path}': {e}")
        raise ImportError(f"Could not import scenario module '{module_path}'. Ensure it exists and is correctly named.")
    logger.info(f"Succesfully imported scenario module: {module_path}")
    return scenario_module

def create_scenario(scenario_name: str, stage: str, **kwargs):
    """Creates a scenario instance by name, assuming convention-based mapping."""
    # Import the module to trigger registration
    scenario_module = import_scenario_module(scenario_name, stage)

    # Convert 'faraday_efficiency' to 'FaradayEfficiency'
    # class_name = snake_to_pascal(scenario_name)

    # Lookup class in registry

    # Here we need to instantiate the class
    cls = getattr(scenario_module, snake_to_pascal(scenario_name))


    # cls = SCENARIO_REGISTRY.get(scenario_name)
    # if cls is None:
    #     logger.error(f"Scenario class '{snake_to_pascal(scenario_name)}' not found in registry.")
    #     raise ValueError(f"Scenario class '{snake_to_pascal(scenario_name)}' not found in registry.")
    return cls(**kwargs)

def snake_to_pascal(s: str) -> str:
    return ''.join(word.capitalize() for word in s.split('_'))