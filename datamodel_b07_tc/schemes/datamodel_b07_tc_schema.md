```mermaid
classDiagram
    Device <-- Pump
    Device <-- Thermocouple
    Device <-- MassFlowMeter
    Device <-- GC
    Dataset *-- GeneralInformation
    Dataset *-- Experiment
    GeneralInformation *-- Author
    Experiment *-- PlantSetup
    Experiment *-- Calculation
    PlantSetup *-- Device
    PlantSetup *-- Tubing
    PlantSetup *-- Input
    PlantSetup *-- Output
    Pump *-- PumpType
    Thermocouple *-- ThermocoupleType
    MassFlowMeter *-- MassFlowRate
    MassFlowMeter *-- Parameter
    MassFlowRate *-- Data
    Parameter *-- Unit
    Tubing *-- Material
    Tubing *-- Insulation
    Input *-- Chemical
    Output *-- Chemical
    Chemical *-- Role
    Chemical *-- Stoichiometry
    Insulation *-- Material
    GC *-- GCMeasurement
    GCMeasurement *-- Data
    Calculation *-- Data
    Calculation *-- Calibration
    Calibration *-- Data
    
    class Dataset {
        +GeneralInformation general_information
        +Experiment[0..*] experiments
    }
    
    class GeneralInformation {
        +string title
        +string description
        +Author[0..*] authors
    }
    
    class Author {
        +string name
        +string affiliation
    }
    
    class Experiment {
        +PlantSetup plant_setup
        +Calculation calculations
    }
    
    class PlantSetup {
        +Device[0..*] devices
        +Tubing[0..*] tubing
        +Input[0..*] input
        +Output[0..*] output
    }
    
    class Device {
        +string manufacturer
        +string device_type
        +string series
        +string on_off
    }
    
    class Pump {
        +PumpType pump_type
    }
    
    class Thermocouple {
        +ThermocoupleType thermocouple_type
    }
    
    class MassFlowMeter {
        +Parameter min_flow
        +Parameter max_flow
        +MassFlowRate[0..*] mass_flow_rates
    }
    
    class MassFlowRate {
        +Data time
        +Data flow_rate
    }
    
    class Parameter {
        +float value
        +Unit unit
    }
    
    class Data {
        +float[0..*] values
        +enum unit
    }
    
    class Tubing {
        +Material material
        +float inner_diameter
        +float outer_diameter
        +integer length
        +Insulation insulation
    }
    
    class Input {
        +Chemical[0..*] component
    }
    
    class Output {
        +Chemical[0..*] component
    }
    
    class Chemical {
        +string[0..*] name
        +string formula
        +float pureness
        +string supplier
        +Stoichiometry stoichiometry
        +string state_of_matter
        +Role role
    }
    
    class Stoichiometry {
        +float equivalents
        +float amount_of_substance
        +float mass
        +float volume
        +float density
        +float molar_mass
        +float mass_concentration
        +float molar_concentration
    }
    
    class Insulation {
        +float thickness
        +Material material
    }
    
    class GC {
        +GCMeasurement[0..*] gc_measurements
    }
    
    class GCMeasurement {
        +Data[0..*] retention_time
        +Data[0..*] peak_area
    }
    
    class Series {
        +float[0..*] values
    }
    
    class Calculation {
        +Calibration[0..*] calibrations
        +Data[0..*] faraday_coefficients
    }
    
    class Calibration {
        +Data[0..*] peak_area
        +Data[0..*] concentration
        +Data slope
        +Data intercept
        +Data coefficient_of_determination
    }
    
    class ThermocoupleType {
        << Enumeration >>
        +JTYPE
        +KTYPE
    }
    
    class Material {
        << Enumeration >>
        +SS14404
        +SS14571
        +SS14301
        +PTFE
        +PFA
        +STONEWOOL
        +GLASSWOOL
        +GLASSFIBER
    }
    
    class PumpType {
        << Enumeration >>
        +TUBINGPUMP
        +DIAPHRAGMPUMP
    }
    
    class Role {
        << Enumeration >>
        +EDUCT
        +PRODUCT
        +CATALYST
        +SOLVENT
        +INERTGAS
    }
    
    class DeviceList {
        << Enumeration >>
        +MASSFLOWCONTROLLER
        +HPLC
        +POTENTIOSTAT
        +PRESSURETRANSDUCER
        +CONTROLUNIT
    }
    
    class Unit {
        << Enumeration >>
        +NONE
        +VOLFRACTION
        +PERCENTAGE
        +SECONDS
        +MINUTES
        +HOURS
        +KILOGRAMS
        +GRAMS
        +MILLIGRAMS
        +LITER
        +MILLILITER
        +KILOGRAMPERHOUR
        +GRAMPERSECOND
        +MILLILITERPERSECOND
    }
    
```