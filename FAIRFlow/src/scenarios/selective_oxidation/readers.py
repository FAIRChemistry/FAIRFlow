import pandas as pd
from pathlib import Path
from datetime import datetime
from FAIRFlow.core import DataType
from FAIRFlow.core import Quantity
from FAIRFlow.core import Measurement


def gc_parser_selective_oxidation(data_path: Path):
    """
    Function that reads in a file from the gas chromotograph for the
    selective oxidation scenario. 

    Args:
        data_path (Path): Path to measurement output file
    """
    # print(data_path)
    column_names = [
        'Date',
        'Time',
        'Sample_Id',
        'Filename',
        'Method_name',
        'Username',
        'Vial',
        'Volume',
        'Autosampler_program',
        'MSA',
        'o-Xylol',
        'o-Toluylaldehyd',
        'o-Toluylsaeure',
        'PSA',
        'Phthalid',
        'unknown 13.64',
        'unknown 13.72',
    ]
    data_df = pd.read_csv(
        data_path,
        sep="\t",
        names=column_names,
        engine="python",
        encoding='cp1252',
        skiprows=3

    )
    datetime = pd.to_datetime(data_df.Date + ' ' + data_df.Time)
    data_df['datetime'] = datetime
    data_df = data_df.drop(columns=[
        'Date',
        'Time',
        'Username',
        'Volume',
        'Autosampler_program',
    ])
    cols = data_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_df = data_df[cols]
    return data_df