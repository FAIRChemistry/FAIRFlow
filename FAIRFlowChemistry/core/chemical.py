import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature
from .stoichiometry import Stoichiometry
from .reactantrole import ReactantRole


@forge_signature
class Chemical(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@cc21fbb7a702dae1961589c15c88101f41227f56#Chemical"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    name: Optional[str] = element(
        description="IUPAC name of the compound.",
        default=None,
        tag="name",
        json_schema_extra=dict(),
    )

    formula: Optional[str] = element(
        description="molecular formula of the compound.",
        default=None,
        tag="formula",
        json_schema_extra=dict(),
    )

    pureness: Optional[float] = element(
        description="pureness of the compound in percent.",
        default=None,
        tag="pureness",
        json_schema_extra=dict(),
    )

    supplier: Optional[str] = element(
        description="name of the supplier of the compound.",
        default=None,
        tag="supplier",
        json_schema_extra=dict(),
    )

    stoichiometry: Optional[Stoichiometry] = element(
        description=(
            "stoichiometric information like equivalents, mass, amount of substance,"
            " volume"
        ),
        default_factory=Stoichiometry,
        tag="stoichiometry",
        json_schema_extra=dict(),
    )

    state_of_matter: Optional[str] = element(
        description="s for solid, l for liquid and g for gaseous",
        default=None,
        tag="state_of_matter",
        json_schema_extra=dict(),
    )

    reactant_role: Optional[ReactantRole] = element(
        description=(
            "Role that a reactand plays in a chemical reaction or  in a process."
        ),
        default=None,
        tag="reactant_role",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="cc21fbb7a702dae1961589c15c88101f41227f56"
    )
