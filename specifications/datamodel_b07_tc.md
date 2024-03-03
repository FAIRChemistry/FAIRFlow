# Data model for CRC 1333 project B07 TC

This is the perliminary data model for CRC 1333 project B07. At the current time, the data model is still under development and major changes can occur at any time. Please feel free to make changes and contribute to the project.

## Objects

### Dataset

- general_information
  - Type: GeneralInformation
  - Description: general data about the data model.
- experiments
  - Type: Experiment[]
  - Description: information about the individual experiment.


### GeneralInformation

- title
  - Type: string
  - Description: title of the work.
- project
  - Type: string
  - Description: name of the project this work is related to.
- description
  - Type: string
  - Description: describtion of the content of the dataset.
- authors
  - Type: Author[]
  - Description: authors of this dataset.
- contact
  - Type: {name:string, affiliation:string, email:string}
  - Description: point of contact for this project.
- subject
  - Type: string[]
  - Description: domain specific subject categories that are topically relevant to the dataset.
- related_publication
  - Type: RelatedPublication
  - Description: publication related to the dataset.
- keywords
  - Type: Keyword[]
  - Description: keywords and url related to the project.
- topic_classification
  - Type: TopicClassification[]
  - Description: topic classification.


### Author

- name
  - Type: string
  - Description: full name including given and family name.
- affiliation
  - Type: string
  - Description: organization the author is affiliated to.
- identifier_scheme
  - Type: string
  - Description: name of the identifier scheme (ORCID, ISNI).
- identifier
  - Type: string
  - Description: unique identifier of an individual author or organization, according to various schemes.


### RelatedPublication

- citation
  - Type: string
  - Description: full bibliographic citation for this related publication.
- id_type
  - Type: string
  - Description: type of digital identifier used for this publication, e.g., digital object identifier, DOI.
- id_number
  - Type: string
  - Description: identifier for the selected ID type.
- url
  - Type: string
  - Description: link to the publication web page, e.g., journal article page, archive record page, or other.


### Keyword

- value
  - Type: string
  - Description: key terms describing important aspects of the dataset. 
- vocabulary
  - Type: string
  - Description: for the specification of the keyword controlled vocabulary in use, such as LCSH, MeSH, or others.
- vocabulary_uri
  - Type: string
  - Description: keyword vocabulary URI points to the web presence that describes the keyword vocabulary, if appropriate.


### TopicClassification

- value
  - Type: string
  - Description: topic or Subject term that is relevant to this Dataset.
- vocab
  - Type: string
  - Description: provided for specification of the controlled vocabulary in use, e.g., LCSH, MeSH, etc.
- vocab_uri
  - Type: string
  - Description: specifies the URI location for the full controlled vocabulary.


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

- component
  - Type: Component[]
  - Description: bla.
- input
  - Type: string[]
  - Description: bla.
- output
  - Type: string[]
  - Description: bla.


### Component

- component_type
  - Type: ComponentType
  - Description: equipment or piping component.
- id
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
- generic_attribute
  - Type: string[]
  - Description: a generic attribute as defined by DEXPI.
- connections
  - Type: string[]
  - Description: other component this component is connected to via pipes, wires or similar.


### Parameter

  - value
    - Type: float
    - Description: values.
  - unit
    - Type: string
    - Description: unit of the values.


### Data

- quantity
  - Type: Quantity
  - Description: quantity of a value.
- values
  - Type: float, string, datetime[]
  - Description: values.
- unit
  - Type: string
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
  - Type: DataType, string
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
  - Description: recorded peak areas of the individual calibration solutions.
- concentrations
  - Type: Data
  - Description: concentrations of the individual calibration solutions. 
- regression_coefficients
  - Type: float[]
  - Description: polynomial coefficients in order of increasing degree.
- degree
  - Type: int
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