import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .generalinformation import GeneralInformation
from .experiment import Experiment
from .measurement import Measurement
from .plantsetup import PlantSetup
from .analysis import Analysis


@forge_signature
class Dataset(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("datasetINDEX"),
        xml="@id",
    )

    general_information: Optional[GeneralInformation] = Field(
        default=None,
        description="general data about the data model.",
    )

    experiments: List[Experiment] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="information about the individual experiment.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="6a28c05c7b083b9ad2b52323e96000b4075f6c52"
    )

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        measurements: List[Measurement] = ListPlus(),
        analysis: Optional[Analysis] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Experiment' to attribute experiments

        Args:
            id (str): Unique identifier of the 'Experiment' object. Defaults to 'None'.
            plant_setup (): the individual plant setup that is used in this one experiment.. Defaults to None
            measurements (): different measurements that are made within the scope of one experiment.. Defaults to ListPlus()
            analysis (): all the calculations that are done within the scope of one experiment.. Defaults to None
        """

        params = {
            "plant_setup": plant_setup,
            "measurements": measurements,
            "analysis": analysis,
        }

        if id is not None:
            params["id"] = id

        self.experiments.append(Experiment(**params))
