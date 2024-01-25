import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .material import Material


@forge_signature
class Insulation(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@2142e14e0bb639468af89bac2b4b7b5dbd2087b1#Insulation"
    },
):
    """Small type for attribute 'insulation'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )
    thickness: Optional[float] = element(
        default=None, tag="thickness", json_schema_extra=dict()
    )
    material: Optional[str] = element(
        default=None, tag="material", json_schema_extra=dict()
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="2142e14e0bb639468af89bac2b4b7b5dbd2087b1"
    )


@forge_signature
class Tubing(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@2142e14e0bb639468af89bac2b4b7b5dbd2087b1#Tubing"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    material: Optional[Material] = element(
        description="material with which the fluid flowing through comes into contact.",
        default=None,
        tag="material",
        json_schema_extra=dict(),
    )

    inner_diameter: Optional[float] = element(
        description="inner diameter of the tubing in mm.",
        default=None,
        tag="inner_diameter",
        json_schema_extra=dict(),
    )

    outer_diameter: Optional[float] = element(
        description="outer diameter of the tubing in mm.",
        default=None,
        tag="outer_diameter",
        json_schema_extra=dict(),
    )

    length: Optional[int] = element(
        description="length of the tubing in mm.",
        default=None,
        tag="length",
        json_schema_extra=dict(),
    )

    insulation: Optional[Insulation] = element(
        description="insulation of the tubing.",
        default_factory=Insulation,
        tag="insulation",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="2142e14e0bb639468af89bac2b4b7b5dbd2087b1"
    )
