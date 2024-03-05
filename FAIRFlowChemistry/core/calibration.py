import sdRDM

from typing import List, Optional
from uuid import uuid4
from pydantic import PrivateAttr
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature


from .data import Data


@forge_signature
class Calibration(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@238a0547367fc736463730403ca8c1b7c46e9422#Calibration"
    },
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

    regression_coefficients: List[float] = wrapped(
        "regression_coefficients",
        element(
            description="regression coefficients in order of increasing degree.",
            default_factory=ListPlus,
            tag="float",
            json_schema_extra=dict(
                multiple=True,
            ),
        ),
    )

    degree: Optional[int] = element(
        description="degree of regression model.",
        default=1,
        tag="degree",
        json_schema_extra=dict(),
    )

    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="238a0547367fc736463730403ca8c1b7c46e9422"
    )
