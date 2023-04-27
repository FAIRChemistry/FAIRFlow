# Data model for CRC 1333 project B02 TC

This is the perliminary data model for CRC 1333 project B02. At the current time, the data model is still under development and major changes can occur at any time. Please feel free to make changes and contribute to the project.

## Objects

### Dataset
- general_information
  - Type: GeneralInformation
  - Description: general data about the data model.
- experiments
  - Type: Experiment
  - Multiple: True
  - Description: information about the individual experiment.

### GeneralInformation
- title
  - Type: string
  - Description: title of the work.
- description
  - Type: string
  - Description: describes the content of the dataset.
- authors
  - Type: Author
  - Multiple: True
  - Description: authors of this dataset.

### Author
This is another object that represents the author of the dataset. Please note, that the options here contain all required fields but also custom ones. In this example, the ```Dataverse``` option specifies where each field should be mapped, when exported to a Dataverse format. Hence, these options allow you to link your dataset towards any other data model without writing code by yourself.
- name
  - Type: string
  - Description: full name including given and family name.
- affiliation
  - Type: string
  - Description: organization the author is affiliated to.

### Experiment
- plant_setup
  - Type: PlantSetup
- calculations
  - Type: Calculation
  - Description: all the calculations that are done within the scope of one experiment.

### PlantSetup
- devices
  - Type: Device
  - Multiple: True
  - Description: bla
- tubing
  - Type: Tubing
  - Multiple: True
  - Description: bla
- input
  - Type: Input
  - Multiple: True
  - Description: bla
- output
  - Type: Output
  - Multiple: True
  - Description: bla

### Device
- manufacturer
  - Type: string
  - Description: name of the manufacturer of the device.
- device_type
  - Type: string
  - Description: type given by the manufacturer of the device.
- series
  - Type: string
  - Description: the series of the device.
- on_off
  - Type: string
  - Description: operational mode of the flow module.

### Pump[_Device_]
- pump_type
  - Type: PumpType
  - Description: type of the pump.

### Thermocouple[_Device_]
- thermocouple_type
  - Type: ThermocoupleType
  - Description: type of thermocouple like J, K and so on.  

### MassFlowMeter[_Device_]
- min_flow
  - Type: Parameter
  - Description: Minimum possible flow rate.
- max_flow
  - Type: Parameter
  - Description: Maximum possible flow rate.
- mass_flow_rates
  - Type: MassFlowRate
  - Multiple: True
  - Description: Mass flow rate.

### MassFlowRate
- time
  - Type: Data
  - Description: time in seconds.
- flow_rate
  - Type: Data
  - Description: flow rate.

### Parameter
  - value
    - Type: float
    - Description: values.
  - unit
    - Type: Unit
    - Description: unit of the values.

### Data
  - values
    - Type: float
    - Multiple: True
    - Description: values.
  - unit
    - Type: enum
    - Description: unit of the values.

### Tubing
- material
  - Type: Material
  - Description: material with which the fluid flowing through comes into contact.
- inner_diameter
  - Type: float
  - Description: inner diameter of the tubing in mm.
- outer_diameter
  - Type: float
  - Description: outer diameter of the tubing in mm.
- length
  - Type: integer
  - Description: length of the tubing in mm.
- insulation
  - Type: Insulation
  - Description: insulation of the tubing.

### Input
- component
  - Type: Chemical
  - Multiple: True
  - Description: component of the output fluid.

### Output
- component
  - Type: Chemical
  - Multiple: True
  - Description: component of the output fluid.

### Chemical
- name
  - Type: string
  - Description: IUPAC name of the compound.
  - Multiple: True
- formula
  - Type: string
  - Description: molecular formula of the compound.
- pureness
  - Type: float
  - Description: pureness of the compound in percent.
- supplier
  - Type: string
  - Description: name of the supplier of the compound.
- stoichiometry
  - Type: Stoichiometry
  - Description: stoichiometric information like equivalents, mass, amount of substance, volume
- state_of_matter
  - Type: string
  - Description: s for solid, l for liquid and g for gaseous
- role
  - Type: Role
  - Description: Role of the chemical.

### Stoichiometry
Stoichiometric information about the compound.
- equivalents
  - Type: float
  - Description: used equivalents in relation to the reference compound
- amount_of_substance
  - Type: float
  - Description: amount of substance n in mmol
- mass
  - Type: float
  - Description: used mass of the compound in g
- volume
  - Type: float
  - Description: volume of the compound
- density
  - Type: float
  - Description: density of the compound at standard temperature and pressure.
- molar_mass
  - Type: float
  - Description: molar mass of the compound in g per mol
- mass_concentration
  - Type: float
  - Description: mass concentration in percent.
- molar_concentration
  - Type: float
  - Description: molar concentration in mol per l.

### Insulation
- thickness
  - Type: float
  - Description: diameter of the insulating layer in mm.
- material
  - Type: Material
  - Description: insulating material

### GC[_Device_]
- gc_measurements
  - Type: GCMeasurement
  - Multiple: True
  - Description: GC measurements.

### GCMeasurement
- retention_time
  - Type: Data
  - Multiple: True
  - Description: retention time.
- peak_area
  - Type: Data
  - Multiple: True
  - Description: peak area.

### Series
- values
  - Type: float
  - Multiple: True
  - Description: bla

### Calculation
- calibrations
  - Type: Calibration
  - Multiple: True
  - Description: Calibration measurement.
- faraday_coefficients
  - Type: Data
  - Multiple: True
  - Description: Faraday coefficients.
  
### Calibration
- peak_area
  - Type: Data
  - Multiple: True
  - Description: Recorded peak areas of the individual calibration solutions.
- concentration
  - Type: Data
  - Multiple: True
  - Description: concentrations of the individual calibration solutions. 
- slope
  - Type: Data
  - Description: slopes of the (linear) calibration functions.
- intercept
  - Type: Data
  - Description: intercept of the (linear) calibration functions.
- coefficient_of_determination
  - Type: Data
  - Description: coefficients of the (linear) calibration functions.

## Enumerations

### ThermocoupleType
Different types of thermocouples.
```python
JTYPE = "Type J"
KTYPE = "Type K"
```

### Material
Different materials.
```python
SS14404 = "Stainless Steel 1.4404"
SS14571 = "Stainless Steel 1.4571"
SS14301 = "Stainless Steel 1.4301"
PTFE = "PTFE"
PFA = "PFA"
STONEWOOL = "Stone Wool"
GLASSWOOL = "Glass Wool"
GLASSFIBER = "Glass Fiber"
```

### PumpType
Different types of pumps.
```python
TUBINGPUMP = "Tubing pump"
DIAPHRAGMPUMP = "Diaphragm pump"
```

### Role
Role that a chemical plays in a process.
```python
EDUCT = "Educt"
PRODUCT = "Product"
CATALYST = "Catalyst"
SOLVENT = "Solvent"
INERTGAS = "Inert Gas"
```

### DeviceList
List of devices that are part of a plant.
```python
MASSFLOWCONTROLLER = "Mass flow controller"
HPLC = "HPLC"
POTENTIOSTAT = "Potentiostat"
PRESSURETRANSDUCER = "Pressure transducer"
CONTROLUNIT = "Control unit"
```

### Unit
List of units that are supported by the datamodel.
```python
NONE = "none"
VOLFRACTION = "vol%"
PERCENTAGE = "%"
SECONDS = "s"
MINUTES = "min"
HOURS = "h"
KILOGRAMS = "kg"
GRAMS = "g"
MILLIGRAMS = "mg"
LITER = "L"
MILLILITER = "mL"
KILOGRAMPERHOUR = "kg/h"
GRAMPERSECOND = "g/s"
MILLILITERPERSECOND = "ml/s"
```