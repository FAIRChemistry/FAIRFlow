import sdRDM

<<<<<<< HEAD
import json
=======
>>>>>>> 5e18871 (updated core)
from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
<<<<<<< HEAD
from pathlib import Path
from .chemicalformula import ChemicalFormula
from .metadata import Metadata
from .measurementtype import MeasurementType
from .calibration import Calibration
from .data import Data
from .speciesdata import SpeciesData
from .species import Species
from .measurement import Measurement
=======


from .data import Data
from .chemicalformula import ChemicalFormula
from .speciesdata import SpeciesData
from .species import Species
from .measurement import Measurement
from .measurementtype import MeasurementType
from .metadata import Metadata
from .calibration import Calibration
>>>>>>> 5e18871 (updated core)
from .plantsetup import PlantSetup


@forge_signature
class Experiment(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("experimentINDEX"),
        xml="@id",
    )

    plant_setup: Optional[PlantSetup] = Field(
        default=PlantSetup(),
        description="the individual plant setup that is used in this one experiment.",
    )

    measurements: List[Measurement] = Field(
        default_factory=ListPlus,
        multiple=True,
        description=(
            "different measurements that are made within the scope of one experiment."
        ),
    )

    species_data: List[SpeciesData] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="all provided and calculated data about a specific species.",
    )
    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
<<<<<<< HEAD
        default="01b5fdc2e92add8386e9d335f576018888635f17"
=======
        default="466366e7b75450efb6b154eca033fc469f36e2a4"
>>>>>>> 5e18871 (updated core)
    )

    def add_to_measurements(
        self,
        measurement_type: Optional[MeasurementType] = None,
        metadata: List[Metadata] = ListPlus(),
        experimental_data: List[Data] = ListPlus(),
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Measurement' to attribute measurements

        Args:
            id (str): Unique identifier of the 'Measurement' object. Defaults to 'None'.
            measurement_type (): type of a measurement, e.g. potentiostatic or gas chromatography.. Defaults to None
            metadata (): metadata of a measurement.. Defaults to ListPlus()
            experimental_data (): experimental data of a measurement.. Defaults to ListPlus()
        """
        params = {
            "measurement_type": measurement_type,
            "metadata": metadata,
            "experimental_data": experimental_data,
        }
        if id is not None:
            params["id"] = id
        self.measurements.append(Measurement(**params))
        return self.measurements[-1]

    def add_to_species_data(
        self,
        species: Optional[Species] = None,
        chemical_formula: Optional[ChemicalFormula] = None,
        calibration: Optional[Calibration] = None,
        correction_factor: Optional[float] = None,
        faraday_coefficient: Optional[float] = None,
        faraday_efficiency: Optional[Data] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'SpeciesData' to attribute species_data

        Args:
            id (str): Unique identifier of the 'SpeciesData' object. Defaults to 'None'.
            species (): name of the species.. Defaults to None
            chemical_formula (): chemical formula of the species.. Defaults to None
            calibration (): calibration measurement.. Defaults to None
            correction_factor (): correction factors of the individual species.. Defaults to None
            faraday_coefficient (): Faraday coefficients of the individual species.. Defaults to None
            faraday_efficiency (): Faraday efficiencies of the individual species.. Defaults to None
        """
        params = {
            "species": species,
            "chemical_formula": chemical_formula,
            "calibration": calibration,
            "correction_factor": correction_factor,
            "faraday_coefficient": faraday_coefficient,
            "faraday_efficiency": faraday_efficiency,
        }
        if id is not None:
            params["id"] = id
        self.species_data.append(SpeciesData(**params))
        return self.species_data[-1]
<<<<<<< HEAD

    def read_correction_factors(self, path: Path):
        with open(path, "r") as f:
            correction_factors_dict = json.load(f)
            for species, correction_factor in correction_factors_dict.items():
                for species_data_object in self.species_data:
                    if species_data_object.species == species:
                        species_data_object.correction_factor = correction_factor

    def read_faraday_coefficients(self, path: Path):
        with open(path, "r") as f:
            faraday_coefficients_dict = json.load(f)
            for (
                species,
                faraday_coefficient,
            ) in faraday_coefficients_dict.items():
                for species_data_object in self.species_data:
                    if species_data_object.species == species:
                        species_data_object.faraday_coefficient = faraday_coefficient

    @property
    def volumetric_flow_time_course(self) -> list:
        mfm_measurement = self.get(
            "measurements", "measurement_type", "MFM measurement"
        )[0][0]
        volumetric_flow_datetime_list = mfm_measurement.get(
            "experimental_data", "quantity", "Date time"
        )[0][0].values
        volumetric_flow_values_list = mfm_measurement.get(
            "experimental_data", "quantity", "Volumetric flow rate"
        )[0][0].values
        return [volumetric_flow_datetime_list, volumetric_flow_values_list]

    @property
    def initial_time(self) -> float:
        initial_time = float(
            self.get("measurements/metadata", "parameter", "TINIT")[0][0].value
        )
        return initial_time

    @property
    def initial_current(self) -> float:
        initial_current = float(
            self.get("measurements/metadata", "parameter", "IINIT")[0][0].value
        )
        return initial_current

    # def get_injection_date(self) -> datetime:

    #     injection_date_string = self.gc_measurements.get(
    #         "metadata", "parameter", "Injection Date"
    #     )[0][0].value
    #     inj_date_datetime = datetime.strptime(
    #         injection_date_string, "%d-%b-%y, %H:%M:%S"
    #     )
    #     return injection_date_string
=======
>>>>>>> 5e18871 (updated core)
