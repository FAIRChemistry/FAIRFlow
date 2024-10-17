import sdRDM

from typing import Dict, List, Optional
from uuid import uuid4
from pydantic import PrivateAttr, model_validator
from pydantic_xml import attr, element
from lxml.etree import _Element

from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict



from .data import Data


@forge_signature
class Calibration(
    sdRDM.DataModel,
    search_mode="unordered",
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    peak_areas: Optional[Data] = element(
        description="recorded peak areas of the individual calibration solutions.",
        default_factory=Data,
        tag="peak_areas",
        json_schema_extra=dict(),
    )

    concentrations: Optional[Data] = element(
        description="concentrations of the individual calibration solutions.",
        default_factory=Data,
        tag="concentrations",
        json_schema_extra=dict(),
    )

    regression_coefficients: List[float] = element(
        description="regression coefficients in order of increasing degree.",
        default_factory=ListPlus,
        tag="regression_coefficients",
        json_schema_extra=dict(
            multiple=True,
        ),
    )

    degree: Optional[int] = element(
        description="degree of regression model.",
        default=1,
        tag="degree",
        json_schema_extra=dict(),
    )

    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlow"
    )
    _commit: Optional[str] = PrivateAttr(
        default="e8eb42f3ed30a3b47a5f17238ca156f6ff6d5e4b"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                isinstance(i, _Element) for i in value
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)

        return self
