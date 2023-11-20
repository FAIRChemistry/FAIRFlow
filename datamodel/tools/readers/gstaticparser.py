import pandas as pd
import re

from pathlib import Path
from datamodel.core.measurement import Measurement


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
    potentiostatic_measurement = Measurement()
    key_list                   = [ "IINIT", "TINIT", "AREA" ]

    for key in key_list:
        potentiostatic_measurement.add_to_metadata( 
                                parameter = key,
                                value = float(metadata_df.loc[metadata_df['Parameter'] == key, 'Value'].values[0]) ,
                                data_type = float,
                                unit = re.search(r'\((.*?)\)', metadata_df.loc[metadata_df['Parameter'] == key, 'Description'].values[0]).group(1),
                                description = re.match(r'(.*?)\(', metadata_df.loc[metadata_df['Parameter'] == key, 'Description'].values[0]).group(1).strip()
    )
        
    return potentiostatic_measurement
