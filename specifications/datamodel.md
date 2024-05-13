# Data model for the FAIRFlowChemistry platform

In this markdown file the structure of the data model for the FAIRFlowChemistry platform is defined.
It follows the syntax specified by the sdRDM engine.

## Objects

### Dataset

- general_information
  - Type: { title: string, project: string, description: string, purpose: string }
  - Description: general data about the dataset like titel, project name, description, and purpose.
- experiments
  - Type: Experiment[]
  - Description: information about the individual experiment.

### Experiment

- plant_setup
  - Type: PlantSetup
  - Description: the individual plant setup that is used in this one experiment.
- measurements
  - Type: Measurement[]
  - Description: different measurements that are made within the scope of one experiment.
- species_data
  - Type: SpeciesData[]
  - Description: all provided and calculated data about a specific species.


### PlantSetup

- components
  - Type: Component[]
  - Description: bla.
- input
  - Type: string[]
  - Description: bla.
- output
  - Type: string[]
  - Description: bla.

### Measurement

- _measurement_type_
  - Type: MeasurementType
  - Description: type of a measurement, e.g. potentiostatic or gas chromatography.
- metadata
  - Type: Metadata[]
  - Description: metadata of a measurement.
- experimental_data
  - Type: Data[]
  - Description: experimental data of a measurement.
- source
  - Type: Component
  - Description: measuring device the data stems from.


### SpeciesData

- species
  - Type: string
  - Description: name of the species.
- chemical_formula
  - Type: string
  - Description: chemical formula of the species.
- calibration
  - Type: Calibration
  - Description: calibration measurement.
- correction_factor
  - Type: float
  - Description: correction factors of the individual species.
- electron_transfer
  - Type: float
  - Description: Number of transfered electrons of the individual species.
- faraday_efficiency
  - Type: Data
  - Description: Faraday efficiencies of the individual species.
  

### Component

- component_type
  - Type: ComponentType
  - Description: equipment or piping component.
- component_id
  - Type: string
  - Description: id used to unambiguously identify the component.
- component_class
  - Type: string
  - Description: class of the component.
- component_class_uri
  - Type: string
  - Description: uri of the component.
- component_name
  - Type: string
  - Description: name of the component used to link between the abstract component and its shape.
- generic_attributes
  - Type: GenericAttibute[]
  - Description: a generic attribute as defined by DEXPI.
- connections
  - Type: string[]
  - Description: component id of other component this component is connected to via pipes, wires or similar.

###  GenericAttibute

- name
  - Type: string
  - Description: bla.
- attribute_uri
  - Type: string
  - Description: bla.
- value
  - Type: string
  - Description: bla.
- format
  - Type: string
  - Description: bla.
- units
  - Type: string
  - Description: bla.
- units_uri
  - Type: string
  - Description: bla

### Parameter

  - value
    - Type: float
    - Description: values.
  - unit
    - Type: Unit
    - Description: unit of the values.


### Data

- quantity
  - Type: Quantity
  - Description: quantity of a value.
- values
  - Type: float, string, datetime[]
  - Description: values.
- unit
  - Type: Unit
  - Description: unit of the values.


### Metadata

- parameter
  - Type: string
  - Description: name of the parameter.
- value
  - Type: string, float, datetime
  - Description: value of the parameter.
- abbreviation
  - Type: string
  - Description: abbreviation for the parameter.
- data_type
  - Type: DataType
  - Description: type of the parameter.
- mode
  - Type: string
  - Description: mode of the parameter. e.g., on and off.
- unit
  - Type: Unit
  - Description: unit of the parameter.
- description
  - Type: string
  - Description: description of the parameter.


### Calibration

- peak_areas
  - Type: Data
  - Description: recorded peak areas of the individual calibration solutions.
- concentrations
  - Type: Data
  - Description: concentrations of the individual calibration solutions. 
- regression_coefficients
  - Type: float[]
  - Description: regression coefficients in order of increasing degree.
- degree
  - Type: int
  - Default: 1
  - Description: degree of regression model.


## Enumerations

### ComponentType

Component types.

```python
EQUIPMENT = 'Equipment'
PIPINGCOMPONENT = 'Piping component'
```


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
SIGNAL = "Signal"
```


### MeasurementType

List of different measurements that do not need any further quantities to be defined.

```python
POTENTIOSTATIC = "Potentiostatic measurement"
GC = "GC measurement"
MFM = "MFM measurement"
```