import sdRDM

from typing import Dict, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .reactantrole import ReactantRole
from .stoichiometry import Stoichiometry


@forge_signature
class Chemical(sdRDM.DataModel):
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
        default="f8cdbee59156292c0dda1a7171efeb7a002d7a55"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self
