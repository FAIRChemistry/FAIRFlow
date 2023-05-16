import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .datatype import DataType
from .metadata import Metadata
from .unit import Unit
from .listofmeasurements import ListOfMeasurements
from .data import Data


@forge_signature
class Measurement(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("measurementINDEX"),
        xml="@id",
    )

    experimental_data: Optional[Data] = Field(
        default=None,
        description="experimental data of a measurement.",
    )

    metadata: List[Metadata] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="metadata of a measurement.",
    )

    list_of_measurements: Optional[ListOfMeasurements] = Field(
        default=None,
        description=(
            "list of measurements, that do not need any further quantities explanation."
            " E.g., only metadata are of interest."
        ),
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="6674aa21047a54f5f8939308c82f3e9ea953c401"
    )

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
