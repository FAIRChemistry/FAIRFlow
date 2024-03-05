import sdRDM

from typing import List, Optional
from uuid import uuid4
from pydantic import PrivateAttr
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature


from .calibration import Calibration
from .speciesdata import SpeciesData
from .component import Component
from .measurement import Measurement
from .data import Data
from .plantsetup import PlantSetup
from .metadata import Metadata
from .measurementtype import MeasurementType


@forge_signature
class Experiment(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@238a0547367fc736463730403ca8c1b7c46e9422#Experiment"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = element(
        description="the individual plant setup that is used in this one experiment.",
        default_factory=PlantSetup,
        tag="plant_setup",
        json_schema_extra=dict(),
    )

    measurements: List[Measurement] = wrapped(
        "measurements",
        element(
            description=(
                "different measurements that are made within the scope of one"
                " experiment."
            ),
            default_factory=ListPlus,
            tag="Measurement",
            json_schema_extra=dict(
                multiple=True,
            ),
        ),
    )

    species_data: List[SpeciesData] = wrapped(
        "species_data",
        element(
            description="all provided and calculated data about a specific species.",
            default_factory=ListPlus,
            tag="SpeciesData",
            json_schema_extra=dict(
                multiple=True,
            ),
        ),
    )

    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="238a0547367fc736463730403ca8c1b7c46e9422"
    )

    def add_to_measurements(
        self,
        measurement_type: Optional[MeasurementType] = None,
        metadata: List[Metadata] = ListPlus(),
        experimental_data: List[Data] = ListPlus(),
        source: Optional[Component] = None,
        id: Optional[str] = None,
    ) -> Measurement:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            measurement_type (): type of a measurement, e.g. potentiostatic or gas chromatography.. Defaults to None
            metadata (): metadata of a measurement.. Defaults to ListPlus()
            experimental_data (): experimental data of a measurement.. Defaults to ListPlus()
            source (): measuring device the data stems from.. Defaults to None
        """

        params = {
            "measurement_type": measurement_type,
            "metadata": metadata,
            "experimental_data": experimental_data,
            "source": source,
        }

        if id is not None:
            params["id"] = id

        self.measurements.append(Measurement(**params))

        return self.measurements[-1]

    def add_to_species_data(
        self,
        species: Optional[str] = None,
        chemical_formula: Optional[str] = None,
        calibration: Optional[Calibration] = None,
        correction_factor: Optional[float] = None,
        electron_transfer: Optional[float] = None,
        faraday_efficiency: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> SpeciesData:
        """
        This method adds an object of type 'SpeciesData' to attribute species_data

        Args:
            id (str): Unique identifier of the 'SpeciesData' object. Defaults to 'None'.
            species (): name of the species.. Defaults to None
            chemical_formula (): chemical formula of the species.. Defaults to None
            calibration (): calibration measurement.. Defaults to None
            correction_factor (): correction factors of the individual species.. Defaults to None
            electron_transfer (): Number of transfered electrons of the individual species.. Defaults to None
            faraday_efficiency (): Faraday efficiencies of the individual species.. Defaults to None
        """

        params = {
            "species": species,
            "chemical_formula": chemical_formula,
            "calibration": calibration,
            "correction_factor": correction_factor,
            "electron_transfer": electron_transfer,
            "faraday_efficiency": faraday_efficiency,
        }

        if id is not None:
            params["id"] = id

        self.species_data.append(SpeciesData(**params))

        return self.species_data[-1]
