import pandas as pd
import numpy as np
import Levenshtein

from pathlib import Path
from datetime import datetime
from datamodel.core import DataType
from datamodel.core import Quantity
from datamodel.core import Measurement


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
    
    key_list     = [ "Retention Time", "Area", "Area   %" ]

    for key in key_list:
        
        quantity = list(Quantity)[ np.argmax([ Levenshtein.ratio(quantity_type.value, key.replace("%","percentage") if "%" in key else key ) for quantity_type in Quantity ]) ].value

        gc_measurement.add_to_experimental_data( 
                                                quantity = quantity,
                                                values = np.round( experimental_data_df[key], 4 ).to_list(),
                                                unit = quantity_unit_dict[key]
        )

    return gc_measurement
