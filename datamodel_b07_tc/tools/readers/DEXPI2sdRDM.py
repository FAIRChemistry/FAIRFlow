import xml.etree.ElementTree as ET
import pandas as pd
from datamodel_b07_tc.modified.plantsetup import PlantSetup
from sdRDM import DataModel
from pathlib import Path


def DEXPI2sdRDM(cls: PlantSetup, filepath: Path):
    tree = ET.parse(filepath)
    root = tree.getroot()

    dexpi_sdrdm_mapping = {
        "Gas cylinder": "GasCylinder",
        "Valve, three way ball type": "Valve",
    }

    equipment_ID_list = pd.DataFrame(columns=["ID", "P&ID_name", "class"])
    for i, equipment in enumerate(root.findall("Equipment")):
        ID = equipment.get("ID")
        TagName = equipment.get("TagName")
        for generic_attribute in equipment.findall(
            "GenericAttributes/GenericAttribute"
        ):
            if generic_attribute.get("Name") == "CLASS":
                C = generic_attribute.get("Value")
        equipment_ID_list.loc[i] = [ID, TagName, C]

    piping_component_ID_list = pd.DataFrame(
        columns=["ID", "P&ID_name", "class"]
    )
    for i, piping_component in enumerate(
        root.findall("PipingNetworkSystem//PipingComponent")
    ):
        ID = piping_component.get("ID")
        TagName = piping_component.get("TagName")
        for generic_attribute in piping_component.findall(
            "GenericAttributes/GenericAttribute"
        ):
            if generic_attribute.get("Name") == "CLASS":
                C = generic_attribute.get("Value")
        piping_component_ID_list.loc[i] = [ID, TagName, C]

    piping_network_segment_ID_list = pd.DataFrame(
        columns=["FromID", "ToID", "class"]
    )
    for i, PNS in enumerate(
        root.findall("PipingNetworkSystem/PipingNetworkSegment")
    ):
        for connection in PNS.findall("Connection"):
            FromID = connection.get("FromID")
            ToID = connection.get("ToID")
            for generic_attribute in connection.findall(
                "GenericAttributes/GenericAttribute"
            ):
                if generic_attribute.get("Name") == "CLASS":
                    C = generic_attribute.get("Value")
            piping_network_segment_ID_list.loc[i] = [FromID, ToID, C]

    equipment_list = []
    equipment_classes = equipment_ID_list["class"].to_list()
    # print("equipment_classes:", equipment_classes)
    for eq in equipment_classes:
        # print(eq)
        if eq in dexpi_sdrdm_mapping.keys():
            sdrdm_object_name = dexpi_sdrdm_mapping[eq]
            print(sdrdm_object_name)
            if hasattr(DataModel, sdrdm_object_name):
                # print("yes")
                # Get the subclass from the module
                sdrdm_object = getattr(DataModel, sdrdm_object_name)
                # Create an instance of the subclass
                instance = sdrdm_object()
                # print(instance)
                equipment_list.append(instance)

    # piping_network_system_list = DataModel.PipingNetworkSystem()

    plantsetup = cls(equipment=equipment_list)
    return plantsetup
