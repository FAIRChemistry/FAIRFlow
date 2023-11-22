import pandas as pd
import numpy as np
import Levenshtein

from pathlib import Path
from datamodel.core import Measurement
from datamodel.core import Quantity

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
