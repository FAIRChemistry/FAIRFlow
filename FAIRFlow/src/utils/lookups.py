SCENARIO_MAPPING = {
    "SelectiveOxidation": {
        "dir_name": "selective_oxidation",
        "scenario_nr": "1",
    },
    "FaradayEfficiency": {
        "dir_name": "faraday_efficiency",
        "scenario_nr": "2",
    },
}

NR_TO_SCENARIO_TYPE = {
    "1": "SelectiveOxidation",
    "2": "FaradayEfficiency",
}

def NR_TO_SCENARIO_CLS():
    from FAIRFlow.src.acquisition.scenario_specific.scenarios import SelectiveOxidation, FaradayEfficiency
    return {
        "1": SelectiveOxidation,
        "2": FaradayEfficiency,
    }