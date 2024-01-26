import sdRDM

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .speciesdata import SpeciesData
from .plantsetup import PlantSetup
from .generalinformation import GeneralInformation
from .measurement import Measurement
from .experiment import Experiment


@forge_signature
class Dataset(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a#Dataset"
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
        description="general data about the data model.",
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
        default="ecaec8b83d4ad94b6d8a4d0f7be4b76ce6cfa92a"
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
