
from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .device import Device
from .gcmeasurement import GCMeasurement
from .data import Data


@forge_signature
class GC(Device):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("gcINDEX"),
        xml="@id",
    )

    gc_measurements: List[GCMeasurement] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="GC measurements.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="15c1628100dadc5d2ce53ff72a02f247fae78748"
    )

    def add_to_gc_measurements(
        self,
        retention_time: List[Data] = ListPlus(),
        peak_area: List[Data] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'GCMeasurement' to attribute gc_measurements

        Args:
            id (str): Unique identifier of the 'GCMeasurement' object. Defaults to 'None'.
            retention_time (): retention time.. Defaults to ListPlus()
            peak_area (): peak area.. Defaults to ListPlus()
        """

        params = {
            "retention_time": retention_time,
            "peak_area": peak_area,
        }

        if id is not None:
            params["id"] = id

        self.gc_measurements.append(GCMeasurement(**params))
