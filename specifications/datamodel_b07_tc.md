# Data model for CRC 1333 project B07 TC

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
  - Description: the individual plant setup that is used in this one experiment.
- measurements
  - Type: Measurement
  - Multiple: True
  - Description: different measurements that are made within the scope of one experiment.
- species_data
  - Type: SpeciesData
  - Multiple: True
  - Description: all provided and calculated data about a specific species.


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
  - Type: boolean
  - Description: operational mode of the flow module. True is on and False is off.


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


### Parameter

  - value
    - Type: float
    - Description: values.
  - unit
    - Type: UnitClass
    - Description: unit of the values.


### Potentiostat[_Device_]

- measurement
  - Type: Measurement
  - Description: Measuring Data.
- metadata
  - Type: Metadata
  - Description: Metadata of the Potentiostat.


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


### Insulation

- thickness
  - Type: float
  - Description: diameter of the insulating layer in mm.
- material
  - Type: Material
  - Description: insulating material


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
- reactant_role
  - Type: ReactantRole
  - Description: Role that a reactand plays in a chemical reaction or  in a process.


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


### Data

- quantity
  - Type: Quantity
  - Description: quantity of a value.
- values
  - Type: float, string, datetime
  - Multiple: True
  - Description: values.
- unit
  - Type: UnitClass
  - Description: unit of the values.


### Metadata

- parameter
  - Type: string
  - Description: Name of the parameter.
- value
  - Type: string, float, datetime
  - Description: value of the parameter.
- abbreviation
  - Type: string
  - Description: abbreviation for the parameter.
- data_type
  - Type: DataType, string
  - Description: type of the parameter.
- mode
  - Type: string
  - Description: mode of the parameter. E.g., on and off.
- unit
  - Type: UnitClass
  - Description: unit of the parameter.
- description
    - Type: string
    - Description: description of the parameter.


### Measurement

- _measurement_type_
  - Type: MeasurementType
  - Description: type of a measurement, e.g. potentiostatic or gas chromatography.
- metadata
  - Type: Metadata
  - Multiple: True
  - Description: metadata of a measurement.
- experimental_data
  - Type: Data
  - Multiple: True
  - Description: experimental data of a measurement.


### SpeciesData

- species
  - Type: Species
  - Description: name of the species.
- chemical_formula
  - Type: ChemicalFormula
  - Description: chemical formula of the species.
- calibration
  - Type: Calibration
  - Description: calibration measurement.
- correction_factor
  - Type: float
  - Description: correction factors of the individual species.
- faraday_coefficient
  - Type: float
  - Description: Faraday coefficients of the individual species.
- faraday_efficiency
  - Type: Data
  - Description: Faraday efficiencies of the individual species.
  

### Calibration

- peak_areas
  - Type: Data
  - Description: Recorded peak areas of the individual calibration solutions.
- concentrations
  - Type: Data
  - Description: concentrations of the individual calibration solutions. 
- regression_model
  - Type: LinearRegression
  - Description: Linear regression model.


## Enumerations


### DataType

Different data types are supported.

```python
STRING = 'string'
FLOAT = 'float'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
BOOLEAN = 'Boolean'
INTEGER = 'int'
NONE = 'NONE'
LABEL = 'label'
```


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


### ReactantRole

Role that a reactant plays in a chemical reaction or in a process.

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
GC = "GC"
POTENTIOSTAT = "Potentiostat"
PRESSURETRANSDUCER = "Pressure transducer"
CONTROLUNIT = "Control unit"
```


### Quantity

List of different quantities.

```python
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
SIGNAL = "Signal"
PEAKNUMBER = "Peak number"
RETENTIONTIME = "Retention time"
PEAKTYPE = "Peak type"
PEAKAREA = "Peak area"
PEAKHEIGHT = "Peak height"
PEAKAREAPERCENTAGE = "Peak area percentage"
SLOPE = "Slope"
INTERCEPT = "Intercept"
COEFFDET = "Coefficient of determination"
```


### MeasurementType

List of different measurements that do not need any further quantities to be defined.

```python
POTENTIOSTATIC = "Potentiostatic measurement"
GC = "GC measurement"
MFM = "MFM measurement"
``` 


### Species

List of different species.

```python
HYDROGEN = "Hydrogen"
CARBONDIOXIDE = "Carbon dioxide"
CARBONMONOXIDE = "Carbon monoxide"
METHANE = "Methane"
ETHENE = "Ethene"
ETHANE = "Ethane"
```


### ChemicalFormula

List of different chemical formulas.

```python
H2 = "H2"
CO2 = "CO2"
CO = "CO"
CH4 = "CH4"
C2H4 = "C2H4"
C2H6 = "C2H6"
```