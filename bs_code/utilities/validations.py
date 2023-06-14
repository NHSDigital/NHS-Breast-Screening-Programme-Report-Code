from bs_code.utilities.processing import create_output_ts_validations
from bs_code.utilities.processing import create_output_ts_validations_measure

"""
This module contains all the user defined inputs for each validation output (data).

"""


def get_validations_kc63():
    """
    Establishes the functions (contents) required for each validation output
    that uses KC63 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "National Coverage",
         "write_type": "excel_sheet",
         "contents": [create_validation_coverage_age_national]
         },
        {"name": "Regional Coverage 53_70",
         "write_type": "excel_sheet",
         "contents": [create_validation_coverage_53_70_region]
         },
        {"name": "LA Coverage 53_70",
         "write_type": "excel_sheet",
         "contents": [create_validation_coverage_53_70_la]
         },
        {"name": "National Eligible_Screened",
         "write_type": "excel_sheet",
         "contents": [create_validation_elig_screened_national]
         },
        {"name": "Regions Eligible_Screened",
         "write_type": "excel_sheet",
         "contents": [create_validation_elig_screened_region]
         },
        {"name": "LA Eligible_Screened",
         "write_type": "excel_sheet",
         "contents": [create_validation_elig_screened_la]
         },
        ]

    return all_outputs


def get_validations_kc62():
    """
    Establishes the functions (contents) required for each validation that
    uses KC62 data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "National Counts",
         "write_type": "excel_sheet",
         "contents": [create_validation_invited_screened_total_cancer_national]
         },
        {"name": "Regional Counts",
         "write_type": "excel_sheet",
         "contents": [create_validation_invited_screened_total_cancer_region]
         },
        {"name": "BSU Counts",
         "write_type": "excel_sheet",
         "contents": [create_validation_invited_screened_total_cancer_bsu]
         },
        {"name": "BSU Rate_with_cancer",
         "write_type": "excel_sheet",
         "contents": [create_validation_rate_with_cancer_bsu]
         },
        ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

    measures : list[str]
        Name of measure(s) to be returned. Must be an existing value from the
        measure_column, cannot be a rate/percentage calculated field
        from field_definitions.
        create_output_ts_validations function
    measure : str
        Name of single measure to be added and returned.
        Must exist in field_definitions.
        create_output_ts_validations_measure function
    rows : list[str]
        Variable name(s) that holds the output row content (multiple variables can
        be selected).
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on : list[str]
        Optional list of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some outputs. It may consist of one or more filters of the
        dataframe variables.
        e.g. "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    validations: list[str]
        list of pre-defined validations to include in the output. Must
        exist in processing_steps.add_validation_columns
    ts_years: int
        Defines the number of time series years required in the output.
        Default is 1.

Returns:
-------
    Each function returns a dataframe with the output.

"""


def create_validation_coverage_age_national(df):
    rows = ["Row_Def"]
    measure = "Coverage"
    part = ["1"]
    table_code = None
    sort_on = None
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = None
    validations = ["YoY_change", "Avg_columns", "Avg_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations_measure(df, rows, measure,
                                                part, table_code, sort_on,
                                                filter_condition, row_subgroup,
                                                validations, ts_years)


def create_validation_coverage_53_70_region(df):
    rows = ["Parent_Org_Name"]
    measure = "Coverage"
    part = ["1"]
    table_code = None
    sort_on = ["Parent_Org_Name"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Parent_Org_Name": {"South": ["South East", "South West"]}}
    validations = ["YoY_change", "Avg_columns", "Avg_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations_measure(df, rows, measure,
                                                part, table_code, sort_on,
                                                filter_condition, row_subgroup,
                                                validations, ts_years)


def create_validation_coverage_53_70_la(df):
    rows = ["Parent_Org_Name", "Org_ONSCode", "Org_Name"]
    measure = "Coverage"
    part = ["1"]
    table_code = None
    sort_on = ["Org_Name"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = None
    validations = ["YoY_change", "Avg_columns", "Avg_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations_measure(df, rows, measure,
                                                part, table_code, sort_on,
                                                filter_condition, row_subgroup,
                                                validations, ts_years)


def create_validation_elig_screened_national(df):
    rows = ["Col_Def", "Row_Def"]
    measures = ["Women_resident", "Women_eligible", "Women_screened_less3yrs"]
    part = ["1"]
    table_code = None
    sort_on = ["Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_elig_screened_region(df):
    rows = ["Parent_Org_Name", "Col_Def", "Row_Def"]
    measures = ["Women_resident", "Women_eligible", "Women_screened_less3yrs"]
    part = ["1"]
    table_code = None
    sort_on = ["Parent_Org_Name", "Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_elig_screened_la(df):
    rows = ["Parent_Org_Name", "Org_ONSCode", "Org_Name", "Col_Def", "Row_Def"]
    measures = ["Women_resident", "Women_eligible", "Women_screened_less3yrs"]
    part = ["1"]
    table_code = None
    sort_on = ["Org_Name", "Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_invited_screened_total_cancer_national(df):
    rows = ["Col_Def", "Row_Def"]
    measures = ["Invited", "Screened", "Total_with_cancer"]
    part = ["1", "3"]
    table_code = None
    sort_on = ["Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_invited_screened_total_cancer_region(df):
    rows = ["Parent_Org_Name", "Col_Def", "Row_Def"]
    measures = ["Invited", "Screened", "Total_with_cancer"]
    part = ["1", "3"]
    table_code = None
    sort_on = ["Parent_Org_Name", "Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_invited_screened_total_cancer_bsu(df):
    rows = ["Org_Code", "Org_Name", "Col_Def", "Row_Def"]
    measures = ["Invited", "Screened", "Total_with_cancer"]
    part = ["1", "3"]
    table_code = None
    sort_on = ["Org_Name", "Col_Def", "Row_Def"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = {"Row_Def": {" 53<71":
                                ["53-54", "55-59", "60-64", "65-69", "70"]}}
    validations = ["YoY_percent_change", "Avg_columns", "Avg_percent_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                        filter_condition, row_subgroup,
                                        validations, ts_years)


def create_validation_rate_with_cancer_bsu(df):
    rows = ["Org_Code", "Org_Name"]
    measure = "Rate_with_cancer"
    part = ["1", "3"]
    table_code = None
    sort_on = ["Org_Name"]
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    row_subgroup = None
    validations = ["YoY_change", "Avg_columns", "Avg_change",
                   "YoY_breach", "Avg_breach"]
    ts_years = 9

    return create_output_ts_validations_measure(df, rows, measure,
                                                part, table_code, sort_on,
                                                filter_condition, row_subgroup,
                                                validations, ts_years)
