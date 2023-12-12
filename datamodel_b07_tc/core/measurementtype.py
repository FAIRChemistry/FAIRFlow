from enum import Enum


class MeasurementType(Enum):
    POTENTIOSTATIC = "Potentiostatic measurement"
    GALVANOSTATIC = "Galvanostatic measurement"
    GC = "GC measurement"
    MFM = "MFM measurement"
