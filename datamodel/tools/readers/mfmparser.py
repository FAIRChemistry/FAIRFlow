import pandas as pd

from pathlib import Path
from datamodel_b07_tc.test.data import Data
from datamodel.core.measurement import Measurement


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
    ).dropna()

    # Extract important data
    mfm_measurement = Measurement()
    key_list        = [ "Date time", "Volumetric flow rate" ]

    for quantity in key_list:

        values = [ pd.to_datetime(timestamp, format="%d.%m.%Y ; %H:%M:%S").to_pydatetime()
                   for timestamp in experimental_data_df[quantity] ] if quantity == "Date time" \
                   else experimental_data_df[quantity].to_list()

        mfm_measurement.add_to_experimental_data( 
                                                quantity=quantity,
                                                values=values,
                                                unit=quantity_unit_dict[quantity]
        )
  
    return mfm_measurement
