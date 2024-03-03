```mermaid
classDiagram
    Dataset *-- GeneralInformation
    Dataset *-- Experiment
    GeneralInformation *-- Author
    GeneralInformation *-- RelatedPublication
    GeneralInformation *-- Keyword
    GeneralInformation *-- TopicClassification
    Experiment *-- PlantSetup
    Experiment *-- Measurement
    Experiment *-- SpeciesData
    PlantSetup *-- Component
    Component *-- ComponentType
    Component *-- GenericAttibute
    Data *-- Quantity
    Metadata *-- DataType
    Measurement *-- MeasurementType
    Measurement *-- Component
    Measurement *-- Data
    Measurement *-- Metadata
    SpeciesData *-- Species
    SpeciesData *-- ChemicalFormula
    SpeciesData *-- Data
    SpeciesData *-- Calibration
    Calibration *-- Data
    
    class Dataset {
        +GeneralInformation general_information
        +Experiment[0..*] experiments
    }
    
    class GeneralInformation {
        +string title
        +string project
        +string description
        +Author[0..*] authors
        +Contact contact
        +string[0..*] subject
        +RelatedPublication related_publication
        +Keyword[0..*] keywords
        +TopicClassification[0..*] topic_classification
    }
    
    class Author {
        +string name
        +string affiliation
        +string identifier_scheme
        +string identifier
    }
    
    class RelatedPublication {
        +string citation
        +string id_type
        +string id_number
        +string url
    }
    
    class Keyword {
        +string value
        +string vocabulary
        +string vocabulary_uri
    }
    
    class TopicClassification {
        +string value
        +string vocab
        +string vocab_uri
    }
    
    class Experiment {
        +PlantSetup plant_setup
        +Measurement[0..*] measurements
        +SpeciesData[0..*] species_data
    }
    
    class PlantSetup {
        +Component[0..*] component
        +string[0..*] input
        +string[0..*] output
    }
    
    class Component {
        +ComponentType component_type
        +string component_id
        +string component_class
        +string component_class_uri
        +string component_name
        +GenericAttibute[0..*] generic_attributes
        +string[0..*] connections
    }
    
    class GenericAttibute {
        +string name
        +string attribute_uri
        +string value
        +string format
        +string units
        +string units_uri
    }
    
    class Parameter {
        +float value
        +Unit unit
    }
    
    class Data {
        +Quantity quantity
        +float, string, datetime[0..*] values
        +Unit unit
    }
    
    class Metadata {
        +string parameter
        +string, float, datetime value
        +string abbreviation
        +DataType, string data_type
        +string mode
        +Unit unit
        +string description
    }
    
    class Measurement {
        +MeasurementType measurement_type
        +Metadata[0..*] metadata
        +Data[0..*] experimental_data
        +Component source
    }
    
    class SpeciesData {
        +Species species
        +ChemicalFormula chemical_formula
        +Calibration calibration
        +float correction_factor
        +float faraday_coefficient
        +Data faraday_efficiency
    }
    
    class Calibration {
        +Data peak_areas
        +Data concentrations
        +float[0..*] regression_coefficients
        +int degree
    }
    
    class ComponentType {
        << Enumeration >>
        +EQUIPMENT
        +PIPINGCOMPONENT
    }
    
    class DataType {
        << Enumeration >>
        +STRING
        +FLOAT
        +DATE
        +TIME
        +DATETIME
        +BOOLEAN
        +INTEGER
        +NONE
        +LABEL
    }
    
    class Quantity {
        << Enumeration >>
        +TIME
        +VOLTAGE
        +CURRENT
        +SURFACEAREA
        +CONCENTRATION
        +MASS
        +MASSFLOWRATE
        +VOLUMETRICFLOWRATE
        +DATETIME
        +FRACTION
        +RETENTIONTIME
        +PEAKTYPE
        +PEAKAREA
        +PEAKHEIGHT
        +PEAKAREAPERCENTAGE
        +PEAKASSIGNMENT
        +FARADAYEFFIECENCY
    }
    
    class MeasurementType {
        << Enumeration >>
        +POTENTIOSTATIC
        +GC
        +MFM
    }
    
    class Species {
        << Enumeration >>
        +HYDROGEN
        +CARBONDIOXIDE
        +CARBONMONOXIDE
        +METHANE
        +ETHENE
        +ETHANE
    }
    
    class ChemicalFormula {
        << Enumeration >>
        +H2
        +CO2
        +CO
        +CH4
        +C2H4
        +C2H6
    }
    
```