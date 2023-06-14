# Set the parameters for the project
import pathlib

# Sets the file paths for the project
BASE_DIR = pathlib.Path(r"BaseDirectory")
INPUT_DIR = BASE_DIR / "Inputs"
OUTPUT_DIR = BASE_DIR / "Outputs"
MASTER_DIR = OUTPUT_DIR / "MasterFiles"
PUB_DIR = OUTPUT_DIR / "PublicationFiles"
TAB_DIR = PUB_DIR / "DataTables"
CHART_DIR = PUB_DIR / "Charts"
CSV_DIR = PUB_DIR / "CSVs"
REPORT_TAB_DIR = PUB_DIR / "ReportTables"
DASHBOARD_DIR = OUTPUT_DIR / "Dashboard"
VALIDATION_DIR = OUTPUT_DIR / "Validations"
LOG_DIR = OUTPUT_DIR / "Logs"

# Set the locations/filenames of the validation files
VALIDATIONS_OUTPUT_KC63 = VALIDATION_DIR / "breast_screening_kc63_validations.xlsx"
VALIDATIONS_OUTPUT_KC62 = VALIDATION_DIR / "breast_screening_kc62_validations.xlsx"

# Set the locations/filenames of the master files
TABLE_TEMPLATE = MASTER_DIR / "breast_screening_datatables_master.xlsx"
CHART_TEMPLATE = MASTER_DIR / "breast_screening_charts_master.xlsx"
REPORT_TABLES_TEMPLATE = MASTER_DIR / "breast_screening_reporttables_master.xlsx"
# Set the location/filename that contains the organisation table footnote refs.
REF_FOOTNOTES = INPUT_DIR / "breast_screening_footnote_refs.csv"
# Set the location/filename that contains the SDR reference data
SDR_MULTIPLIER = INPUT_DIR / "breast_screening_sdr.csv"
# Set the location that contains the necessary updates to LAs
LA_UPDATES = pathlib.Path(r"ReferenceDataDirectory\CANS_LA_REGION.csv")

# Set the data asset sql database properties
SERVER = "SERVER"
DATABASE = "DATABASE"
TABLE = "TABLE"
TABLE_KC63 = "TABLE2"

# Set the current reporting year (yyyy-yy)
YEAR = "2021-22"

# Sets which outputs should be run as part of the create_publication process
# (True or False)
VALIDATIONS_KC63 = False  # Validations derived from KC63 data
VALIDATIONS_KC62 = False  # Validations derived from KC62 data
TABLES_KC63 = False  # Tables derived from KC63 data
CHARTS_KC63 = False  # Charts derived from KC63 data
CSVS_KC63 = False  # Csvs derived from KC623data
TABLES_KC62 = False  # Tables derived from KC62 data
CHARTS_KC62 = False  # Charts derived from KC62 data
CSVS_KC62 = False  # Csvs derived from KC62 data
REPORT_TABLES_KC62 = False  # Report tables derived from KC62 data
DASHBOARDS = False  # Dashboard output derived from KC62 and KC63 data
# Set whether the final publication outputs should be written as part of the pipeline
RUN_PUBLICATION_OUTPUTS = False
# Worksheets to be removed from final publication file
TABLES_REMOVE = ["Cross Checks", "Org Total Checks"]


# Sets the number of years of KC63 data to be imported (number >=1)
TS_YEARS_KC63 = 13
# Sets the number of years of KC62 data to be imported (number >=1)
TS_YEARS_KC62 = 13
# Set the symbol to be used for not applicable (null) values in the outputs
NOT_APPLICABLE = "z"
# Set the symbol/text to be used for not included values in the csv outputs
CSV_NOT_INC = "not included"
# Set the symbol/text to be used for low numerator warnings
LOW_NUMERATOR = "!"

# Set the time series validation conditions
YOY_TO_YEAR = "2021-22"
YOY_FROM_YEAR = "2020-21"
ROLLING_AVG_YEARS =    # Interger value representing number of years
YOY_BREACH_KC63 =    # Integer value indicating % change to flag
YOY_BREACH_KC62 =    # Integer value indicating % change to flag
AVG_BREACH_KC63 =    # Integer value indicating % change to flag
AVG_BREACH_KC62 =    # Integer value indicating % change to flag
YOY_COV_BREACH_KC63 =    # Integer value representing % point change to flag
AVG_COV_BREACH_KC63 =    # Integer value representing % point change to flag
YOY_RATE_BREACH_KC62 =    # Integer value indicating % change to flag
AVG_RATE_BREACH_KC62 =    # Integer value indicating % change to flag


# Small LAs to combine with larger LAs for KC63
# Reassigns City of London LA E09000001 to Hackney LA E09000012
# Reassigns Isles of Scilly LA E06000053 to Cornwall LA E06000052
ORG_UPDATE_KC63 = {"Org_ONSCode": ["E09000001",
                                   "E06000053"],
                   "Org_ONSCode_New": ["E09000012",
                                       "E06000052"],
                   "Org_Name": ["City of London",
                                "Isles of Scilly"],
                   "Org_Name_New": ["Hackney",
                                    "Cornwall"]
                   }

# Dictionary containing KC63 org names (LAs) that need updating for time series data
# This is just to account for where pre 2015-16 LA names were upper case,
# but need to be camel case for merging with small LA's.
ORG_NAME_UPDATE_KC63 = {"CORNWALL": "Cornwall",
                        "HACKNEY": "Hackney",
                        }

# Dictionary containing the KC62 region codes that need updating for time series data
REGION_UPDATE_KC62 = {"Q30": "R1",
                      "Q31": "R2",
                      "Q32": "R3",
                      "Q33": "R4",
                      "Q34": "R5",
                      "Q35": "R6",
                      "Q36": "R7",
                      "Q37": "R8",
                      "Q38": "R8",
                      "Q39": "R10",
                      "R9": "R8",
                      }

# Dictionary containing the KC62 region names that need updating for time series data
REGION_NAME_UPDATE_KC62 = {"South Central": "South East",
                           "South East Coast": "South East",
                           }

# Dictionary containing KC62 org names (BSUs) that need updating for time series data
ORG_NAME_UPDATE_KC62 = {"Isle Of Wight": "Isle of Wight",
                        "Wigan": "South Lancashire",
                        "Barking, Havering, Redbridge & Brentwood":
                            "Outer North East London",
                        "North & Eastern Devon": "North & East Devon",
                        "Wirral and Chester": "Wirral & Chester",
                        "Basingstoke": "North & Mid Hampshire",
                        }

# Dictionary that defines the region order that KC62 BSU data will be
# presented in the tables
REGION_ORDER_KC62 = {"R1": 1,
                     "R2": 3,
                     "R3": 2,
                     "R4": 4,
                     "R5": 5,
                     "R6": 6,
                     "R7": 7,
                     "R8": 8,
                     "R10": 9,
                     }

# Dictionary that defines the region order that KC63 LA data will be
# presented in the tables
REGION_ORDER_KC63 = {"A": 1,
                     "B": 3,
                     "D": 2,
                     "E": 4,
                     "F": 5,
                     "G": 6,
                     "H": 7,
                     "J": 8,
                     "K": 9,
                     }


# Dictionary containing the BSU flag name and the BSU's it applies to for the
# internal dashboard output. Additional BSU flags can be added if required.
BSU_FLAGGED = {"Flag4749screeningBSU": ["AGA", "DCB", "DGY", "DKL",
                                        "DNF", "DPT", "DSU", "DSW", "LED"]}
