import sdRDM

from typing import Optional, Union, List, Dict
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.base.datatypes import Unit
from sdRDM.tools.utils import elem2dict
from datetime import datetime as Datetime
from .datatype import DataType
from .measurementtype import MeasurementType
from .quantity import Quantity
from .data import Data
from .component import Component
from .metadata import Metadata


@forge_signature
class Measurement(sdRDM.DataModel, search_mode="unordered"):
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

    metadata: List[Metadata] = element(
        description="metadata of a measurement.",
        default_factory=ListPlus,
        tag="metadata",
        json_schema_extra=dict(multiple=True),
    )

    experimental_data: List[Data] = element(
        description="experimental data of a measurement.",
        default_factory=ListPlus,
        tag="experimental_data",
        json_schema_extra=dict(multiple=True),
    )

    source: Optional[Component] = element(
        description="measuring device the data stems from.",
        default_factory=Component,
        tag="source",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlow"
    )
    _commit: Optional[str] = PrivateAttr(
        default="cb79cadf6115feb0ae23be27aec6885df4d70bc8"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self

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
        **kwargs
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
        **kwargs
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
