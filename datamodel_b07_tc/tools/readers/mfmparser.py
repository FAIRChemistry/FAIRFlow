import pandas as pd

from pathlib import Path
from datamodel_b07_tc.test.data import Data
from datamodel_b07_tc.test.measurement import Measurement


def mfm_parser(cls: Measurement, experimental_data_path: Path):
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
    experimental_data_df["Date time"] = pd.to_datetime(
        experimental_data_df["Date time"], format="%d.%m.%Y ; %H:%M:%S"
    )
    experimental_data_list = []
    for quantity, unit in quantity_unit_dict.items():
        if quantity == "Date time":
            values = [
                timestamp.to_pydatetime()
                for timestamp in experimental_data_df[quantity]
            ]
        else:
            values = experimental_data_df[quantity].to_list()
        experimental_data_list.append(
            Data(quantity=quantity, values=values, unit=unit)
        )
    measurement = cls(
        measurement_type="MFM measurement",
        experimental_data=experimental_data_list,
    )
    return experimental_data_df, measurement
