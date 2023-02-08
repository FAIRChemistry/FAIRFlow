# Data model for CRC 1333 project B02 TC

This is the perliminary data model for CRC 1333 project B02. At the current time, the data model is still under development and major changes can occur at any time. Please feel free to make changes and contribute to the project.

### Dataset

- __title*__
  - Type: string
  - Description: title of the work.
- __description*__
  - Type: string
  - Description: describes the content of the dataset.
- __authors*__
  - Type: Author
  - Multiple: True
  - Description: authors of this dataset.
- __process_scheme__
  - Type: ProcessScheme
  - Description: PandID like setup scheme of the reactor.


### Author

This is another object that represents the author of the dataset. Please note, that the options here contain all required fields but also custom ones. In this example, the ```Dataverse``` option specifies where each field should be mapped, when exported to a Dataverse format. Hence, these options allow you to link your dataset towards any other data model without writing code by yourself.

- __name*__
  - Type: string
  - Description: full name including given and family name.
- __affiliation__
  - Type: string
  - Description: to which organization the author is affiliated to.