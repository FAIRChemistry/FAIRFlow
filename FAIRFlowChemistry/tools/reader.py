import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import Levenshtein
import re
from typing import DefaultDict
from pathlib import Path
from datetime import datetime
from FAIRFlowChemistry.core import DataType
from FAIRFlowChemistry.core import Quantity
from FAIRFlowChemistry.core import Measurement
from FAIRFlowChemistry.core import PlantSetup
from FAIRFlowChemistry.core import Component
from FAIRFlowChemistry.core import ComponentType


def gc_parser(metadata_path: Path, experimental_data_path: Path):
    """
    Function that reads in a file from a gas chromotography. Important information that is extracted is the
    injection time, the retention times, as well as the peak areas.

    Args:
        metadata_path (Path): Path to metadata csv file
        experimental_data_path (Path): Path to measurement csv file
    """

    ## Read in the metadata file to correctly map measurement results ##

    # Extract important data
    gc_measurement = Measurement(measurement_type="GC measurement")
    key_list = ["Injection Date"]

    metadata_df = pd.read_csv(
        metadata_path,
        sep=",",
        names=[
            "Parameter",
            "Value",
            "Description",
        ],
        engine="python",
        encoding="utf-16_le",
    )

    # Add important metadata to the measurement

    for key in key_list:

        gc_measurement.add_to_metadata(
            parameter=key,
            value=(
                datetime.strptime(
                    metadata_df.loc[metadata_df["Parameter"] == key, "Value"].values[0],
                    "%d-%b-%y, %H:%M:%S",
                )
                if key == "Injection Date"
                else metadata_df.loc[metadata_df["Parameter"] == key, "Value"].values[0]
            ),
            data_type=(
                DataType.DATETIME.value
                if key == "Injection Date"
                else DataType.STRING.value
            ),
            description=(
                "Injection date of the GC measurement"
                if key == "Injection Date"
                else None
            ),
        )

    # Filter out the header description of the measurement csv file (contaning description and units)
    filtered_columns = metadata_df[metadata_df["Parameter"].str.match(r"^Column \d+$")]
    quantity_unit_dict = {
        row["Value"].strip(): (
            row["Description"]
            if not pd.isna(row["Description"]) and bool(row["Description"].split())
            else ""
        )
        for _, row in filtered_columns.iterrows()
    }

    ## Read in the measurement file  ##

    experimental_data_df = pd.read_csv(
        experimental_data_path,
        sep=",",
        names=list(quantity_unit_dict.keys()),
        engine="python",
        encoding="utf-16_le",
    )

    key_list = ["Retention Time", "Peak Type", "Area", "Area   %"]

    for key in key_list:

        quantity = list(Quantity)[
            np.argmax(
                [
                    Levenshtein.ratio(
                        quantity_type.value,
                        key.replace("%", "percentage") if "%" in key else key,
                    )
                    for quantity_type in Quantity
                ]
            )
        ].value
        values = (
            np.round(experimental_data_df[key], 4).to_list()
            if key != "Peak Type"
            else experimental_data_df[key].to_list()
        )

        gc_measurement.add_to_experimental_data(
            quantity=quantity, values=values, unit=quantity_unit_dict[key]
        )

    return gc_measurement


def gstatic_parser(metadata_path: Path):
    """
    Function that reads in a file from a potentiostat/galvanostat. Important information that is extracted is the
    inital current and time, as well as the electrode surface area

    Args:
        metadata_path (Path): Path to metadata path of potentiostat/galvanostat

    Returns:
        Measurement: Measurement data object, containing the important meta data (in this case the electrode surface area and the initial current.)
    """

    metadata_df = pd.read_csv(
        metadata_path,
        sep="\t",
        names=[
            "Parameter",
            "Type",
            "Value",
            "Description",
        ],
        engine="python",
        encoding="utf-8",
        skiprows=range(0, 7),
        nrows=(54 - 8 + 1),
    )

    # Extract important meta data
    echem_measurement = Measurement(measurement_type="Galvanostatic measurement")
    key_list = ["IINIT", "AREA"]
    Quantity_list = {
        "IINIT": Quantity.CURRENT.value,
        "AREA": Quantity.SURFACEAREA.value,
    }

    for key in key_list:

        quantity = Quantity_list[key]
        value = float(
            metadata_df.loc[metadata_df["Parameter"] == key, "Value"].values[0]
        )

        echem_measurement.add_to_metadata(
            parameter=quantity,
            value=value,
            data_type=DataType.FLOAT.value,
            unit=re.search(
                r"\((.*?)\)",
                metadata_df.loc[metadata_df["Parameter"] == key, "Description"].values[
                    0
                ],
            ).group(1),
            description=re.match(
                r"(.*?)\(",
                metadata_df.loc[metadata_df["Parameter"] == key, "Description"].values[
                    0
                ],
            )
            .group(1)
            .strip(),
        )

    return echem_measurement


def mfm_parser(experimental_data_path: Path):
    """
    Function that reads in a file from a mass flow meter. Important information that is extracted is measurement time and the flowrate

    Args:
        experimental_data_path (Path): Path to csv output of mass flow meter
    """

    quantity_unit_dict = {
        "Date time": "",
        "Time": "s",
        "Signal": "",
        "Volumetric flow rate": "ml / s",
    }

    experimental_data_df = pd.read_csv(
        experimental_data_path,
        sep=",",
        names=[name for name in quantity_unit_dict.keys()],
        engine="python",
        encoding="utf-8",
        skiprows=1,
    )
    experimental_data_df = experimental_data_df.dropna()

    # Extract important data
    mfm_measurement = Measurement(measurement_type="MFM measurement")
    key_list = ["Date time", "Volumetric flow rate"]

    for key in key_list:

        quantity = list(Quantity)[
            np.argmax(
                [
                    Levenshtein.ratio(
                        quantity_type.value,
                        key.replace("%", "percentage") if "%" in key else key,
                    )
                    for quantity_type in Quantity
                ]
            )
        ].value

        values = (
            [
                pd.to_datetime(timestamp, format="%d.%m.%Y ; %H:%M:%S").to_pydatetime()
                for timestamp in experimental_data_df[key]
            ]
            if key == "Date time"
            else np.round(experimental_data_df[key] / 60, 6).to_list()
        )

        mfm_measurement.add_to_experimental_data(
            quantity=quantity, values=values, unit=quantity_unit_dict[key]
        )

    return mfm_measurement


def DEXPI2sdRDM(filepath: Path):
    tree = ET.parse(filepath)
    root = tree.getroot()

    def build_component(component, component_type: ComponentType):
        return Component(
            component_type=component_type,
            component_id=component.get("ID"),
            component_class=component.get("ComponentClass"),
            component_class_uri=component.get("ComponentClassURI"),
        )

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

    for component in components:
        print(component.component_id, component.connections)
    return PlantSetup(components=components)
