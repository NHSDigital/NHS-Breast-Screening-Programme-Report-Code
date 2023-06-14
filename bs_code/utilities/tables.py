from bs_code.utilities.processing import create_output_crosstab
from bs_code.utilities.processing import create_output_measure

"""
This module contains all the user defined inputs for each table.
The write arguments in get_kc63_tables and get_kc62_tables are defined as:

name : str
    Excel worksheet where data is to be written.
write_type: str
    Determines the method of writing the output. Valid options for Excel are:
    excel_static: Writes data to Excel where the length of the data is
    static (write_cell must be populated).
    excel_variable: Writes data to Excel where the length of the data is
    variable (write_cell must be populated).
write_cell: str
    Identifies the cell location in the Excel worksheet where the data
    will be pasted (top left of data)
empty_cols: list[str]
    A list of letters representing any empty (section seperator) excel
    columns in the worksheet. Empty columns will be inserted into the
    dataframe in these positions. Default is None.
contents: list[str]
    The name of the function that creates the output. If more than one are
    included they will be appended together.

"""


def get_tables_kc63():
    """
    Establishes the functions (contents) required for each table that
    uses KC63 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "D12",
         "empty_cols": None,
         "contents": [create_table_coverage_year]
         },
        {"name": "Table 2",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["D", "G"],
         "contents": [create_table_coverage_age]
         },
        {"name": "Table 2a",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["D", "G"],
         "contents": [create_table_coverage_region]
         },
        {"name": "Table 11",
         "write_type": "excel_static",
         "write_cell": "E9",
         "empty_cols": ["H"],
         "contents": [create_table_coverage_region_year]
         },
        {"name": "Table 11",
         "write_type": "excel_variable",
         "write_cell": "A21",
         "empty_cols": ["D", "H"],
         "contents": [create_table_coverage_la_year]
         }
        ]

    return all_outputs


def get_tables_kc62():
    """
    Establishes the functions (contents) required for each table that
    uses KC62 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "D18",
         "empty_cols": None,
         "contents": [create_table_invite_screened_year]
         },
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "D20",
         "empty_cols": None,
         "contents": [create_table_uptake_year]
         },
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "D25",
         "empty_cols": None,
         "contents": [create_table_screened_invite_outcome_year_50_70]
         },
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "D31",
         "empty_cols": None,
         "contents": [create_table_screened_invite_outcome_year_45over]
         },
        {"name": "Table 3",
         "write_type": "excel_static",
         "write_cell": "B10",
         "empty_cols": None,
         "contents": [create_table_uptake_region_year]
         },
        {"name": "Table 3a",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["G"],
         "contents": [create_table_uptake_invite_region]
         },
        {"name": "Table 4",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["E"],
         "contents": [create_table_uptake_invite_age_counts]
         },
        {"name": "Table 4",
         "write_type": "excel_static",
         "write_cell": "B21",
         "empty_cols": ["E"],
         "contents": [create_table_uptake_invite_age_percents]
         },
        {"name": "Table 5",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["E"],
         "contents": [create_table_screened_age]
         },
        {"name": "Table 6",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_45over]
         },
        {"name": "Table 6",
         "write_type": "excel_static",
         "write_cell": "B23",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_50_70]
         },
        {"name": "Table 7",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_region_45over]
         },
        {"name": "Table 7",
         "write_type": "excel_static",
         "write_cell": "B27",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_region_50_70]
         },
        {"name": "Table 7a",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_age]
         },
        {"name": "Table 8",
         "write_type": "excel_static",
         "write_cell": "B12",
         "empty_cols": ["C", "G"],
         "contents": [create_table_cancers_45over]
         },
        {"name": "Table 8",
         "write_type": "excel_static",
         "write_cell": "B25",
         "empty_cols": ["C", "G"],
         "contents": [create_table_cancers_50_70]
         },
        {"name": "Table 9",
         "write_type": "excel_static",
         "write_cell": "B12",
         "empty_cols": ["C", "G"],
         "contents": [create_table_cancers_region_45over]
         },
        {"name": "Table 9",
         "write_type": "excel_static",
         "write_cell": "B27",
         "empty_cols": ["C", "G"],
         "contents": [create_table_cancers_region_50_70]
         },
        {"name": "Table 9a",
         "write_type": "excel_static",
         "write_cell": "B10",
         "empty_cols": ["C", "G"],
         "contents": [create_table_cancers_age]
         },
        {"name": "Table 10",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["E"],
         "contents": [create_table_cancers_size_age]
         },
        {"name": "Table 10a",
         "write_type": "excel_static",
         "write_cell": "B11",
         "empty_cols": ["C"],
         "contents": [create_table_cancers_size_invite]
         },
        {"name": "Table 12",
         "write_type": "excel_static",
         "write_cell": "C10",
         "empty_cols": None,
         "contents": [create_table_uptake_region_year]
         },
        {"name": "Table 12",
         "write_type": "excel_variable",
         "write_cell": "A23",
         "empty_cols": None,
         "contents": [create_table_uptake_bsu_year]
         },
        {"name": "Table 13",
         "write_type": "excel_static",
         "write_cell": "C9",
         "empty_cols": ["H"],
         "contents": [create_table_uptake_invite_region]
         },
        {"name": "Table 13",
         "write_type": "excel_variable",
         "write_cell": "A22",
         "empty_cols": ["H"],
         "contents": [create_table_uptake_invite_bsu]
         },
        {"name": "Table 14",
         "write_type": "excel_static",
         "write_cell": "C9",
         "empty_cols": None,
         "contents": [create_table_diagnostic_region]
         },
        {"name": "Table 14",
         "write_type": "excel_variable",
         "write_cell": "A22",
         "empty_cols": None,
         "contents": [create_table_diagnostic_bsu]
         },
        {"name": "Table 15",
         "write_type": "excel_static",
         "write_cell": "C9",
         "empty_cols": None,
         "contents": [create_table_diagnostic_prevalent_region]
         },
        {"name": "Table 15",
         "write_type": "excel_variable",
         "write_cell": "A22",
         "empty_cols": None,
         "contents": [create_table_diagnostic_prevalent_bsu]
         },
        {"name": "Table 15",
         "write_type": "excel_static",
         "write_cell": "M9",
         "empty_cols": None,
         "contents": [create_table_diagnostic_incident_region]
         },
        {"name": "Table 15",
         "write_type": "excel_static",
         "write_cell": "M22",
         "empty_cols": None,
         "contents": [create_table_diagnostic_incident_bsu]
         },
        {"name": "Table 16",
         "write_type": "excel_static",
         "write_cell": "B10",
         "empty_cols": ["C", "F", "I"],
         "contents": [create_table_outcome_highrisk]
         },
        {"name": "Table 17",
         "write_type": "excel_static",
         "write_cell": "C10",
         "empty_cols": None,
         "contents": [create_table_hr_screened_region]
         },
        {"name": "Table 17",
         "write_type": "excel_variable",
         "write_cell": "A23",
         "empty_cols": None,
         "contents": [create_table_hr_screened_bsu]
         },
        ]

    return all_outputs


def get_report_tables_kc62():
    """
    Establishes the functions (contents) required for each report table that
    uses KC62 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "Invited_Age",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": None,
         "contents": [create_report_table_invited_age]
         },
        {"name": "Invited_Type",
         "write_type": "excel_static",
         "write_cell": "B8",
         "empty_cols": ["D"],
         "contents": [create_report_table_invited_type]
         },
        {"name": "Screened_Referred_Invite",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["C", "F", "H"],
         "contents": [create_report_table_screened_referrals]
         },
        {"name": "Assessment_Invite",
         "write_type": "excel_static",
         "write_cell": "B8",
         "empty_cols": ["E"],
         "contents": [create_report_table_referrals_assessment_invite]
         },
        {"name": "STR_Outcomes",
         "write_type": "excel_static",
         "write_cell": "B8",
         "empty_cols": None,
         "contents": [create_report_table_str_outcome]
         },
        {"name": "Cancer_DetRate_Age",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["E"],
         "contents": [create_report_table_cancers_age]
         },
        {"name": "Cancer_DetRate_Age_Invite",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": None,
         "contents": [create_report_table_cancers_age_invite_rates]
         },
        {"name": "Cancer_DetRate_Age_Invite",
         "write_type": "excel_static",
         "write_cell": "K9",
         "empty_cols": None,
         "contents": [create_report_table_cancers_age_invite_counts]
         },
        {"name": "Cancer_Type_Size",
         "write_type": "excel_static",
         "write_cell": "B8",
         "empty_cols": ["D"],
         "contents": [create_report_table_cancer_type_size]
         },
        {"name": "Cancer_Type_Invite",
         "write_type": "excel_static",
         "write_cell": "B9",
         "empty_cols": ["D"],
         "contents": [create_report_table_cancer_type_invite]
         },
        {"name": "InvCancer_Size",
         "write_type": "excel_static",
         "write_cell": "B8",
         "empty_cols": None,
         "contents": [create_report_table_invasive_cancer_size]
         },
        {"name": "HR_Cat_CancersDectected ",
         "write_type": "excel_static",
         "write_cell": "B10",
         "empty_cols": None,
         "contents": [create_report_table_hr_cancer_detected]
         },
        ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

    measure_column : str
        Single variable name that holds the measure numerator and denominator
        information (e.g. Col_Def).
        Only applicable for the create_output_measure function
    measure : str
        Name of single measure to be returned. Must be a value from the
        measure_column or a calculated field from field_definitions.
    rows : list[str]
        Variable name(s) that holds the output row content (mutliple variables can
        be selected).
    columns : str
        Variable name that holds the output column content (single variable only)
        If set to None then output will be in a list format (based on rows
        content) without counts.
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on : list[str]
        Optional list of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        Note that using this option will mean that totals will be removed
        e.g. for use in org outputs.
        If row_order is not None then this input should be None.
    row_order: list[str]
        Optional list of row content that determines the order data will be
        presented in the output. Allows for full control of row ordering
        (can only include row values that exist in the collection).
        Used where for precise user-defined row ordering.
        If sort_on is not None then this input should be None.
    column_order: list[str]
        List of content from the 'columns' variable that determines what is
        included and the order they will be presented in the output.
        This can include derived variables as long as they have been added to
        field_definitions.py.
        If set to None then only the grand total of columns for each year
        will be outputted. If columns is also set to None then the
        output will be a list (based on rows content) without counts.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement. Any column set within the 'rows' or
        'column order' parameters can be renamed.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some outputs. It may consist of one or more filters of the
        dataframe variables.
    visible_condition : str
        This is an optional condition, as a string.
        This is used to select rows that will not be visible (use 'not in') or
        that will be the only rows visible (use 'in') in the output. This will not
        affect totals / subgroup totals which are added before this condition
        is applied.
        e.g. "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
        e.g. {"AgeBand": {'53<71': ['53-54', '55-59', '60-64', '65-69', '70']}}
        Not applicable for the create_output_measure function.
    column_subgroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on column content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the 'columns' variable) that
        will form the group.
        Not applicable for the create_output_measure function.
    subgroup: dict(dict(str, list))
        As per row_subgroup except can be applied to variables that have been
        set as either the rows or column content.
        Only applicable for the create_output_measure function.
    include_row_labels: bol
        Determines if the row labels will be included in the output.
    measure_as_rows: bool
        Indicates if there are measures to be added as rows (can only be applied
        to the first variable held in the 'rows' input list).
        Not applicable for the create_output_measure function.
    ts_years: int
        Defines the number of time series years required in the output.
        Default is 1.

Returns:
-------
    Each function returns a dataframe with the output.

"""


def create_table_coverage_year(df):
    rows = ["Col_Def"]
    columns = "CollectionYearRange"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["Women_eligible", "Women_screened_less3yrs", "Coverage"]
    column_order = None
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_table_invite_screened_year(df):
    rows = ["Col_Def"]
    columns = "CollectionYearRange"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = ["Invited", "Screened"]
    column_order = None
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_table_uptake_year(df):
    rows = ["Col_Def"]
    columns = "CollectionYearRange"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = ["Uptake"]
    column_order = None
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_table_screened_invite_outcome_year_50_70(df):
    rows = ["Col_Def"]
    columns = "CollectionYearRange"
    part = ["1", "2", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Invited", "Screened", "Initial_referred",
                 "Total_with_cancer", "Rate_with_cancer"]
    column_order = None
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_table_screened_invite_outcome_year_45over(df):
    rows = ["Col_Def"]
    columns = "CollectionYearRange"
    part = ["1", "2", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Invited", "Screened", "Initial_referred",
                 "Total_with_cancer", "Rate_with_cancer"]
    column_order = None
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_table_coverage_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["50-74", "65-70", "53<71", "45-49", "50-52", "53-54", "55-59",
                 "60-64", "65-69", "70", "71-74"]
    column_order = ["Women_resident", "Women_ineligible",
                    "Women_never_screened", "Percent_never_screened",
                    "Women_screened_less3yrs", "Coverage"]
    column_rename = None
    filter_condition = "(Row_Def not in['<45','>=75'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"50-52": ["50", "51-52"],
                                "71-74": ["71-73", "74"],
                                "50-74": ["50", "51-52", "53-54", "55-59",
                                          "60-64", "65-69", "70", "71-73", "74"],
                                "65-70": ["65-69", "70"],
                                "53<71": ["53-54", "55-59", "60-64", "65-69",
                                          "70"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_coverage_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["Grand_total", "A", "D", "B", "E", "F", "G", "H", "S", "J", "K"]
    column_order = ["Women_resident", "Women_ineligible",
                    "Women_never_screened", "Percent_never_screened",
                    "Women_screened_less3yrs", "Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"S": ["J", "K"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_uptake_region_year(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                                        "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_table_uptake_invite_region(df):
    measure_column = "Col_Def"
    measure = "Uptake"
    rows = ["Parent_Org_Code"]
    columns = "Table_Code"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["A", "B", "C1", "C2", "D", "A and C1", "A to C2"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                                    "S": ["R8", "R10"]},
                "Table_Code": {"A and C1": ["A", "C1"],
                               "A to C2": ["A", "B", "C1", "C2"]}}
    include_row_labels = False

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels)


def create_table_uptake_invite_age_counts(df):
    rows = ["Table_Code"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["A to C2", "Grand_total", "A", "B", "C1", "C2", "D"]
    column_order = ["Grand_total", "45-74", "50<71", "45-49", "50-52", "53-54",
                    "55-59", "60-64", "65-70", "Over 70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44']) & (Col_Def in['Invited'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"A to C2": ["A", "B", "C1", "C2"]}}
    column_subgroup = {"65-70": ["65-69", "70"],
                       "Over 70": ["71-74", ">=75"],
                       "45-74": ["45-49", "50-52", "53-54", "55-59", "60-64",
                                 "65-69", "70", "71-74"],
                       "50<71": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"]}
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_uptake_invite_age_percents(df):
    measure_column = "Col_Def"
    measure = "Uptake"
    rows = ["Table_Code"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["A to C2", "Grand_total", "A", "B", "C1", "C2", "D"]
    column_order = ["Grand_total", "45-74", "50<71", "45-49", "50-52", "53-54",
                    "55-59", "60-64", "65-70", "Over 70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    subgroup = {"Table_Code": {"A to C2": ["A", "B", "C1", "C2"]},
                "Row_Def": {"65-70": ["65-69", "70"],
                            "Over 70": ["71-74", ">=75"],
                            "45-74": ["45-49", "50-52", "53-54", "55-59",
                                      "60-64", "65-69", "70", "71-74"],
                            "50<71": ["50-52", "53-54", "55-59",
                                      "60-64", "65-69", "70"]}}
    include_row_labels = False

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels)


def create_table_screened_age(df):
    rows = ["Table_Code"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    column_order = ["Grand_total", "45-74", "50<71", "45-49", "50-52", "53-54",
                    "55-59", "60-64", "65-70", "Over 70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44']) & (Col_Def in['Screened'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"65-70": ["65-69", "70"],
                       "Over 70": ["71-74", ">=75"],
                       "45-74": ["45-49", "50-52", "53-54", "55-59", "60-64",
                                 "65-69", "70", "71-74"],
                       "50<71": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"]}
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_45over(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment",
                    "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                    "Percent_STR"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_50_70(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment",
                    "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                    "Percent_STR"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_region_45over(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "North East, Yorkshire and the Humber", "R1",
                 "R3", "R2", "R4", "R5", "R6", "R7", "South", "R8", "R10"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment",
                    "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                    "Percent_STR"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"North East, Yorkshire and the Humber":
                                        ["R1", "R3"],
                                        "South": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_region_50_70(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "North East, Yorkshire and the Humber", "R1",
                 "R3", "R2", "R4", "R5", "R6", "R7", "South", "R8", "R10"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment",
                    "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                    "Percent_STR"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"North East, Yorkshire and the Humber":
                                        ["R1", "R3"],
                                        "South": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "45-74", "50<71", "45-49", "50-52", "53-54",
                 "55-59", "60-64", "65-70", "Over 70"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment",
                    "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                    "Percent_STR"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"65-70": ["65-69", "70"],
                                "Over 70": ["71-74", ">=75"],
                                "45-74": ["45-49", "50-52", "53-54", "55-59",
                                          "60-64", "65-69", "70", "71-74"],
                                "50<71": ["50-52", "53-54", "55-59", "60-64",
                                          "65-69", "70"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_45over(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "3"]
    sort_on = None
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    column_order = ["Screened", "Total_with_cancer", "Non_or_micro_invasive",
                    "Small_invasive", "Rate_with_cancer",
                    "Rate_non_or_micro_invasive", "Rate_small_invasive"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_50_70(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    column_order = ["Screened", "Total_with_cancer", "Non_or_micro_invasive",
                    "Small_invasive", "Rate_with_cancer",
                    "Rate_non_or_micro_invasive", "Rate_small_invasive"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_region_45over(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "North East, Yorkshire and the Humber", "R1",
                 "R3", "R2", "R4", "R5", "R6", "R7", "South", "R8", "R10"]
    column_order = ["Screened", "Total_with_cancer", "Non_or_micro_invasive",
                    "Small_invasive", "Rate_with_cancer",
                    "Rate_non_or_micro_invasive", "Rate_small_invasive"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"North East, Yorkshire and the Humber":
                                        ["R1", "R3"],
                                        "South": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_region_50_70(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "North East, Yorkshire and the Humber", "R1",
                 "R3", "R2", "R4", "R5", "R6", "R7", "South", "R8", "R10"]
    column_order = ["Screened", "Total_with_cancer", "Non_or_micro_invasive",
                    "Small_invasive", "Rate_with_cancer",
                    "Rate_non_or_micro_invasive", "Rate_small_invasive"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"North East, Yorkshire and the Humber":
                                        ["R1", "R3"],
                                        "South": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "45-74", "50<71", "45-49", "50-52", "53-54",
                 "55-59", "60-64", "65-70", "Over 70"]
    column_order = ["Screened", "Total_with_cancer", "Non_or_micro_invasive",
                    "Small_invasive", "Rate_with_cancer",
                    "Rate_non_or_micro_invasive", "Rate_small_invasive"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"65-70": ["65-69", "70"],
                                "Over 70": ["71-74", ">=75"],
                                "45-74": ["45-49", "50-52", "53-54", "55-59",
                                          "60-64", "65-69", "70", "71-74"],
                                "50<71": ["50-52", "53-54", "55-59", "60-64",
                                          "65-69", "70"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_size_age(df):
    rows = ["Col_Def"]
    columns = "Row_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Total_with_cancer", "Invasive_not_known",
                 "Cancer_non_microinvasive", "Cancer_microinvasive",
                 "Invasive_total", "Small_invasive",
                 "Rate_small_invasive", "Percent_small_invasive",
                 "Invasive_lessthan10mm", "Invasive_10mmto15mm",
                 "Invasive_15mmto20mm", "Invasive_20mmto50mm",
                 "Invasive_50mmplus", "Invasive_unknown"]
    column_order = ["Grand_total", "45-74", "50<71", "45-49", "50-54",
                    "55-59", "60-64", "65-70", "Over 70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"65-70": ["65-69", "70"],
                       "Over 70": ["71-74", ">=75"],
                       "45-74": ["45-49", "50-52", "53-54", "55-59", "60-64",
                                 "65-69", "70", "71-74"],
                       "50<71": ["50-52", "53-54", "55-59", "60-64", "65-69",
                                 "70"],
                       "50-54": ["50-52", "53-54"]}
    include_row_labels = False
    measure_as_rows = True

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_cancers_size_invite(df):
    rows = ["Col_Def"]
    columns = "Table_Code"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Total_with_cancer", "Invasive_not_known",
                 "Cancer_non_microinvasive", "Cancer_microinvasive",
                 "Invasive_total", "Small_invasive",
                 "Rate_small_invasive", "Percent_small_invasive",
                 "Invasive_lessthan10mm", "Invasive_10mmto15mm",
                 "Invasive_15mmto20mm", "Invasive_20mmto50mm",
                 "Invasive_50mmplus", "Invasive_unknown"]
    column_order = ["Grand_total", "A to D", "A", "B", "C1", "C2", "D"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"A to D": ["A", "B", "C1", "C2", "D"]}
    include_row_labels = False
    measure_as_rows = True

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_coverage_region_year(df):
    rows = ["Parent_OrgONSCode"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["Grand_total", "E12000001", "E12000002", "E12000003",
                 "E12000004", "E12000005", "E12000006", "E12000007", "S",
                 "E12000008", "E12000009"]
    column_order = ["Women_eligible", "Women_screened_less3yrs",
                    "Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Parent_OrgONSCode": {"S": ["E12000008", "E12000009"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_table_coverage_la_year(df):
    rows = ["Org_ONSCode", "Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["Parent_OrgONSCode", "Org_Name"]
    row_order = None
    column_order = ["Women_eligible", "Women_screened_less3yrs", "Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_table_uptake_bsu_year(df):
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_table_uptake_invite_bsu(df):
    measure_column = "Col_Def"
    measure = "Uptake"
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Table_Code"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["A", "B", "C1", "C2", "D", "A and C1", "A to C2"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    subgroup = {"Table_Code": {"A and C1": ["A", "C1"],
                               "A to C2": ["A", "B", "C1", "C2"]}}
    include_row_labels = True

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels)


def create_table_diagnostic_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = None
    table_code = None
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["Screened", "Rate_benign_biopsy",
                    "Rate_benign_biopsy_warning", "Non-op_diag_rate_invasive",
                    "Non-op_diag_rate_non-invasive", "Rate_non_op_diagnosis",
                    "Rate_non_op_diagnosis_warning", "Percent_assessment",
                    "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "((Table_Code == 'T' & Part =='4' & Row_Def == '50-70')) | ((Part in ['1','2'] & Row_Def not in['<=44', '45-49', '71-74', '>=75']))"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                                        "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_diagnostic_bsu(df):
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = None
    table_code = None
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["Screened", "Rate_benign_biopsy",
                    "Rate_benign_biopsy_warning", "Non-op_diag_rate_invasive",
                    "Non-op_diag_rate_non-invasive", "Rate_non_op_diagnosis",
                    "Rate_non_op_diagnosis_warning", "Percent_assessment",
                    "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "((Table_Code == 'T' & Part =='4' & Row_Def == '50-70')) | ((Part in ['1','2'] & Row_Def not in['<=44', '45-49', '71-74', '>=75']))"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_diagnostic_prevalent_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "2", "3"]
    table_code = ["A", "B"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                    "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                    "Rate_small_invasive", "Rate_small_invasive_warning",
                    "SDR", "SDR_warning",
                    "Percent_assessment", "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                    "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_diagnostic_prevalent_bsu(df):
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["1", "2", "3"]
    table_code = ["A", "B"]
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                    "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                    "Rate_small_invasive", "Rate_small_invasive_warning",
                    "SDR", "SDR_warning",
                    "Percent_assessment", "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_diagnostic_incident_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1", "2", "3"]
    table_code = ["C1", "C2"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                    "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                    "Rate_small_invasive", "Rate_small_invasive_warning",
                    "SDR", "SDR_warning",
                    "Percent_assessment", "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                    "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_diagnostic_incident_bsu(df):
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["1", "2", "3"]
    table_code = ["C1", "C2"]
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                    "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                    "Rate_small_invasive", "Rate_small_invasive_warning",
                    "SDR", "SDR_warning",
                    "Percent_assessment", "Percent_assessment_warning"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_report_table_invited_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["Grand_total", "45-74", "45-49", "50-70", "71-74"]
    column_order = ["Invited"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {'45-74': ['45-49', '50-52', '53-54', '55-59',
                                          '60-64', '65-69', '70', '71-74'],
                                '50-70': ['50-52', '53-54', '55-59', '60-64',
                                          '65-69', '70']}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_report_table_invited_type(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["Grand_total", "A", "B", "C1", "C2", "D"]
    column_order = ['Invited', 'Invited_of_total']
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_report_table_screened_referrals(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Screened", "Initial_referred", "Percent_assessment"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_report_table_referrals_assessment_invite(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Initial_referred", "Referral_cyt_bio",
                    "Percent_cyt_biop_referrals", "Open_biop_total",
                    "Percent_open_biop_referrals"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_report_table_str_outcome(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Initial_referred", "Final_STR", "Percent_STR_referrals"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_report_table_cancers_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "45-49", "50-70", "71-74", ">=75"]
    column_order = ["Screened", "Total_with_cancer", "Rate_with_cancer"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"50-70": ["50-52", "53-54", "55-59", "60-64",
                                          "65-69", "70"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_report_table_cancers_age_invite_rates(df):
    measure_column = "Col_Def"
    measure = "Rate_with_cancer"
    rows = ["Table_Code"]
    columns = "Row_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Grand_total", "50-70", "45-49", "50-54", "55-59", "60-64",
                    "65-70", "Over-70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    subgroup = {"Table_Code": {"AB": ["A", "B"],
                               "C1C2": ["C1", "C2"]},
                "Row_Def": {"50-70": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"],
                            "50-54": ["50-52", "53-54"],
                            "65-70": ["65-69", "70"],
                            "Over-70": ["71-74", ">=75"]}}
    include_row_labels = False

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels)


def create_report_table_cancers_age_invite_counts(df):
    rows = ["Table_Code"]
    columns = "Row_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Grand_total", "50-70", "45-49", "50-54", "55-59", "60-64",
                    "65-70", "Over-70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'] & Col_Def ==['Screened'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = {"50-70": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"],
                       "50-54": ["50-52", "53-54"],
                       "65-70": ["65-69", "70"],
                       "Over-70": ["71-74", ">=75"]}
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_report_table_cancer_type_size(df):
    rows = ["Col_Def"]
    columns = None
    part = ["3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "Invasive_not_known", "Non_or_micro_invasive",
                 "Total_invasive", "Small_invasive", "Invasive_15mmplus",
                 "Invasive_unknown"]
    column_order = ["Value", "Value_of_total"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'] & Col_Def not in['Total_with_cancer','Invasive_total','Invasive_lessthan10mm','Invasive_10mmto15mm','Invasive_15mmto20mm','Invasive_20mmto50mm','Invasive_50mmplus','Cancer_microinvasive','Cancer_non_microinvasive'])"
    visible_condition = None
    row_subgroup = {"Col_Def": {"Total_invasive": ["Small_invasive",
                                                   "Invasive_15mmplus",
                                                   "Invasive_unknown"]
                                }}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = True
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_report_table_cancer_type_invite(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Total_with_cancer", "Percent_cancer_non_or_micro_invasive",
                    "Percent_cancer_invasive_total", "Percent_cancer_small_invasive",
                    "Percent_cancer_invasive_15mmplus"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_report_table_invasive_cancer_size(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = ["Grand_total", "AB", "A", "B", "C1C2", "C1", "C2", "D", "E",
                 "F1", "F2"]
    column_order = ["Invasive_total", "Percent_small_invasive",
                    "Percent_invasive_15mmplus", "Percent_invasive_unknown"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"AB": ["A", "B"],
                                   "C1C2": ["C1", "C2"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_outcome_highrisk(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = None
    row_order = ["Grand_total", "Genetic/familial risk", "BRCA 1", "BRCA 2",
                 "Untested BRCA", "CDH1", "PALB2", "PTEN", "STK11",
                 "Other high-risk gene", "Not Tested", "TP53",
                 "A-T Homozygotes", "A-T Heterozygotes",
                 "Supradiaphragmatic radiotherapy (Irradiated <30)",
                 "Radiotherapy Aged 10-19", "Radiotherapy Aged 20-29",
                 "Radiotherapy Below age 30", "Multiple Risks"]
    column_order = ["HR_Total_screened", "HR_Total_referred",
                    "Percent_hr_referred_assess",
                    "HR_Total_women_with_cancer", "Rate_hr_cancer_detected",
                    "HR_Total_invasive_cancers", "Rate_hr_invasive_cancers"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = {"Row_Def": {"Genetic/familial risk":
                                ["BRCA 1", "BRCA 2", "Untested BRCA", "CDH1",
                                 "PALB2", "PTEN", "STK11",
                                 "Other high-risk gene", "Not Tested",
                                 "TP53", "A-T Heterozygotes", "A-T Homozygotes"],
                                "Supradiaphragmatic radiotherapy (Irradiated <30)":
                                    ["Radiotherapy Aged 10-19",
                                     "Radiotherapy Aged 20-29",
                                     "Radiotherapy Below age 30"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_table_hr_screened_bsu(df):
    rows = ["Org_Name", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = ["Parent_Org_Order", "Org_Name"]
    row_order = None
    column_order = ["HR_Total_screened"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = None
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_table_hr_screened_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5",
                 "R6", "R7", "S", "R8", "R10"]
    column_order = ["HR_Total_screened"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                                        "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup,
                                  include_row_labels, measure_as_rows,
                                  ts_years)


def create_report_table_hr_cancer_detected(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = None
    row_order = ["BRCA 1", "BRCA 2", "Not Tested",
                 "Supradiaphragmatic radiotherapy (Irradiated <30)"]
    column_order = ["Rate_hr_cancer_detected", "Rate_hr_invasive_cancers"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = {"Row_Def": {"Supradiaphragmatic radiotherapy (Irradiated <30)":
                                ["Radiotherapy Aged 10-19",
                                 "Radiotherapy Aged 20-29",
                                 "Radiotherapy Below age 30"]}}
    column_subgroup = None
    include_row_labels = False
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)
