import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .experiment import Experiment
from .plantsetup import PlantSetup
from .speciesdata import SpeciesData
from .generalinformation import GeneralInformation
from .measurement import Measurement


@forge_signature
class Dataset(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("datasetINDEX"),
        xml="@id",
    )

    general_information: Optional[GeneralInformation] = Field(
        description="general data about the data model.",
        default_factory=GeneralInformation,
    )

    experiments: List[Experiment] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="information about the individual experiment.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="ed10fc6e603fb8f740a021c26dca5f02dcdc1043"
    )

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        measurements: List[Measurement] = ListPlus(),
        species_data: List[SpeciesData] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
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
