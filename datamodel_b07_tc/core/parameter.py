import sdRDM

from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator

from astropy.units import UnitBase


@forge_signature
class Parameter(sdRDM.DataModel):

    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("parameterINDEX"),
        xml="@id",
    )

    value: Optional[float] = Field(
        default=None,
        description="values.",
    )

    unit: Optional[UnitBase] = Field(
        default=None,
        description="unit of the values.",
    )
<<<<<<< Updated upstream

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8f3ba22c83330e0532dcb7cdb12b205c1f881980"
    )
=======
>>>>>>> Stashed changes
