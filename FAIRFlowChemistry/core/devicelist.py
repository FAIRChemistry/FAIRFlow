from enum import Enum


class DeviceList(Enum):
    MASSFLOWCONTROLLER = "Mass flow controller"
    HPLC = "HPLC"
    GC = "GC"
    POTENTIOSTAT = "Potentiostat"
    GALVANOSTAT = "Galvanostat"
    PRESSURETRANSDUCER = "Pressure transducer"
    CONTROLUNIT = "Control unit"
