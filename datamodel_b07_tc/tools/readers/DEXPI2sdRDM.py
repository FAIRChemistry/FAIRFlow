import xml.etree.ElementTree as ET
import pandas as pd
from datamodel_b07_tc.core.plantsetup import PlantSetup
from sdRDM import DataModel
from pathlib import Path


def DEXPI2sdRDM(cls: PlantSetup, filepath: Path):
    tree = ET.parse(filepath)
    root = tree.getroot()
    equipment_ID_list = pd.DataFrame(columns=["ID", "P&ID_name", "class"])

    for i, equipment in enumerate(root.findall("Equipment")):
        ID = equipment.get("ID")
        TagName = equipment.get("TagName")
        print(f"equipment:{ID}, {TagName}")
        for generic_attribute in equipment.findall(
            "GenericAttributes/GenericAttribute"
        ):
            if generic_attribute.get("Name") == "CLASS":
                C = generic_attribute.get("Value")
        equipment_ID_list.iloc[i] = [ID, TagName, C]

    piping_component_ID_list = pd.DataFrame(
        columns=["ID", "P&ID_name", "class"]
    )
    for piping_component in root.findall(
        "PipingNetworkSystem//PipingComponent"
    ):
        ID = piping_component.get("ID")
        TagName = piping_component.get("TagName")
        print(f"piping_component:{ID}, {TagName}")
        for generic_attribute in piping_component.findall(
            "GenericAttributes/GenericAttribute"
        ):
            if generic_attribute.get("Name") == "CLASS":
                C = generic_attribute.get("Value")
                print(f"class:{C}")
        piping_component_ID_list.iloc[i] = [ID, TagName, C]

    piping_network_segment_ID_list = pd.DataFrame(
        columns=["FromID", "ToID", "class"]
    )
    for i, PNS in enumerate(
        root.findall("PipingNetworkSystem/PipingNetworkSegment")
    ):
        for connection in PNS.findall("Connection"):
            FromID = connection.get("FromID")
            ToID = connection.get("ToID")
            print(f"connection:{FromID}, {ToID}")
            for generic_attribute in connection.findall(
                "GenericAttributes/GenericAttribute"
            ):
                if generic_attribute.get("Name") == "CLASS":
                    C = generic_attribute.get("Value")
                    print(f"class:{C}")
            piping_component_ID_list.iloc[i] = [FromID, ToID, C]

    # ID_list
    # print(f"ID_list:{ID_list}")
    piping_network_system_list = []
    plantsetup = cls(
        equipment=equipment_list,
        piping_network_system=piping_network_system_list,
    )
    return
