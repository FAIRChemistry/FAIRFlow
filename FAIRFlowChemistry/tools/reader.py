import pandas as pd
import numpy as np
import Levenshtein
import re

from pathlib import Path
from datetime import datetime
from FAIRFlowChemistry.core import DataType
from FAIRFlowChemistry.core import Quantity
from FAIRFlowChemistry.core import Measurement


def gc_parser( metadata_path: Path, experimental_data_path: Path ):
    """
    Function that reads in a file from a gas chromotography. Important information that is extracted is the 
    injection time, the retention times, as well as the peak areas.

    Args:
        metadata_path (Path): Path to metadata csv file
        experimental_data_path (Path): Path to measurement csv file
    """

    ## Read in the metadata file to correctly map measurement results ##

    # Extract important data
    gc_measurement = Measurement( measurement_type = "GC measurement" )
    key_list       = [ "Injection Date" ]

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
        
        gc_measurement.add_to_metadata( parameter = key,
                                        value = datetime.strptime( metadata_df.loc[metadata_df['Parameter'] == key, 'Value'].values[0], "%d-%b-%y, %H:%M:%S" ) if key == "Injection Date" \
                                                                   else metadata_df.loc[metadata_df['Parameter'] == key, 'Value'].values[0],
                                        data_type = DataType.DATETIME.value if key == "Injection Date" else DataType.STRING.value,
                                        description = "Injection date of the GC measurement"  if key == "Injection Date" else None
                                       )

    # Filter out the header description of the measurement csv file (contaning description and units)
    filtered_columns   = metadata_df[metadata_df['Parameter'].str.match(r'^Column \d+$')]
    quantity_unit_dict = { row["Value"].strip(): row["Description"] if not pd.isna(row["Description"]) and bool(row["Description"].split()) else None for _, row in filtered_columns.iterrows()}


    ## Read in the measurement file  ##

    experimental_data_df = pd.read_csv(
            experimental_data_path,
            sep=",",
            names=list( quantity_unit_dict.keys() ),
            engine="python",
            encoding="utf-16_le",
        )
    
    key_list     = [ "Retention Time", "Peak Type", "Area", "Area   %" ]

    for key in key_list:
        
        quantity = list(Quantity)[ np.argmax([ Levenshtein.ratio(quantity_type.value, key.replace("%","percentage") if "%" in key else key ) for quantity_type in Quantity ]) ].value
        values   = np.round( experimental_data_df[key], 4 ).to_list() if key != "Peak Type" else experimental_data_df[key].to_list()

        gc_measurement.add_to_experimental_data( 
                                                quantity = quantity,
                                                values = values,
                                                unit = quantity_unit_dict[key]
        )

    return gc_measurement


def gstatic_parser(metadata_path: Path):
    """
    Function that reads in a file from a potentiostat. Important information that is extracted is the 
    inital current and time, as well as the electrode surface area

    Args:
        metadata_path (Path): Path to metadata path of potentiostat

    Returns:
        _type_: _description_
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
        skiprows=[
            *[i for i in range(0, 7)],
            *[j for j in range(55, 3658)],
        ],
    )

    # Extract important meta data
    potentiostatic_measurement = Measurement( measurement_type = "Potentiostatic measurement")
    key_list                   = [ "IINIT", "AREA" ]
    Quantity_list              = {"IINIT": Quantity.CURRENT.value, "AREA": Quantity.SURFACEAREA.value}

    for key in key_list:

        quantity = Quantity_list[key]
        value    = float(metadata_df.loc[metadata_df['Parameter'] == key, 'Value'].values[0]) 
        
        potentiostatic_measurement.add_to_metadata( 
                                parameter = quantity,
                                value = value ,
                                data_type = DataType.FLOAT.value,
                                unit = re.search(r'\((.*?)\)', metadata_df.loc[metadata_df['Parameter'] == key, 'Description'].values[0]).group(1),
                                description = re.match(r'(.*?)\(', metadata_df.loc[metadata_df['Parameter'] == key, 'Description'].values[0]).group(1).strip()
    )
        
    return potentiostatic_measurement


def mfm_parser(experimental_data_path: Path):
    """
    Function that reads in a file from a mass flow meter. Important information that is extracted is measurement time and the flowrate

    Args:
        experimental_data_path (Path): Path to csv output of mass flow meter
    """

    quantity_unit_dict = {
        "Date time": None,
        "Time": "s",
        "Signal": None,
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
    mfm_measurement = Measurement( measurement_type = "MFM measurement" )
    key_list        = [ "Date time", "Volumetric flow rate" ]

    for key in key_list:

        quantity = list(Quantity)[ np.argmax([ Levenshtein.ratio(quantity_type.value, key.replace("%","percentage") if "%" in key else key ) for quantity_type in Quantity ]) ].value

        values = [ pd.to_datetime(timestamp, format="%d.%m.%Y ; %H:%M:%S").to_pydatetime()
                   for timestamp in experimental_data_df[key] ] if key == "Date time" \
                   else np.round( experimental_data_df[key] / 60, 6 ).to_list()

        mfm_measurement.add_to_experimental_data( 
                                                quantity = quantity,
                                                values = values,
                                                unit = quantity_unit_dict[key]
        )
  
    return mfm_measurement
