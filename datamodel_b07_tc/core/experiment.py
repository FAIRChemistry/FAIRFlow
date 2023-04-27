import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .calculation import Calculation
from .plantsetup import PlantSetup


@forge_signature
class Experiment(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = Field(
        default=None,
    )

    calculations: Optional[Calculation] = Field(
        default=None,
        description=(
            "all the calculations that are done within the scope of one experiment."
        ),
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="15c1628100dadc5d2ce53ff72a02f247fae78748"
    )
