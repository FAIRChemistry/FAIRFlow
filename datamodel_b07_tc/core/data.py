import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .unit import Unit


@forge_signature
class Data(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("dataINDEX"),
        xml="@id",
    )

    values: List[float] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="values.",
    )

    unit: Optional[Unit] = Field(
        default=None,
        description="unit of the values.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="9b8bf8969a4a0a93beb9de6b91cb3dd024a74d1d"
    )
