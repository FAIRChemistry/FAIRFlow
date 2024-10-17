from enum import Enum


class Quantity(Enum):

    TIME = "Time"
    VOLTAGE = "Voltage"
    CURRENT = "Current"
    SURFACEAREA = "Electrode surface area"
    CONCENTRATION = "Concentration"
    MASS = "Mass"
    MASSFLOWRATE = "Mass flow rate"
    VOLUMETRICFLOWRATE = "Volumetric flow rate"
    DATETIME = "Date time"
    FRACTION = "Fraction"
    RETENTIONTIME = "Retention time"
    PEAKTYPE = "Peak type"
    PEAKAREA = "Peak area"
    PEAKHEIGHT = "Peak height"
    PEAKAREAPERCENTAGE = "Peak area percentage"
    PEAKASSIGNMENT = "Peak assignment"
    FARADAYEFFIECENCY = "Faraday efficiency"
    SIGNAL = "Signal"
