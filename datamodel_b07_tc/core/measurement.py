import sdRDM

from typing import Optional, Union, List
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from astropy.units import UnitBase
from datetime import datetime as Datetime
from .metadata import Metadata
from .quantity import Quantity
from .measurementtype import MeasurementType
from .data import Data
from .datatype import DataType


@forge_signature
class Measurement(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("measurementINDEX"),
        xml="@id",
    )

    measurement_type: Optional[MeasurementType] = Field(
        default=None,
        description="type of a measurement, e.g. potentiostatic or gas chromatography.",
    )

    metadata: List[Metadata] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="metadata of a measurement.",
    )

    experimental_data: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="experimental data of a measurement.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8b7eacb04935747b31b603de5a7dd9dc8a26d3f7"
    )

    def add_to_metadata(
        self,
        parameter: Optional[str] = None,
        value: Union[str, float, Datetime, None] = None,
        abbreviation: Optional[str] = None,
        type: Optional[str] = None,
        data_type: Optional[DataType] = None,
        mode: Optional[str] = None,
        unit: Optional[UnitBase] = None,
        description: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Metadata' to attribute metadata

        Args:
            id (str): Unique identifier of the 'Metadata' object. Defaults to 'None'.
            parameter (): Name of the parameter.. Defaults to None
            value (): value of the parameter.. Defaults to None
            abbreviation (): abbreviation for the parameter.. Defaults to None
            type (): type of the parameter, e.g. a quantity, a toggle, a label.. Defaults to None
            data_type (): type of the data, e.g. string, float, bool.. Defaults to None
            mode (): mode of the parameter. E.g., on and off.. Defaults to None
            unit (): unit of the parameter.. Defaults to None
            description (): description of the parameter.. Defaults to None
        """
        params = {
            "parameter": parameter,
            "value": value,
            "abbreviation": abbreviation,
            "type": type,
            "data_type": data_type,
            "mode": mode,
            "unit": unit,
            "description": description,
        }
        if id is not None:
            params["id"] = id
        self.metadata.append(Metadata(**params))
        return self.metadata[-1]

    def add_to_experimental_data(
        self,
        quantity: Optional[Quantity] = None,
        values: List[Union[float, str, Datetime]] = ListPlus(),
        unit: Optional[UnitBase] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute experimental_data

        Args:
            id (str): Unique identifier of the 'Data' object. Defaults to 'None'.
            quantity (): quantity of a value.. Defaults to None
            values (): values.. Defaults to ListPlus()
            unit (): unit of the values.. Defaults to None
        """
        params = {"quantity": quantity, "values": values, "unit": unit}
        if id is not None:
            params["id"] = id
        self.experimental_data.append(Data(**params))
        return self.experimental_data[-1]
