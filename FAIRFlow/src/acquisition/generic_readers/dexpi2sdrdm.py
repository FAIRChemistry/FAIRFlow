
import xml.etree.ElementTree as ET
from typing import DefaultDict
from pathlib import Path

from FAIRFlow.core import PlantSetup
from FAIRFlow.core import Component
from FAIRFlow.core import ComponentType

def build_component(component, component_type: ComponentType):
        return Component(
            component_type=component_type,
            component_id=component.get("ID"),
            component_class=component.get("ComponentClass"),
            component_class_uri=component.get("ComponentClassURI"),
        )

def DEXPI2sdRDM(filepath: Path|str ):
    tree = ET.parse(filepath)
    root = tree.getroot()

    components = []
    nozzles = DefaultDict(list)
    for eq in root.findall("Equipment"):
        components.append(build_component(eq, ComponentType.EQUIPMENT))
        for nozzle in eq.findall("Nozzle"):
            nozzles[eq.get("ID")].append(nozzle.get("ID"))

    connections = []
    piping_network_system = root.findall("PipingNetworkSystem")
    for pns in piping_network_system:
        for piping_network_segment in pns.findall("PipingNetworkSegment"):
            connection = [
                piping_network_segment.find("Connection").get("FromID"),
                piping_network_segment.find("Connection").get("ToID"),
            ]
            connections.append(connection)
            for piping_component in piping_network_segment.findall("PipingComponent"):
                components.append(
                    build_component(piping_component, ComponentType.PIPINGCOMPONENT)
                )

    for connection in connections:
        for connection_point in connection:
            if "Nozzle" in connection_point:
                for eq, nozzle in nozzles.items():
                    for n in nozzle:
                        if n in connection_point:
                            connection[connection.index(connection_point)] = eq
    for component in components:
        for connection in connections:
            if component.component_id in connection:
                component.connections.extend(connection)
                component.connections.remove(component.component_id)

    return PlantSetup(components=components)