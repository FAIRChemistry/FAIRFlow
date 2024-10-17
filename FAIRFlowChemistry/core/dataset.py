import sdRDM

from typing import Dict, List, Optional
from uuid import uuid4
from pydantic import PrivateAttr, model_validator
from pydantic_xml import attr, element
from lxml.etree import _Element

from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict



from .speciesdata import SpeciesData
from .measurement import Measurement
from .plantsetup import PlantSetup
from .experiment import Experiment


@forge_signature
class GeneralInformation(
    sdRDM.DataModel,
    search_mode="unordered",
):
    """Small type for attribute 'general_information'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    title: Optional[str] = element(
        default=None,
        tag="title",
        json_schema_extra=dict(),
    )

    project: Optional[str] = element(
        default=None,
        tag="project",
        json_schema_extra=dict(),
    )

    description: Optional[str] = element(
        default=None,
        tag="description",
        json_schema_extra=dict(),
    )

    purpose: Optional[str] = element(
        default=None,
        tag="purpose",
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


@forge_signature
class Dataset(
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

    general_information: Optional[GeneralInformation] = element(
        description=(
            "general data about the dataset like titel, project name, description, and"
            " purpose."
        ),
        default_factory=GeneralInformation,
        tag="general_information",
        json_schema_extra=dict(),
    )

    experiments: List[Experiment] = element(
        description="information about the individual experiment.",
        default_factory=ListPlus,
        tag="experiments",
        json_schema_extra=dict(
            multiple=True,
        ),
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

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        measurements: List[Measurement] = ListPlus(),
        species_data: List[SpeciesData] = ListPlus(),
        id: Optional[str] = None,
        **kwargs,
    ) -> Experiment:
        """
        This method adds an object of type 'Experiment' to attribute experiments

        Args:
            id (str): Unique identifier of the 'Experiment' object. Defaults to 'None'.
            plant_setup (): the individual plant setup that is used in this one experiment.. Defaults to None
            measurements (): different measurements that are made within the scope of one experiment.. Defaults to ListPlus()
            species_data (): all provided and calculated data about a specific species.. Defaults to ListPlus()
        """

        params = {
            "plant_setup": plant_setup,
            "measurements": measurements,
            "species_data": species_data,
        }

        if id is not None:
            params["id"] = id

        self.experiments.append(Experiment(**params))

        return self.experiments[-1]
