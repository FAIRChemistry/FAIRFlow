import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class Stoichiometry(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@db5f6da1081228bb92912b00a9cbad9be469320c#Stoichiometry"
    },
):
    """Stoichiometric information about the compound."""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    equivalents: Optional[float] = element(
        description="used equivalents in relation to the reference compound",
        default=None,
        tag="equivalents",
        json_schema_extra=dict(),
    )

    amount_of_substance: Optional[float] = element(
        description="amount of substance n in mmol",
        default=None,
        tag="amount_of_substance",
        json_schema_extra=dict(),
    )

    mass: Optional[float] = element(
        description="used mass of the compound in g",
        default=None,
        tag="mass",
        json_schema_extra=dict(),
    )

    volume: Optional[float] = element(
        description="volume of the compound",
        default=None,
        tag="volume",
        json_schema_extra=dict(),
    )

    density: Optional[float] = element(
        description="density of the compound at standard temperature and pressure.",
        default=None,
        tag="density",
        json_schema_extra=dict(),
    )

    molar_mass: Optional[float] = element(
        description="molar mass of the compound in g per mol",
        default=None,
        tag="molar_mass",
        json_schema_extra=dict(),
    )

    mass_concentration: Optional[float] = element(
        description="mass concentration in percent.",
        default=None,
        tag="mass_concentration",
        json_schema_extra=dict(),
    )

    molar_concentration: Optional[float] = element(
        description="molar concentration in mol per l.",
        default=None,
        tag="molar_concentration",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="db5f6da1081228bb92912b00a9cbad9be469320c"
    )
