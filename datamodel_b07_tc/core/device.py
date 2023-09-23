import sdRDM

from typing import Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.utils import forge_signature, IDGenerator


@forge_signature
class Device(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("deviceINDEX"),
        xml="@id",
    )

    manufacturer: Optional[str] = Field(
        default=None,
        description="name of the manufacturer of the device.",
    )

    device_type: Optional[str] = Field(
        default=None,
        description="type given by the manufacturer of the device.",
    )

    series: Optional[str] = Field(
        default=None,
        description="the series of the device.",
    )

    on_off: Optional[bool] = Field(
        default=None,
        description="operational mode of the flow module. True is on and False is off.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="bbb668ee02d61b804e0aaa03c0a40b01dd45cfd3"
    )
