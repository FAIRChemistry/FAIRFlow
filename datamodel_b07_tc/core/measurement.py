import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .listofmeasurements import ListOfMeasurements
from .metadata import Metadata
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
        default="e243332d34aace2b933a1385915f3b8871a64409"
    )
