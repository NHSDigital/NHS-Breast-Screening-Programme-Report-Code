from bs_code.utilities.processing import create_output_crosstab
from bs_code.utilities.processing import create_output_measure

"""
This module contains all the user defined inputs for each chart output (data).

See the tables.py file for details of each argument.

"""


def get_charts_kc63():
    """
    Establishes the functions (contents) required for each chart output
    that uses KC63 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "Coverage_Year",
         "write_type": "excel_static",
         "write_cell": "B4",
         "empty_cols": None,
         "contents": [create_chart_coverage_year]
         },
        {"name": "Coverage_Age",
         "write_type": "excel_static",
         "write_cell": "A4",
         "empty_cols": None,
         "contents": [create_chart_coverage_age]
         },
        {"name": "Coverage_Region",
         "write_type": "excel_static",
         "write_cell": "A4",
         "empty_cols": None,
         "contents": [create_chart_coverage_region]
         },
        {"name": "Coverage_LA",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "empty_cols": None,
         "contents": [create_chart_coverage_la]
         }
        ]

    return all_outputs


def get_charts_kc62():
    """
    Establishes the functions (contents) required for each chart output
    that uses KC62 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "Screened_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_screened_year]
         },
        {"name": "Screened_Age_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_screened_age_year]
         },
        {"name": "Screened_Invite_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_screened_invite_year]
         },
        {"name": "Screened_SelfGP_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_screened_selfgp_year]
         },
        {"name": "Uptake_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_uptake_year]
         },
        {"name": "Uptake_Region",
         "write_type": "excel_static",
         "write_cell": "B3",
         "empty_cols": None,
         "contents": [create_chart_uptake_region]
         },
        {"name": "Uptake_Invite",
         "write_type": "excel_static",
         "write_cell": "B3",
         "empty_cols": None,
         "contents": [create_chart_uptake_invite]
         },
        {"name": "Uptake_Invite_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_uptake_invite_year]
         },
        {"name": "Uptake_BSU",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "empty_cols": None,
         "contents": [create_chart_uptake_bsu]
         },
        {"name": "Uptake_Age",
         "write_type": "excel_static",
         "write_cell": "B3",
         "empty_cols": None,
         "contents": [create_chart_uptake_age]
         },
        {"name": "Cancer_Det_Age_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_cancers_age_year]
         },
        {"name": "Cancer_Det_Type_Year",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_cancers_type_year]
         },
        {"name": "HighRisk_RiskCat",
         "write_type": "excel_static",
         "write_cell": "B5",
         "empty_cols": None,
         "contents": [create_chart_cancers_hr_risk_cat]
         },
        {"name": "HighRisk_Region",
         "write_type": "excel_static",
         "write_cell": "A3",
         "empty_cols": None,
         "contents": [create_chart_cancers_hr_region]
         },
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


def create_chart_coverage_year(df):
    rows = ["CollectionYearRange"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = None
    column_order = ["Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
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
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_coverage_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["53<71", "53-54", "55-59", "60-64", "65-69", "70"]
    column_order = ["Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"53<71": ["53-54", "55-59", "60-64",
                                          "65-69", "70"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_coverage_region(df):
    rows = ["Parent_OrgONSCode", "Parent_Org_Name"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = None
    row_order = ["Grand_total", "E12000001", "E12000002", "E12000003",
                 "E12000004", "E12000005", "E12000006", "E12000007",
                 "E12000008", "E12000009"]
    column_order = ["Coverage"]
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
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_coverage_la(df):
    rows = ["Org_Name"]
    columns = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["Org_Name"]
    row_order = None
    column_order = ["Coverage"]
    column_rename = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
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


def create_chart_screened_year(df):
    rows = ["CollectionYearRange"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["45 and over", "50-70"]
    column_rename = None
    filter_condition = "(Col_Def in['Screened'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"45 and over": ["45-49", "50-52", "53-54", "55-59", "60-64",
                                       "65-69", "70", "71-74", ">=75"],
                       "50-70": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"]}
    include_row_labels = True
    measure_as_rows = False
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_screened_age_year(df):
    rows = ["CollectionYearRange"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["45 and over", "45-49", "50-70", "71-74", ">=75"]
    column_rename = None
    filter_condition = "(Col_Def in['Screened'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"45 and over": ["45-49", "50-52", "53-54", "55-59", "60-64",
                                       "65-69", "70", "71-74", ">=75"],
                       "50-70": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"]}
    include_row_labels = True
    measure_as_rows = False
    ts_years = 6

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_screened_invite_year(df):
    rows = ["CollectionYearRange"]
    columns = "Table_Code"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["A to D", "E to F"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44']) & (Col_Def in['Screened'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"A to D": ["A", "B", "C1", "C2", "D"],
                       "E to F": ["E", "F1", "F2"]}
    include_row_labels = True
    measure_as_rows = False
    ts_years = 6

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_screened_selfgp_year(df):
    rows = ["CollectionYearRange"]
    columns = "Row_Def"
    part = ["1"]
    table_code = ["E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["45-49", "50 to <71", "71-74", ">=75"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44']) & (Col_Def in['Screened'])"
    visible_condition = None
    row_subgroup = None
    column_subgroup = {"50 to <71": ["50-52", "53-54", "55-59", "60-64", "65-69", "70"]}
    include_row_labels = True
    measure_as_rows = False
    ts_years = 11

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_uptake_year(df):
    rows = ["CollectionYearRange"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = None
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
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
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_uptake_region(df):
    rows = ["Parent_Org_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = ["Grand_total", "NEYH", "R1", "R3", "R2", "R4", "R5", "R6",
                 "R7", "S", "R8", "R10"]
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Parent_Org_Code": {"NEYH": ["R1", "R3"],
                                        "S": ["R8", "R10"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_uptake_invite(df):
    rows = ["Table_Code"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["A", "B", "C1", "C2", "D", "A and C1", "A to C2"]
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = None
    row_subgroup = {"Table_Code": {"A and C1": ["A", "C1"],
                    "A to C2": ["A", "B", "C1", "C2"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_chart_uptake_invite_year(df):
    measure_column = "Col_Def"
    measure = "Uptake"
    rows = ["CollectionYearRange"]
    columns = "Table_Code"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = None
    row_order = None
    column_order = ["B to C2", "A"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    subgroup = {"Table_Code": {"B to C2": ["B", "C1", "C2"]}}
    include_row_labels = True
    ts_years = 11

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels, ts_years)


def create_chart_uptake_bsu(df):
    rows = ["Org_Name"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2"]
    sort_on = ["Org_Name"]
    row_order = None
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
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


def create_chart_uptake_age(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = None
    row_order = ["45-49", "50-52", "53-54", "55-59", "60-64", "65-70",
                 "71-74"]
    column_order = ["Uptake"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44','>=75'])"
    visible_condition = None
    row_subgroup = {"Row_Def": {"65-70": ["65-69", "70"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_chart_cancers_age_year(df):
    measure_column = "Col_Def"
    measure = "Rate_with_cancer"
    rows = ["CollectionYearRange"]
    columns = "Row_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["45-49", "50-54", "55-59", "60-64", "65-70", "Over 70"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
    subgroup = {"Row_Def": {"50-54": ["50-52", "53-54"], "65-70": ["65-69", "70"],
                            "Over 70": ["71-74", ">=75"]}}
    include_row_labels = True
    ts_years = 11

    return create_output_measure(df, measure_column, measure, rows, columns,
                                 part, table_code, sort_on, row_order,
                                 column_order, column_rename,
                                 filter_condition, subgroup,
                                 include_row_labels, ts_years)


def create_chart_cancers_type_year(df):
    rows = ["CollectionYearRange"]
    columns = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = None
    row_order = None
    column_order = ["Rate_with_cancer", "Rate_invasive_15mmplus",
                    "Rate_small_invasive", "Rate_non_or_micro_invasive"]
    column_rename = None
    filter_condition = "(Row_Def not in['<=44'])"
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
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)


def create_chart_cancers_hr_risk_cat(df):
    rows = ["Row_Def"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = None
    row_order = ["BRCA 1", "BRCA 2", "Untested BRCA", "CDH1", "PALB2", "PTEN",
                 "STK11", "Other high-risk gene", "Not Tested", "TP53",
                 "A-T Homozygotes", "A-T Heterozygotes",
                 "Supradiaphragmatic radiotherapy (Irradiated <30)",
                 "Multiple Risks"]
    column_order = ["HR_Total_screened"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = {"Row_Def": {"Supradiaphragmatic radiotherapy (Irradiated <30)":
                                ["Radiotherapy Aged 10-19",
                                 "Radiotherapy Aged 20-29",
                                 "Radiotherapy Below age 30"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows)


def create_chart_cancers_hr_region(df):
    rows = ["Parent_Org_Name"]
    columns = "Col_Def"
    part = ["3"]
    table_code = ["U3"]
    sort_on = None
    row_order = ["NEYH", "North East", "Yorkshire and the Humber",
                 "North West", "East Midlands", "West Midlands",
                 "East of England", "London", "South", "South East",
                 "South West"]
    column_order = ["HR_Total_screened"]
    column_rename = None
    filter_condition = None
    visible_condition = None
    row_subgroup = {"Parent_Org_Name": {"NEYH": ["North East",
                                                 "Yorkshire and the Humber"],
                                        "South": ["South East", "South West"]}}
    column_subgroup = None
    include_row_labels = True
    measure_as_rows = False
    ts_years = 2

    return create_output_crosstab(df, rows, columns, part, table_code,
                                  sort_on, row_order, column_order,
                                  column_rename, filter_condition,
                                  visible_condition, row_subgroup,
                                  column_subgroup, include_row_labels,
                                  measure_as_rows, ts_years)
