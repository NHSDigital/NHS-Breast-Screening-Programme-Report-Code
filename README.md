Repository owner: [NHS Digital](https://github.com/NHSDigital)

Email: cancer.screening@nhs.net

To contact us raise an issue via email and we will respond promptly.

## Clone repository
To clone respositary, please see our [community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/development-approach/02_using-git-collaboratively.md).

## Set up environment
There are two options to set up the python enviroment:
1.1 Pip using `requirements.txt`.
1.2. Conda using `environment.yml`.

Users would need to delete as appropriate which set they do not need. For details, please see our [virtual environments in the community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/python/virtual-environments.md).


Run the following command in Terminal or VScode to set up the package
```
pip install --user --no-warn-script-location -r requirements.txt
```

or if using conda environments:
```
conda env create -f environment.yml
```

The first line of the `.yml` file sets the new environment's name. In this template, the name is `rap`.

2. Activate the new environment: 
```
    conda activate <enviroment_name>
```

3. Verify that the new environment was installed correctly:
```
   conda env list
```

# Package structure:
```
rap-package-template
│   README.md
│
├───bs_code
│   │   create_publication.py
│   │   parameters.py
│   │
│   └───utilities                               - This module contains all the main modules used to create the publication
│       │   charts.py                           - Defines the functions needed to create and export charts to Excel
│       │   csvs.py                             - Defines the functions needed to create and export data to csvs
│       │   dashboards.py                       - Defines the functions needed to create and export data used in dasboards
│       │   data_connections.py                 - Defines the df_from_sql function, used when importing SQL data
│       │   field_definitions.py                - Defines the functions used to abstract new field (column) creation
│       │   helpers.py                          - Contains general functions used throughout the codebase
│       │   import_data.py                      - Contains functions for reading in the required data from .csv files and SQL tables
│       │   logger_config.py                    - The configuration functions for the publication logger
│       │   processing_steps.py                 - Defines the main functions used to manipulate data and produce outputs
│       │   publication_files.py                - Contains functions used to create publication ready outputs and save in relevant folders
│       │   tables.py                           - Contains every output table defined as a function
│       └─  write.py                            - Contains functions needed for writing output to Excel
|   └───sql_code
|       └─  query_assest
│
└───tests
    ├───unittests                           - Unit tests for all Python functions/modules
            │   test_data_connections.py
            │   test_field_definitions.py
            │   test_helpers.py    
            └─  test_processing_steps.py
 
```

# Running the main process

There are two main files that users running the process will need to interact with:

- [parameters.py](bs_code/parameters.py)

- [create_publication.py](bs_code/create_publication.py)


The file parameters.py contains all of the things that we expect to change from one publication
to the next. Indeed, if the output requirements have not changed, then this should be the only file
that needs to be modified. This file specifies the input and output folder locations and file names,
the reporting year, default values used in the pipeline, and other user defined settings.
It also allows the user to control which elements of the report they want to run. Each input in
the parameters file has annotation explaining it's role.

The publication pipeline is run using the top-level script, create_publication.py. 
This script imports and runs all the required functions and from the sub-modules.

# Link to publication
https://digital.nhs.uk/data-and-information/publications/statistical/breast-screening-programme

# Licence
The NHS England Breast Screening Programme National Statistics publication codebase is released under the MIT License.
The documentation is © Crown copyright and available under the terms of the [Open Government 3.0 licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
________________________________________
You may re-use this document/publication (not including logos) free of charge in any format or medium, under the terms of the Open Government Licence v3.0.
Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU;
email: psi@nationalarchives.gsi.gov.uk
