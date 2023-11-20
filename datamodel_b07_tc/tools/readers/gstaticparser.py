import pandas as pd

from pathlib import Path
from pydantic import BaseModel
from datamodel_b07_tc.core.metadata import Metadata
from datamodel_b07_tc.core.measurement import Measurement


def gstatic_parser(cls: Measurement, metadata_path: Path):
    """ """
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
    metadata_list = []
    for index in metadata_df.index:
        metadata_list.append(
            Metadata(
                parameter=metadata_df["Parameter"][index],
                type=metadata_df["Type"][index],
                value=metadata_df["Value"][index],
                description=metadata_df["Description"][index],
            )
        )
    potentiostatic_measurement = cls(
        measurement_type="Potentiostatic measurement", metadata=metadata_list
    )
    return metadata_df, potentiostatic_measurement
