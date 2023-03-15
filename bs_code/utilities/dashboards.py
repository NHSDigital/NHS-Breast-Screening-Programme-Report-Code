from bs_code.utilities.processing_steps import create_output_crosstab


"""
This module contains all the user defined inputs for each dashboard data output.
The write arguments in get_dashboards_kc63 and get_dashboards_kc62 are defined as:

name : str
    Name of the worksheet to be written to (for Excel) or to be assigned
    as the name of the output file (for csv's).
write_type: str
    Determines the method of writing the output. Valid options are:
    excel_static: Writes data to Excel where the length of the data is
    static (write_cell must be populated).
    excel_variable: Writes data to Excel where the length of the data is
    variable (write_cell must be populated).
    csv: Writes data to a csv file. Will be named as per 'name' input.
write_cell: str
    Identifies the cell location in the Excel worksheet where the data
    will be pasted (top left of data). Not required for write_type = csv.
empty_cols: list[str]
    A list of letters representing any empty (section seperator) excel
    measure_column in the worksheet. Empty column will be inserted into the
    dataframe in these positions. Not required for write_type = csv.
contents: list[str]
    The name of the function that creates the output. If more than one are
    included they will be appended together.

"""


def get_dashboards_kc63():
    """
    Establishes each of the output csv files, and associated processes
    required for each csv that uses KC63 data.
    Add or remove any from the list as required.

    Parameters:
        None
    Returns:
        Filename and function to be run for each csv.

    """
    all_outputs = [
        {"name": "Dashboard_Coverage_Age",
         "write_type": "csv",
         "contents": [create_db_coverage_age,
                      ]},
        {"name": "Dashboard_Coverage",
         "write_type": "csv",
         "contents": [create_db_coverage_la,
                      create_db_coverage_region,
                      create_db_coverage_national
                      ]}
        ]

    return all_outputs


def get_dashboards_kc62():
    """
    Establishes each of the output csv files, and associated processes
    required for each csv that uses KC62 data.
    Add or remove any from the list as required.

    Parameters:
        None
    Returns:
        Filename and function to be run for each csv.

    """
    all_outputs = [
        {"name": "Dashboard_Uptake_Age",
         "write_type": "csv",
         "contents": [create_db_uptake_age,
                      ]},
        {"name": "Dashboard_Uptake",
         "write_type": "csv",
         "contents": [create_db_uptake_bsu,
                      create_db_uptake_region,
                      create_db_uptake_national
                      ]},
        {"name": "Dashboard_Internal_BSU",
         "write_type": "csv",
         "contents": [create_db_bsu
                      ]},
        {"name": "Dashboard_Internal_BSU_Flagged",
         "write_type": "csv",
         "contents": [create_db_bsu_flags
                      ]}
        ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

    breakdowns : list[str]
        Variable name(s) that holds the output breakdown content (mutliple
        variables can be selected).
    measure_column : str
        Variable name that holds the measure content (single variable only)
        If set to None then a single aggregated count column will be created.
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on : list[str]
        Optional list of column names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        Note that using this option will mean that totals will be removed
        e.g. for use in org outputs.
        If breakdown_order is not None then this input should be None.
    breakdown_order: list[str]
        Optional list of row content that determines the order data will be
        presented in the output. Allows for full control of row ordering
        (can only include row values that exist in the breakdown column(s)).
        Used for precise user-defined row ordering.
        If sort_on is not None then this input should be None.
    measure_order: list[str]
        list of measure names from measure_column that determines what is
        included and the order they will be presented in the output.
        This can include derived variables as long as they have been added to
        field_definitions.py.
        If set to None then only the grand total for each year in the time
        series will be outputted.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement. Any column set within the 'breakdowns' or
        'column order' parameters can be renamed.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some charts. It may consist of one or more filters of the
        dataframe variables.
    visible_condition : str
        This is an optional condition, as a string.
        This is used to select breakdowns that will not be visible (use 'not in') or
        that will be the only breakdowns visible (use 'in') in the output. This will not
        affect totals / subgroup totals which are added before this condition
        is applied.
        e.g. "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    breakdown_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on breakdown content.
        Contains the breakdown column name, and for each column name another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
        e.g. {"AgeBand": {'53<71': ['53-54', '55-59', '60-64', '65-69', '70']}}
    measure_subgroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on measure content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the 'measure_column' variable) that
        will form the group.
    measure_as_rows: bool
        Set to False for dashboard outputs where the measures are always set as
        column headers.
    ts_years: int
        Defines the number of years required in the output.
        Default is 1 if not included.

Returns:
-------
    Each function returns a dataframe with the output for the dashboard.

"""


def create_db_coverage_age(df):
    breakdowns = ["CollectionYearRange", "Row_Def"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def"]
    breakdown_order = None
    measure_order = ["Women_eligible", "Coverage"]
    column_rename = {"Women_eligible": "Eligible"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = "(Row_Def not in['65-69', '70'])"
    breakdown_subgroup = {"Row_Def": {"53-70": ["53-54", "55-59", "60-64",
                                                "65-69", "70"],
                                      "65-70": ["65-69", "70"]}}
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_uptake_age(df):
    breakdowns = ["CollectionYearRange", "Table_CodeDescription", "Row_Def"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = ["CollectionYearRange", "Row_Def"]
    breakdown_order = None
    measure_order = ["Invited", "Uptake"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44', '>=75'])"
    visible_condition = "(Row_Def not in['65-69', '70'])"
    breakdown_subgroup = {"Row_Def": {"50-70": ["50-52", "53-54", "55-59", "60-64",
                                                "65-69", "70"],
                                      "65-70": ["65-69", "70"]},
                          "Table_CodeDescription":
                              {"First and all routine invitations":
                               ["First invitation for routine screening",
                                "Routine invitation to previous non-attenders",
                                "Routine invitation to previous attenders (Last screen within 5 years)",
                                "Routine invitation to previous attenders (Last screen more than 5 years)"
                                ]}}
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_coverage_la(df):
    breakdowns = ["CollectionYearRange", "Parent_Org_Code", "Parent_Org_Name",
                  "Org_ONSCode", "Org_Name"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    breakdown_order = None
    measure_order = ["Women_eligible", "Coverage"]
    column_rename = {"Women_eligible": "Eligible_53to70",
                     "Coverage": "Coverage_53to70"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70']) & (Org_Type =='LA')"
    visible_condition = None
    breakdown_subgroup = None
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 9

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_coverage_region(df):
    breakdowns = ["CollectionYearRange", "Parent_Org_Code"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    breakdown_order = None
    measure_order = ["Women_eligible", "Coverage"]
    column_rename = {"Women_eligible": "REG_Eligible_53to70",
                     "Coverage": "REG_Coverage_53to70"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70']) & (Org_Type =='LA')"
    visible_condition = None
    breakdown_subgroup = None
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 9

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_coverage_national(df):
    breakdowns = ["CollectionYearRange"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    breakdown_order = None
    measure_order = ["Women_eligible", "Coverage"]
    column_rename = {"Women_eligible": "ENG_Eligible_53to70",
                     "Coverage": "ENG_Coverage_53to70"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70']) & (Org_Type =='LA')"
    visible_condition = None
    breakdown_subgroup = None
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 9

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_uptake_bsu(df):
    breakdowns = ["CollectionYearRange", "Parent_Org_Code", "Parent_Org_Name",
                  "Org_Name", "Table_CodeDescription"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    breakdown_order = None
    measure_order = ["Invited", "Uptake"]
    column_rename = {"Invited": "Invited_50to70",
                     "Uptake": "Uptake_50to70"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    breakdown_subgroup = {"Table_CodeDescription":
                          {"First and all routine invitations":
                           ["First invitation for routine screening",
                            "Routine invitation to previous non-attenders",
                            "Routine invitation to previous attenders (Last screen within 5 years)",
                            "Routine invitation to previous attenders (Last screen more than 5 years)"
                            ]}}
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_uptake_region(df):
    breakdowns = ["CollectionYearRange", "Parent_Org_Code",
                  "Table_CodeDescription"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    breakdown_order = None
    measure_order = ["Invited", "Uptake"]
    column_rename = {"Invited": "REG_Invited_50to70",
                     "Uptake": "REG_Uptake_50to70"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    breakdown_subgroup = {"Table_CodeDescription":
                          {"First and all routine invitations":
                           ["First invitation for routine screening",
                            "Routine invitation to previous non-attenders",
                            "Routine invitation to previous attenders (Last screen within 5 years)",
                            "Routine invitation to previous attenders (Last screen more than 5 years)"
                            ]}}
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_uptake_national(df):
    breakdowns = ["CollectionYearRange", "Table_CodeDescription"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    breakdown_order = None
    measure_order = ["Invited", "Uptake"]
    column_rename = {"Invited": "ENG_Invited_50to70",
                     "Uptake": "ENG_Uptake_50to70"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = None
    breakdown_subgroup = {"Table_CodeDescription":
                          {"First and all routine invitations":
                           ["First invitation for routine screening",
                            "Routine invitation to previous non-attenders",
                            "Routine invitation to previous attenders (Last screen within 5 years)",
                            "Routine invitation to previous attenders (Last screen more than 5 years)"
                            ]}}
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_bsu(df):
    breakdowns = ["CollectionYearRange", "Parent_Org_Name", "Org_Code",
                  "Org_Name", "Table_CodeDescription", "Row_Def", "Col_Def"]
    measure_column = None
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange"]
    breakdown_order = None
    measure_order = None
    column_rename = None
    filter_condition = "(Col_Def in['Invited', 'Screened'])"
    visible_condition = None
    breakdown_subgroup = None
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False
    ts_years = 13

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows, ts_years)


def create_db_bsu_flags(df):
    breakdowns = ["Org_Code", "Org_Name"]
    measure_column = None
    part = None
    table_code = None
    sort_on = ["Org_Code"]
    breakdown_order = None
    measure_order = None
    column_rename = None
    filter_condition = None
    visible_condition = None
    breakdown_subgroup = None
    measure_subgroup = None
    include_breakdown_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, breakdowns, measure_column, part, table_code,
                                  sort_on, breakdown_order, measure_order,
                                  column_rename, filter_condition,
                                  visible_condition, breakdown_subgroup,
                                  measure_subgroup, include_breakdown_labels,
                                  measure_as_rows)
