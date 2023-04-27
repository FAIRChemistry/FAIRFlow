from enum import Enum


class DeviceList(Enum):
    MASSFLOWCONTROLLER = "Mass flow controller"
    HPLC = "HPLC"
    POTENTIOSTAT = "Potentiostat"
    PRESSURETRANSDUCER = "Pressure transducer"
    CONTROLUNIT = "Control unit"
