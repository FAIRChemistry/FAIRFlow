
from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator
<<<<<<< HEAD
from .measurement import Measurement
from .metadata import Metadata
=======


from .metadata import Metadata
from .measurement import Measurement
>>>>>>> 5e18871 (updated core)
from .device import Device


@forge_signature
class Potentiostat(Device):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("potentiostatINDEX"),
        xml="@id",
    )

    measurement: Optional[Measurement] = Field(
        default=Measurement(),
        description="Measuring Data.",
    )

    metadata: Optional[Metadata] = Field(
        default=Metadata(),
        description="Metadata of the Potentiostat.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
<<<<<<< HEAD
        default="01b5fdc2e92add8386e9d335f576018888635f17"
=======
        default="466366e7b75450efb6b154eca033fc469f36e2a4"
>>>>>>> 5e18871 (updated core)
    )
