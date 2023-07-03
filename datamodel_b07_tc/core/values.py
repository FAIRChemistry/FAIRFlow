import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Values(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("valuesINDEX"),
        xml="@id",
    )

    floats: List[float] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="values of data type float.",
    )

    strings: List[str] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="values of data type string.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="1868255755c897190362907bed191a98450f9d11"
    )
