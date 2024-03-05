import sdRDM

from typing import Optional, Union, List
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from datetime import datetime as Datetime
from sdRDM.base.datatypes import Unit
from .metadata import Metadata
from .measurementtype import MeasurementType
from .quantity import Quantity
from .data import Data
from .datatype import DataType
from .component import Component


@forge_signature
class Measurement(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@f4f90b698573ebe018bb7f96d10be4877e4643b3#Measurement"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    measurement_type: Optional[MeasurementType] = element(
        description="type of a measurement, e.g. potentiostatic or gas chromatography.",
        default=None,
        tag="measurement_type",
        json_schema_extra=dict(),
    )

    metadata: List[Metadata] = wrapped(
        "metadata",
        element(
            description="metadata of a measurement.",
            default_factory=ListPlus,
            tag="Metadata",
            json_schema_extra=dict(multiple=True),
        ),
    )

    experimental_data: List[Data] = wrapped(
        "experimental_data",
        element(
            description="experimental data of a measurement.",
            default_factory=ListPlus,
            tag="Data",
            json_schema_extra=dict(multiple=True),
        ),
    )

    source: Optional[Component] = element(
        description="measuring device the data stems from.",
        default_factory=Component,
        tag="source",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="f4f90b698573ebe018bb7f96d10be4877e4643b3"
    )

    def add_to_metadata(
        self,
        parameter: Optional[str] = None,
        value: Union[str, float, Datetime, None] = None,
        abbreviation: Optional[str] = None,
        data_type: Optional[DataType] = None,
        mode: Optional[str] = None,
        unit: Optional[Unit] = None,
        description: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Metadata:
        """
        This method adds an object of type 'Metadata' to attribute metadata

        Args:
            id (str): Unique identifier of the 'Metadata' object. Defaults to 'None'.
            parameter (): name of the parameter.. Defaults to None
            value (): value of the parameter.. Defaults to None
            abbreviation (): abbreviation for the parameter.. Defaults to None
            data_type (): type of the parameter.. Defaults to None
            mode (): mode of the parameter. e.g., on and off.. Defaults to None
            unit (): unit of the parameter.. Defaults to None
            description (): description of the parameter.. Defaults to None
        """
        params = {
            "parameter": parameter,
            "value": value,
            "abbreviation": abbreviation,
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
        unit: Optional[Unit] = None,
        id: Optional[str] = None,
    ) -> Data:
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
