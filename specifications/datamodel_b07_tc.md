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
- project
  - Type: string
  - Description: Name of the project this work is related to.
- description
  - Type: string
  - Description: describes the content of the dataset.
- authors
  - Type: Author
  - Multiple: True
  - Description: authors of this dataset.
- contact
  - Type: Contact
  - Description: point of contact for this projecet
- subject
  - Type: string
  - Multiple: True
  - Description: Domain-specific Subject Categories that are topically relevant to the Dataset.
- related_publication
  - Type: RelatedPublication
  - Description: Related publication to the dataset.
- keywords
  - Type: Keyword
  - Multiple: True
  - Description: Keywords and url related to the project.
- topic_classification
  - Type: TopicClassification
  - Multiple: True
  - Description: Topic classification.


### Author

- name
  - Type: string
  - Description: full name including given and family name.
- affiliation
  - Type: string
  - Description: organization the author is affiliated to.
- identifier_scheme
  - Type: string
  - Description: Name of the identifier scheme (ORCID, ISNI).
- identifier
  - Type: string
  - Description: Uniquely identifies an individual author or organization, according to various schemes.

### Contact

- name
  - Type: string
  - Description: full name including given and family name.
- affiliation
  - Type: string
  - Description: organization the author is affiliated to.
- email
  - Type: string
  - Description: The e-mail address of the contact for the Dataset

### RelatedPublication

- citation
  - Type: string
  - Description: The full bibliographic citation for this related publication.
- id_type
  - Type: string
  - Description: The type of digital identifier used for this publication (e.g., Digital Object Identifier (DOI)).
- id_number
  - Type: string
  - Description: 'The identifier for the selected ID type.'
- url
  - Type: string
  - Description: 'Link to the publication web page (e.g., journal article page, archive record page, or other).

### Keyword

- term
  - Type: string
  - Description: Key terms that describe important aspects of the Dataset. 
- vocabulary
  - Type: string
  - Description: For the specification of the keyword controlled vocabulary in use, such as LCSH, MeSH, or others.
- vocabulary_url
  - Type: string
  - Description: Keyword vocabulary URL points to the web presence that describes the keyword vocabulary, if appropriate.

### TopicClassification

- term
  - Type: string
  - Description: Topic or Subject term that is relevant to this Dataset.
- vocabulary
  - Type: string
  - Description: Provided for specification of the controlled vocabulary in use, e.g., LCSH, MeSH, etc.
- vocabulary_url
  - Type: string
  - Description: Specifies the URL location for the full controlled vocabulary.

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
- regression_coefficients
  - Type: float
  - Multiple: True
  - Description: Polynomial coefficients in order of increasing degree.
- degree
  - Type: int
  - Default: 1
  - Description: Degree of regression model.


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
GALVANOSTAT  = "Galvanostat"
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
RETENTIONTIME = "Retention time"
PEAKTYPE = "Peak type"
PEAKAREA = "Peak area"
PEAKHEIGHT = "Peak height"
PEAKAREAPERCENTAGE = "Peak area percentage"
PEAKASSIGNMENT = "Peak assignment"
FARADAYEFFIECENCY = "Faraday efficiency"
```


### MeasurementType

List of different measurements that do not need any further quantities to be defined.

```python
POTENTIOSTATIC = "Potentiostatic measurement"
GALVANOSTATIC  = "Galvanostatic measurement"
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