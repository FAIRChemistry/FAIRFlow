import xml.etree.ElementTree as ET
from sdRDM import DataModel


def DEXPI2sdRDM(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    ID_list = pd.DataFrame(columns=["ID", "P&ID_name", "neighbors"])

    for equipment in root.findall("Equipment"):
        ID = equipment.get("ID")
        TagName = equipment.get("TagName")

    ID_list
    print("ID_list:", ID_list)

    return cls()
