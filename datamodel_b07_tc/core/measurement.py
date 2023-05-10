import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .metadata import Metadata
from .data import Data
from .listofmeasurements import ListOfMeasurements


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

    metadata: Optional[Metadata] = Field(
        default=None,
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
        default="087d97eb5882e9a8535a8faaabe6baaea7a85f78"
    )
