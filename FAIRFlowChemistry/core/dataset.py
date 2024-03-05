import sdRDM

from typing import Dict, List, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from lxml.etree import _Element
from .speciesdata import SpeciesData
from .measurement import Measurement
from .experiment import Experiment
from .plantsetup import PlantSetup


@forge_signature
class GeneralInformation(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@d957c6074b70fafa6e197b474ff403e15b0f7142#GeneralInformation"
    },
):
    """Small type for attribute 'general_information'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )
    title: Optional[str] = element(default=None, tag="title", json_schema_extra=dict())
    project: Optional[str] = element(
        default=None, tag="project", json_schema_extra=dict()
    )
    description: Optional[str] = element(
        default=None, tag="description", json_schema_extra=dict()
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="d957c6074b70fafa6e197b474ff403e15b0f7142"
    )


@forge_signature
class Dataset(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@d957c6074b70fafa6e197b474ff403e15b0f7142#Dataset"
    },
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
            "general data about the datasetm like titel, project name, and description."
        ),
        default_factory=GeneralInformation,
        tag="general_information",
        json_schema_extra=dict(),
    )

    experiments: List[Experiment] = wrapped(
        "experiments",
        element(
            description="information about the individual experiment.",
            default_factory=ListPlus,
            tag="Experiment",
            json_schema_extra=dict(multiple=True),
        ),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="d957c6074b70fafa6e197b474ff403e15b0f7142"
    )

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        measurements: List[Measurement] = ListPlus(),
        species_data: List[SpeciesData] = ListPlus(),
        id: Optional[str] = None,
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


@forge_signature
class Dataset(sdRDM.DataModel):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    general_information: Optional[GeneralInformation] = element(
        description=(
            "general data about the datasetm like titel, project name, and description."
        ),
        default_factory=GeneralInformation,
        tag="general_information",
        json_schema_extra=dict(),
    )

    experiments: List[Experiment] = element(
        description="information about the individual experiment.",
        default_factory=ListPlus,
        tag="experiments",
        json_schema_extra=dict(multiple=True),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="8cd2a321d0f28e24e41c7a3ac5d90aa738b1646d"
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

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        measurements: List[Measurement] = ListPlus(),
        species_data: List[SpeciesData] = ListPlus(),
        id: Optional[str] = None,
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
