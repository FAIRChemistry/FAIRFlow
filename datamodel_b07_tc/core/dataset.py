import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .experiment import Experiment
from .plantsetup import PlantSetup
from .calculation import Calculation
from .generalinformation import GeneralInformation


@forge_signature
class Dataset(sdRDM.DataModel):

    """"""

    id: str = Field(
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
        default="15c1628100dadc5d2ce53ff72a02f247fae78748"
    )

    def add_to_experiments(
        self,
        plant_setup: Optional[PlantSetup] = None,
        calculations: Optional[Calculation] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Experiment' to attribute experiments

        Args:
            id (str): Unique identifier of the 'Experiment' object. Defaults to 'None'.
            plant_setup (): . Defaults to None
            calculations (): all the calculations that are done within the scope of one experiment.. Defaults to None
        """

        params = {
            "plant_setup": plant_setup,
            "calculations": calculations,
        }

        if id is not None:
            params["id"] = id

        self.experiments.append(Experiment(**params))
