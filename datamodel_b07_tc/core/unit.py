from enum import Enum


class Unit(Enum):
    NONE = "none"
    VOLFRACTION = "vol%"
    PERCENTAGE = "%"
    SECONDS = "s"
    MINUTES = "min"
    HOURS = "h"
    YEARSMONTHSDAYSHOURSMINUTESSECONDS = "YYYY-MM-DDTHH:MM:SS. mmmmmm"
    KILOGRAMS = "kg"
    GRAMS = "g"
    MILLIGRAMS = "mg"
    LITER = "L"
    MILLILITER = "mL"
    KILOGRAMPERHOUR = "kg/h"
    GRAMPERSECOND = "g/s"
    MILLILITERPERSECOND = "ml/s"
