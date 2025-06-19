import importlib
package_name = "numpy"  # or any package name determined at runtime
module = importlib.import_module(package_name)

# Now you can use it like:
print(module.__version__)
array = module.array([1, 2, 3])

SCENARIO_MAPPING = {
    "selective_oxidation": "SelectiveOxidation",
    "faraday_efficiency": "FaradayEfficiency"  
}

# def NR_TO_SCENARIO_CLS(scenario_name):

#     from FAIRFlow.src.acquisition.scenario_specific.scenarios import SelectiveOxidation, FaradayEfficiency # make the import scenario dependent
#     return {
#         "1": SelectiveOxidation,
#         "2": FaradayEfficiency,
#     }