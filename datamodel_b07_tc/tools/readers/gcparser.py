import pandas as pd
from pathlib import Path

from datamodel_b07_tc.core.measurement import Measurement
from datamodel_b07_tc.core.data import Data
from datamodel_b07_tc.core.metadata import Metadata


def gc_parser(
    cls: Measurement, metadata_path: Path, experimental_data_path: Path
):
    def _extract_metadata(metadata_path: Path):
        """Extract only data block as a `pandas.DataFrame`.
        Args:
            filestem (str): Name of the file (only stem) of which the data is to be extracted.
        Returns:
            pandas.DataFrame: DataFrame containing only the data from the file.
        """
        metadata_df = pd.read_csv(
            metadata_path,
            sep=",",
            names=[
                "parameter",
                "value",
                "description",
            ],
            engine="python",
            encoding="utf-16_le",
        )
        metadata_df.dropna(how="all", inplace=True)
        records = [
            row.dropna().to_dict() for index, row in metadata_df.iterrows()
        ]
        metadata_list = []
        for record in records:
            metadata_list.append(Metadata(**record))
        return metadata_list, metadata_df

    def _extract_experimental_data(experimental_data_path: Path):
        """Extract only data block as a `pandas.DataFrame`.
        Args:
            experimental_data_path (Path): path to the file from which the experimental data are to be extracted.
        Returns:
            pandas.DataFrame: DataFrame containing the experimental data from the file read in.
        """
        quantity_unit_dict = {
            "Peak number": None,
            "Retention time": "s",
            "Signal": None,
            "Peak type": None,
            "Peak area": None,
            "Peak height": None,
            "Peak area percentage": "%",
        }
        experimental_data_df = pd.read_csv(
            experimental_data_path,
            sep=",",
            names=[name for name in quantity_unit_dict.keys()],
            engine="python",
            encoding="utf-16_le",
        )
        experimental_data_list = []
        for quantity, unit in quantity_unit_dict.items():
            experimental_data_list.append(
                Data(
                    quantity=quantity,
                    values=experimental_data_df[quantity].to_list(),
                    unit=unit,
                )
            )
        return experimental_data_list, experimental_data_df

    experimental_data_list, experimental_data_df = _extract_experimental_data(
        experimental_data_path=experimental_data_path
    )
    metadata_list, metadata_df = _extract_metadata(metadata_path=metadata_path)
    measurement = cls(
        metadata=metadata_list,
        experimental_data=experimental_data_list,
        measurement_type="GC measurement",
    )
    return metadata_df, experimental_data_df, measurement
