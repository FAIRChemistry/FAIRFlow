
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


from .metadata import Metadata
from .device import Device
from .measurement import Measurement


@forge_signature
class Potentiostat(Device):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("potentiostatINDEX"),
        xml="@id",
    )

    measurement: Optional[Measurement] = Field(
        default=None,
        description="Measuring Data.",
    )

    metadata: Optional[Metadata] = Field(
        default=None,
        description="Metadata of the Potentiostat.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="a92cd7e4d0326d4eafac9c6c2b73ea481e0b61b8"
    )
