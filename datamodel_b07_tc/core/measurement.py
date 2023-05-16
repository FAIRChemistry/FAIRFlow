import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from datetime import datetime

from .measurementtype import MeasurementType
from .data import Data
from .quantity import Quantity
from .unit import Unit
from .datatype import DataType
from .metadata import Metadata


@forge_signature
class Measurement(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("measurementINDEX"),
        xml="@id",
    )

    experimental_data: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="experimental data of a measurement.",
    )

    metadata: List[Metadata] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="metadata of a measurement.",
    )

    measurement_type: Optional[MeasurementType] = Field(
        default=None,
        description="type of a measurement, e.g. potentiostatic or gas chromatography.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="89bafe6cb4730e9ef596157d40746f132b6dd2f0"
    )

    def add_to_experimental_data(
        self,
        quantity: Optional[Quantity] = None,
        values: Union[float, str, datetime, None] = None,
        unit: Optional[Unit] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute experimental_data

        Args:
            id (str): Unique identifier of the 'Data' object. Defaults to 'None'.
            quantity (): quantity of a value.. Defaults to None
            values (): values.. Defaults to None
            unit (): unit of the values.. Defaults to None
        """

        params = {
            "quantity": quantity,
            "values": values,
            "unit": unit,
        }

        if id is not None:
            params["id"] = id

        self.experimental_data.append(Data(**params))

    def add_to_metadata(
        self,
        parameter: Optional[str] = None,
        abbreviation: Optional[str] = None,
        data_type: Optional[DataType] = None,
        mode: Optional[str] = None,
        size: Optional[float] = None,
        unit: Optional[Unit] = None,
        description: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Metadata' to attribute metadata

        Args:
            id (str): Unique identifier of the 'Metadata' object. Defaults to 'None'.
            parameter (): Name of the parameter.. Defaults to None
            abbreviation (): abbreviation for the parameter.. Defaults to None
            data_type (): type of the parameter.. Defaults to None
            mode (): mode of the parameter. E.g., on and off.. Defaults to None
            size (): size of the parameter.. Defaults to None
            unit (): unit of the parameter.. Defaults to None
            description (): description of the parameter.. Defaults to None
        """

        params = {
            "parameter": parameter,
            "abbreviation": abbreviation,
            "data_type": data_type,
            "mode": mode,
            "size": size,
            "unit": unit,
            "description": description,
        }

        if id is not None:
            params["id"] = id

        self.metadata.append(Metadata(**params))
