from bs_code.utilities.processing import create_output_crosstab


"""
This module contains all the user defined inputs for each dashboard output (data).

See the tables.py file for details of each argument.

"""


def get_dashboards_kc63():
    """
    Establishes the functions (contents) required for each dashboard output that
    uses KC63 data, and the arguments needed for the write process.

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
    Establishes the functions (contents) required for each dashboard output that
    uses KC62 data, and the arguments needed for the write process.

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
    dataframe content for each output.

    See the tables.py file for details of each argument.

Returns:
-------
    Each function returns a dataframe with the output.

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
