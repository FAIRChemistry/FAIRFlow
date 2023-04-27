import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator

from pydantic.types import Enum

from .data import Data


@forge_signature
class GCMeasurement(sdRDM.DataModel):

    """"""

    id: str = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("gcmeasurementINDEX"),
        xml="@id",
    )

    retention_time: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="retention time.",
    )

    peak_area: List[Data] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="peak area.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="96bbf6ec578d62bf60443d8a32630f121f735f0a"
    )

    def add_to_retention_time(
        self,
        values: List[float] = ListPlus(),
        unit: Optional[Enum] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute retention_time

        Args:
            id (str): Unique identifier of the 'Data' object. Defaults to 'None'.
            values (): values.. Defaults to ListPlus()
            unit (): unit of the values.. Defaults to None
        """

        params = {
            "values": values,
            "unit": unit,
        }

        if id is not None:
            params["id"] = id

        self.retention_time.append(Data(**params))

    def add_to_peak_area(
        self,
        values: List[float] = ListPlus(),
        unit: Optional[Enum] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Data' to attribute peak_area

        Args:
            id (str): Unique identifier of the 'Data' object. Defaults to 'None'.
            values (): values.. Defaults to ListPlus()
            unit (): unit of the values.. Defaults to None
        """

        params = {
            "values": values,
            "unit": unit,
        }

        if id is not None:
            params["id"] = id

        self.peak_area.append(Data(**params))
