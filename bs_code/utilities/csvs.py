from bs_code.utilities.processing import create_output_csv_tidy


"""
This module contains all the user defined inputs for each tidy csv output.
The write arguments in get_csvs_KC63 and get_csvs_KC62 are defined as:

name : str
    Name of the output file.
write_type: str
    Determines the method of writing the output.
    All should be set to 'csv' for these outputs.
contents: list[str]
    The name of the function that creates the output. If more than one are
    included they will be appended together.

"""


def get_csvs_kc63():
    """
    Establishes each of the output csv files, and associated processes
    required for each csv that uses KC63 data.
    Add or remove any from the list as required.

    Parameters:
        None
    Returns:
        Filename and function to be run for each csv.

    """
    all_csvs = [
        {"name": "kc63_coverage",
         "write_type": "csv",
         "contents": [create_csv_coverage_national,
                      create_csv_coverage_region,
                      create_csv_coverage_la
                      ]}
        ]

    return all_csvs


def get_csvs_kc62():
    """
    Establishes each of the output csv files, and associated processes
    required for each csv that uses KC62 data.
    Add or remove any from the list as required.

    Parameters:
        None
    Returns:
        Filename and function to be run for each csv.

    """
    all_csvs = [
        {"name": "kc62_invite_screened_uptake",
         "write_type": "csv",
         "contents": [create_csv_uptake_national,
                      create_csv_uptake_self_gp_national,
                      create_csv_uptake_region,
                      create_csv_uptake_bsu,
                      ]},
        {"name": "kc62_referral_outcome",
         "write_type": "csv",
         "contents": [create_csv_referral_national,
                      create_csv_referral_region,
                      create_csv_referral_bsu,
                      ]},
        {"name": "kc62_cancers_detected",
         "write_type": "csv",
         "contents": [create_csv_cancers_national,
                      create_csv_cancers_region,
                      create_csv_cancers_bsu
                      ]},
        {"name": "kc62_diagnostic_outcomes",
         "write_type": "csv",
         "contents": [create_csv_diagnostic_all_national,
                      create_csv_diagnostic_prevalent_national,
                      create_csv_diagnostic_incident_national,
                      create_csv_diagnostic_all_region,
                      create_csv_diagnostic_prevalent_region,
                      create_csv_diagnostic_incident_region,
                      create_csv_diagnostic_all_bsu,
                      create_csv_diagnostic_prevalent_bsu,
                      create_csv_diagnostic_incident_bsu
                      ]}
        ]

    return all_csvs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

    collection: str
        Screening collection source for the output (KC62 or KC63).
    breakdown : list[str]
        Variable name(s) that define the breakdowns to be included in the
        output (multiple variables can be selected).
        Note that the year field is included in the output by default
        so does not need including in this list.
    org_level : str
        Defines the level of organisation that the data will include.
        Valid inputs are 'national', 'regional', 'local'.
    measure_column : str
        Variable name that holds the measure information (e.g. Col_Def).
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on : list[str]
        Optional list of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
    measure_order: list[str]
        List of measure names from measure_column that determines what is
        included and the order they will be presented in the output.
        This can include derived variables as long as they have been added to
        field_definitions.py.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement. Any column set within the 'breakdowns' or
        'measure order' parameters can be renamed.
    filter_condition : str
        This is a non-standard, optional dataframe filter, as a string.
    visible_condition : str
        This is an optional condition, as a string.
        This is used to select rows that will not be visible (use 'not in') or
        that will be the only rows visible (use 'in') in the output. This will not
        affect totals / subgroup totals which are added before this condition
        is applied.
        e.g. "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    breakdown_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
        e.g. {"AgeBand": {'53<71': ['53-54', '55-59', '60-64', '65-69', '70']}}
    ts_years: int
        Defines the number of time series years required in the csv.
        Default is 1.


Returns:
-------
    Each function returns a dataframe with the output for the csv.
"""


def create_csv_coverage_national(df):
    collection = "KC63"
    org_level = "national"
    breakdown = ["Row_Def"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def"]
    measure_order = ["Women_resident", "Women_ineligible", "Women_eligible",
                     "Women_never_screened", "Percent_never_screened",
                     "Women_screened_less3yrs", "Coverage"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<45','>=75'])"
    visible_condition = None
    breakdown_subgroup = {"Row_Def": {"53<71": ["53-54", "55-59", "60-64",
                                                "65-69", "70"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_coverage_region(df):
    collection = "KC63"
    org_level = "regional"
    breakdown = ["Row_Def"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def"]
    measure_order = ["Women_resident", "Women_ineligible", "Women_eligible",
                     "Women_never_screened", "Percent_never_screened",
                     "Women_screened_less3yrs", "Coverage"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    breakdown_subgroup = {"Row_Def": {"53<71": ["53-54", "55-59", "60-64",
                                                "65-69", "70"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_coverage_la(df):
    collection = "KC63"
    org_level = "local"
    breakdown = ["Row_Def"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def"]
    measure_order = ["Women_eligible", "Women_screened_less3yrs", "Coverage"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def in['53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = "(Row_Def not in['53-54', '55-59', '60-64', '65-69', '70'])"
    breakdown_subgroup = {"Row_Def": {"53<71": ["53-54", "55-59", "60-64",
                                                "65-69", "70"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_uptake_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Screened", "Invited", "Uptake"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def not in['65-69', '70', '71-74', '>=75'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "65-70": ["65-69", "70"],
                                      "Over 70": ["71-74", ">=75"]},
                          "Table_Code": {"A and C1": ["A", "C1"],
                                         "A to C2": ["A", "B", "C1", "C2"],
                                         "A to D": ["A", "B", "C1", "C2", "D"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_uptake_self_gp_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Screened"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def not in['65-69', '70', '71-74', '>=75'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "65-70": ["65-69", "70"],
                                      "Over 70": ["71-74", ">=75"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_uptake_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Screened", "Invited", "Uptake"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = "(Row_Def in['50<71'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"A and C1": ["A", "C1"],
                                         "A to C2": ["A", "B", "C1", "C2"],
                                         "A to D": ["A", "B", "C1", "C2", "D"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_uptake_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1"]
    table_code = ["A", "B", "C1", "C2", "D"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Uptake"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def in['50-52', '53-54', '55-59', '60-64', '65-69', '70'])"
    visible_condition = "(Row_Def in['50<71'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"A and C1": ["A", "C1"],
                                         "A to C2": ["A", "B", "C1", "C2"],
                                         "A to D": ["A", "B", "C1", "C2", "D"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_referral_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Initial_referred", "Percent_assessment",
                     "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                     "Percent_STR"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def not in['65-69', '70', '71-74', '>=75'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"],
                                      "65-70": ["65-69", "70"],
                                      "Over 70": ["71-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_referral_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Initial_referred", "Percent_assessment",
                     "Referral_cyt_bio", "Open_biop_total", "Final_STR",
                     "Percent_STR"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def in['50<71', '45 and over']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_referral_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "2"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Percent_assessment"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def in['50<71', '45 and over']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_cancers_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Total_with_cancer", "Invasive_total",
                     "Non_or_micro_invasive", "Cancer_non_microinvasive",
                     "Cancer_microinvasive", "Small_invasive",
                     "Invasive_not_known", "Invasive_lessthan10mm",
                     "Invasive_10mmto15mm", "Invasive_15mmto20mm",
                     "Invasive_20mmto50mm", "Invasive_50mmplus",
                     "Invasive_unknown", "Rate_with_cancer",
                     "Rate_non_or_micro_invasive", "Rate_small_invasive",
                     "Percent_small_invasive"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def not in['65-69', '70', '71-74', '>=75'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"],
                                      "65-70": ["65-69", "70"],
                                      "Over 70": ["71-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_cancers_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Total_with_cancer", "Invasive_total",
                     "Non_or_micro_invasive", "Cancer_non_microinvasive",
                     "Cancer_microinvasive", "Small_invasive",
                     "Invasive_not_known", "Invasive_lessthan10mm",
                     "Invasive_10mmto15mm", "Invasive_15mmto20mm",
                     "Invasive_20mmto50mm", "Invasive_50mmplus",
                     "Invasive_unknown", "Rate_with_cancer",
                     "Rate_non_or_micro_invasive", "Rate_small_invasive",
                     "Percent_small_invasive"]
    filter_condition = "(Row_Def not in['<=44'])"
    column_rename = {"Row_Def": "Age_Band"}
    visible_condition = "(Row_Def in['50<71', '45 and over']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_cancers_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = ["1", "3"]
    table_code = ["A", "B", "C1", "C2", "D", "E", "F1", "F2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Total_with_cancer", "Rate_with_cancer",
                     "Rate_non_or_micro_invasive", "Rate_small_invasive",
                     "Percent_small_invasive"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44'])"
    visible_condition = "(Row_Def in['50<71', '45 and over']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"],
                                      "45-74": ["45-49", "50-52", "53-54",
                                                "55-59", "60-64", "65-69",
                                                "70", "71-74"],
                                      "45 and over": ["45-74", ">=75"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_all_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = None
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Non-op_diag_rate_invasive",
                     "Non-op_diag_rate_non-invasive",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "((Table_Code == 'T' & Part =='4' & Row_Def == '50-70')) | ((Part in ['1','2'] & Row_Def not in['<=44', '45-49', '71-74', '>=75']))"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70",
                                                "50-70"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2",
                                                     "T"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_prevalent_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["A", "B"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A and B'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"A and B": ["A", "B"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_incident_national(df):
    collection = "KC62"
    org_level = "national"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["C1", "C2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    column_rename = {"Row_Def": "Age_Band"}
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['C1 and C2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"C1 and C2": ["C1", "C2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_all_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = None
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Non-op_diag_rate_invasive",
                     "Non-op_diag_rate_non-invasive",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "((Table_Code == 'T' & Part =='4' & Row_Def == '50-70')) | ((Part in ['1','2'] & Row_Def not in['<=44', '45-49', '71-74', '>=75']))"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70",
                                                "50-70"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2",
                                                     "T"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_prevalent_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["A", "B"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A and B'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"A and B": ["A", "B"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_incident_region(df):
    collection = "KC62"
    org_level = "regional"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["C1", "C2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['C1 and C2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"C1 and C2": ["C1", "C2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_all_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = None
    table_code = None
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Non-op_diag_rate_invasive",
                     "Non-op_diag_rate_non-invasive",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "((Table_Code == 'T' & Part =='4' & Row_Def == '50-70')) | ((Part in ['1','2'] & Row_Def not in['<=44', '45-49', '71-74', '>=75']))"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A to F2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70",
                                                "50-70"]},
                          "Table_Code": {"A to F2": ["A", "B", "C1", "C2",
                                                     "D", "E", "F1", "F2",
                                                     "T"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_prevalent_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["A", "B"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['A and B'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"A and B": ["A", "B"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)


def create_csv_diagnostic_incident_bsu(df):
    collection = "KC62"
    org_level = "local"
    breakdown = ["Row_Def", "Table_Code"]
    measure_column = "Col_Def"
    part = part = ["1", "2", "3"]
    table_code = ["C1", "C2"]
    sort_on = ["CollectionYearRange", "Row_Def", "Table_Code"]
    measure_order = ["Rate_benign_biopsy", "Rate_benign_biopsy_warning",
                     "Rate_non_op_diagnosis", "Rate_non_op_diagnosis_warning",
                     "Rate_small_invasive", "Rate_small_invasive_warning",
                     "SDR", "SDR_warning"]
    column_rename = {"Row_Def": "Age_Band"}
    filter_condition = "(Row_Def not in['<=44', '45-49', '71-74', '>=75'])"
    visible_condition = "(Row_Def in['50<71']) & (Table_Code in['C1 and C2'])"
    breakdown_subgroup = {"Row_Def": {"50<71": ["50-52", "53-54", "55-59",
                                                "60-64", "65-69", "70"]},
                          "Table_Code": {"C1 and C2": ["C1", "C2"]}}
    ts_years = 11

    return create_output_csv_tidy(df, collection, org_level, breakdown,
                                  measure_column, part, table_code, sort_on,
                                  measure_order, column_rename,
                                  filter_condition, visible_condition,
                                  breakdown_subgroup, ts_years)
