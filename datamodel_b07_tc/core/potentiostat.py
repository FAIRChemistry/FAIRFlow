
from typing import Optional
from pydantic import Field
from sdRDM.base.utils import forge_signature, IDGenerator


<<<<<<< Updated upstream
=======
from .device import Device
from .metadata import Metadata
>>>>>>> Stashed changes
from .measurement import Measurement
from .device import Device
from .metadata import Metadata


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
<<<<<<< Updated upstream

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="8f3ba22c83330e0532dcb7cdb12b205c1f881980"
    )
=======
>>>>>>> Stashed changes
