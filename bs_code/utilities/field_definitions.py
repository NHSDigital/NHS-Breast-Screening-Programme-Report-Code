import bs_code.parameters as param
import bs_code.utilities.helpers as helpers
import pandas as pd
import numpy as np
import logging


def add_measures_counts(df, collection,
                        counts_column="Value",
                        measure_column="Col_Def"):
    """
    Checks which collection is being run and applies any additional aggregated
    counts used in reporting to the measure column (Col_Def). These are applied
    to the dataframe directly after import so they can be used throughout the
    pipeline.
    Parameters
    ----------
    df : pandas.DataFrame
    collection: str
        Breast Screening collection being processed
    counts_column_content: str
        Name of column which contains the aggregated counts
    measure_column_content: str
        Name of column which contains the measure information

    Returns
    -------
    pandas.DataFrame
        df with required counts added to the measure column.
    """
    logging.info("Adding calculated counts to the dataframe")

    # Establish the df column names and create an index with all column names
    # except the column that contains the counts (ready for transpose/unstack)
    column_names = list(df.columns)
    column_names.remove(counts_column)
    df.set_index(column_names, inplace=True)
    # Transpose the measure column into columns (one per value in measure column)
    df = df.unstack(measure_column)
    df.columns = df.columns.droplevel(0)
    # Replace nulls in measure column with 0s
    df = df.fillna(0)

    # Add KC63 measures to the columns
    if collection == "KC63":
        df = women_eligible(df)
        df = women_never_screened(df)

    # Add KC62 measures to the columns
    if collection == "KC62":
        df = small_invasive(df)
        df = invasive_15mmplus(df)
        df = non_or_micro_invasive(df)
        df = benign_biopsy(df)
        df = cancers_diagnosed(df)
        df = benign_biopsy(df)

    # Transpose the measures back into a single column and reapply the counts
    # label to the counts column name
    df = df.stack().reset_index()
    df.rename(columns={0: counts_column}, inplace=True)

    return df


def check_measure_as_rows(df, column_content,
                          measure_as_rows=False, row_content=None, rows=None):
    """
    Checks if there are any rates/percentage measures to be added from the rows
    content and if so transforms the dataframe for these to be applied (so they
    are temporarily set as columns) using the add_measures function.
    Then also applies any rates/percentage that are required for the column
    content.
    Parameters
    ----------
    df : pandas.DataFrame
    column_content: list[str]
        List of column values to be checked which will determine which measures
        will be added to the column content.
        Only used if measure_as_rows is False.
    measure_as_rows: bool
        Indicates if the measures are currently stored in rows (within the first
        variable held in the rows input list).
        Default is False
    row_content: list[str]
        List of column values to be checked which will determine which measure
        will be added to the row content.
        Only used if measure_as_rows is True.
    rows : list[str]
        Variable name that holds the output row information (e.g. region). If
        there are multiple variable names in the list, only the first is checked.
        Only used if measure_as_rows is True.

    Returns
    -------
    pandas.DataFrame
        df with required measures added
    """
    # If the measure as rows flag is set to True
    # then the datframe will be temporarily transposed so that the measures
    # are in columns whilst extra measures are added
    if measure_as_rows:
        # The measures are always expected to be in a single column, as defined
        # by the rows input, so only this column will be selected to be transposed
        rows = rows[0]
        df.set_index([rows], inplace=True)
        df = df.transpose()
        column_content_temp = row_content

        # Add the measures
        df = add_measures(df, column_content_temp)

        # Then transpose the measures back into rows
        df = df.transpose()
        df.reset_index(inplace=True)
    else:
        # Else process the measures in columns
        df = add_measures(df, column_content)

    return df


def add_measures(df, columns):
    """
    Adds required percentage/rates to the dataframe.
    These are only applied where needed for a particular output (as determined
    by the columns content).
    Parameters
    ----------
    df : pandas.DataFrame
    columns: list[str]
        List of column values to be checked which will determine which measures
        will be added to the column content.

    Returns
    -------
    pandas.DataFrame
        df with required measures added
    """

    # This will add a new percentage of (column) total field to a dataframe
    # where column_order includes a parameter ending in '_of_total'
    # (e.g 'Invited_of_total to calcuate percentage of individuals invited).
    for column in columns:
        if str(column).endswith("_of_total"):
            helpers.add_percent_of_total(df, column)

    # Add coverage measures
    if 'Coverage' in columns:
        df = coverage(df)
        df = percent_never_screened(df)

    # Add uptake measures
    if 'Uptake' in columns:
        df = uptake(df)

    # Add assessment referral measures
    if 'Percent_assessment' in columns:
        df = percent_assessment(df)

    # Add STR measures
    if 'Final_STR' in columns:
        df = percent_str(df)
        df = percent_str_referrals(df)

    # Add cancer rate
    if 'Rate_with_cancer' in columns:
        df = rate_with_cancer(df)

    # Add percent of total cancer measures
    if 'Percent_cancer_small_invasive' in columns:
        df = percent_cancer_non_or_micro_invasive(df)
        df = percent_cancer_invasive_total(df)
        df = percent_cancer_small_invasive(df)
        df = percent_cancer_invasive_15mmplus(df)

    # Add invasive cancer measures (percents)
    if 'Percent_small_invasive' in columns:
        df = percent_small_invasive(df)
        df = percent_invasive_15mmplus(df)
        df = percent_invasive_unknown(df)

    # Add invasive cancer measures (rates)
    if ('Rate_small_invasive' in columns) | ('SDR' in columns):
        df = rate_small_invasive(df)
        df = rate_invasive_15mmplus(df)
        df = rate_non_or_micro_invasive(df)

    # Add biopsy referral measures
    if (('Percent_cyt_biop_referrals' in columns)
            | ('Percent_open_biop_referrals' in columns)):
        df = percent_cyt_biop_referrals(df)
        df = percent_open_biop_referrals(df)

    # Add diagnostic measures
    if 'Rate_benign_biopsy' in columns:
        df = rate_benign_biopsy(df)
    if 'Rate_non_op_diagnosis' in columns:
        df = rate_non_op_diagnosis(df)

    # Add SDR calculation
    if 'SDR' in columns:
        df = sdr(df)

    # Add percent high risk screens referred for assessment
    if 'Percent_hr_referred_assess' in columns:
        df = percent_hr_referred_assess(df)

    # Add percent high risk screens referred for assessment
    if 'Rate_hr_cancer_detected' in columns:
        df = rate_hr_cancer_detected(df)

    # Add percent high risk screens referred for assessment
    if 'Rate_hr_invasive_cancers' in columns:
        df = rate_hr_invasive_cancers(df)

    return df


def coverage(df):
    """
    Adds a coverage column to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Women_screened_less3yrs] and df[Women_eligible]
        among the columns

    Returns
    -------
    pandas.DataFrame
        df with 'Coverage' column added

    """
    new_column_name = "Coverage"
    numerator = "Women_screened_less3yrs"
    denominator = "Women_eligible"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_never_screened(df):
    """
    Adds a percent of women never screened column to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Women_never_screened] and df[Women_eligible]
        among the columns

    Returns
    -------
    pandas.DataFrame
        df with percent never screened column added

    """
    new_column_name = "Percent_never_screened"
    numerator = "Women_never_screened"
    denominator = "Women_eligible"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def women_eligible(df):
    """
    Adds a women eligible column to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Women_resident] and df[Women_ineligible] among
        the columns

    Returns
    -------
    pandas.DataFrame
        df with women eligible column added

    """
    df["Women_eligible"] = df["Women_resident"] - df["Women_ineligible"]

    return df


def women_never_screened(df):
    """
    Adds a women never screened column to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Women_selected_no_screen] and
        df[Women_not_selected_not_screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with women never screened column added

    """
    df["Women_never_screened"] = (df["Women_selected_no_screen"]
                                  + df["Women_not_selected_not_screened"])

    return df


def uptake(df):
    """
    Adds an uptake column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invited] and df[Screened]
        among the columns

    Returns
    -------
    pandas.DataFrame
        df with 'Uptake' column added

    """
    new_column_name = "Uptake"
    numerator = "Screened"
    denominator = "Invited"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_assessment(df):
    """
    Adds a referral for assessment percentage column
    and associated low numerator warning to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Women_screened] and
        df[Initial_referred] among the columns

    Returns
    -------
    pandas.DataFrame
        df with percent referred for assessment added

    """
    new_column_name = "Percent_assessment"
    numerator = "Initial_referred"
    denominator = "Screened"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def percent_str(df):
    """
    Adds a short term recall percentage column
    and associated low numerator warning to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Screened] and
        df[Final_STR] among the columns

    Returns
    -------
    pandas.DataFrame
        df with short term recall assessment percentage added

    """
    new_column_name = "Percent_STR"
    numerator = "Final_STR"
    denominator = "Screened"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def invasive_15mmplus(df):
    """
    Adds an invasive (>=15mm) sub-group total to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_15mmto20mm], df[Invasive_20mmto50mm] and
        df[Invasive_50mmplus] among the columns

    Returns
    -------
    pandas.DataFrame
        df with invasive cancer 15mmplus column added

    """
    df["Invasive_15mmplus"] = (df["Invasive_15mmto20mm"]
                               + df["Invasive_20mmto50mm"]
                               + df["Invasive_50mmplus"])

    return df


def small_invasive(df):
    """
    Adds a small invasive (<15mm) sub-group total to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_lessthan10mm] and
        df[Invasive_10mmto15mm] among the columns

    Returns
    -------
    pandas.DataFrame
        df with small invasive column added

    """
    df["Small_invasive"] = (df["Invasive_lessthan10mm"]
                            + df["Invasive_10mmto15mm"])

    return df


def non_or_micro_invasive(df):
    """
    Adds a non or micro invasive (<15mm) sub-group total to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Cancer_non_microinvasive] and
        df[Cancer_microinvasive] among the columns

    Returns
    -------
    pandas.DataFrame
        df with non or micro invasive cancer column added

    """
    df["Non_or_micro_invasive"] = (df["Cancer_non_microinvasive"]
                                   + df["Cancer_microinvasive"])

    return df


def rate_with_cancer(df):
    """
    Adds a 'number with cancer per 1000' column
    and associated low numerator warning to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Total_with_cancer] and
        df[Screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with number with cancer per 1000 people column added

    """
    new_column_name = "Rate_with_cancer"
    numerator = "Total_with_cancer"
    denominator = "Screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def rate_non_or_micro_invasive(df):
    """
    Adds a 'rate non or micro invasive cancer per 1000' column
    and associated low numerator warning to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Non_micro_invasive] and
        df[Screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with number with non or micro invasive cancer per 1000 people screened
        column added

    """
    new_column_name = "Rate_non_or_micro_invasive"
    numerator = "Non_or_micro_invasive"
    denominator = "Screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def rate_invasive_15mmplus(df):
    """
    Adds a 'rate invasive cancer 15mm plus per 1000' column
    and associated low numerator warning to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Large_invasive] and
        df[Screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with number with invasive cancer per 1000 people screened column added

    """
    new_column_name = "Rate_invasive_15mmplus"
    numerator = "Invasive_15mmplus"
    denominator = "Screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def rate_small_invasive(df):
    """
    Adds a 'number with small invasive cancer per 1000' column to the dataframe
    and associated low numerator warning column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Small_invasive] and
        df[Screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with small invasive cancer per 1000 people screened column added

    """
    new_column_name = "Rate_small_invasive"
    numerator = "Small_invasive"
    denominator = "Screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def percent_small_invasive(df):
    """
    Adds a 'percent of small invasive cancers of total invasive cancers'
    column and associated low numerator warning column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Small_invasive] and
        df[Invasive_total] among the columns

    Returns
    -------
    pandas.DataFrame
        df with percent small invasive column added

    """
    new_column_name = "Percent_small_invasive"
    numerator = "Small_invasive"
    denominator = "Invasive_total"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def percent_invasive_15mmplus(df):
    """
    Adds a 'percent of invasive cancers 15mm plus of total invasive cancers'
    column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_15mmplus] and
        df[Invasive_total] among the columns

    Returns
    -------
    pandas.DataFrame
        df with percent invasive 15mm plus column added

    """
    new_column_name = "Percent_invasive_15mmplus"
    numerator = "Invasive_15mmplus"
    denominator = "Invasive_total"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_invasive_unknown(df):
    """
    Adds a 'percent of invasive cancers unknown of total invasive cancers'
    column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_unknown] and
        df[Invasive_total] among the columns

    Returns
    -------
    pandas.DataFrame
        df with percent invasive 15mm plus column added

    """
    new_column_name = "Percent_invasive_unknown"
    numerator = "Invasive_unknown"
    denominator = "Invasive_total"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def benign_biopsy(df):
    """
    Adds a total benign biopsy column to the dataframe

    Parameters
    ----------
    df: pandas.DataFrame
        df expects df[Open_biop_RR] and [Open_biop_STR] among the columns

    Returns
    -------
    pandas.DataFrame
        df with total benign biopsy column added

    """
    df["Benign_biopsy"] = df["Open_biop_RR"] + df["Open_biop_STR"]

    return df


def rate_benign_biopsy(df):
    """
    Adds 'benign biopsy rate' column and associated low numerator warning
    column to the dataframe.

    Parameters
    ----------
    df: pandas.DataFrame
        df expects df[Benign_biopsy] and
        df[Screened] among the columns

    Returns
    -------
    pandas.DataFrame
        df with benign biopsy rate per 1000 screened column added

    """
    new_column_name = "Rate_benign_biopsy"
    numerator = "Benign_biopsy"
    denominator = "Screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def cancers_diagnosed(df):
    """
    Adds a total cancers diagnosed column to the dataframe

    Parameters
    ----------
    df: pandas.DataFrame
        df expects df[Cyt_bio_cancer] and [Open_biop_cancer] among the columns

    Returns
    -------
    pandas.DataFrame
        df with cancers diagnosed column added

    """
    df["Cancers_diagnosed"] = df["Cyt_bio_cancer"] + df["Open_biop_cancer"]

    return df


def rate_non_op_diagnosis(df):
    """
    Adds a 'Non-operative diagnosis rate (overall)' column and associated
    low numerator warning to the dataframe.

    Parameters
    ----------
    df: pandas.DataFrame
        df expects df[Cyt_bio_cancer] and
        df[Open_biop_cancer] among the columns

    Returns
    -------
    pandas.DataFrame
        df with non-operative diagnosis rate (percent) column added

    """
    new_column_name = "Rate_non_op_diagnosis"
    numerator = "Cyt_bio_cancer"
    denominator = "Cancers_diagnosed"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def sdr_expected(df, table_code, year,
                 measure_column="Col_Def",
                 ref_file=param.SDR_MULTIPLIER):
    """
    Creates the expected number of invasive cancers based on the Standardised
    Detection Ratio (SDR) multiplier csv file provided by NHSE.

    Parameters
    ----------
    df : pandas.DataFrame
    columns: str
        Variable name that holds the measure(s) values (to identify 'Screened'
        as used in the SDR calculation)
    table_code: list{str}
        Variable name that holds the collection table code (used to apply the
        correct multiplier - incidence or prevalence).
    year: str
        Used to select the applicable version of SDR ratio data
    measure_column: str
        Column that holds the screened information
    ref_file: Path
        Location of the SDR multipliers csv file.

    Returns
    -------
    df : pandas.DataFrame
        With expected values added as additional rows within the 'Col_Def' column
    """
    # A test is first run the ensure that only the accepted table code inputs
    # have been used where SDR is being created (["A", "B"], or ["C1", "C2"])
    table_code_valid = [["A", "B"], ["C1", "C2"]]
    helpers.validate_value_with_list("table_code", table_code, table_code_valid)

    # Import SDR multiplier csv
    df_sdr = pd.read_csv(ref_file, index_col=None,
                         parse_dates=['Date_start', 'Date_end'], dayfirst=True)

    # Filter SDR multiplier for current year
    df_sdr = helpers.filter_for_year(df_sdr, year)

    # Assert there are no duplicate age band values after filtering
    if not df_sdr['Age band'].is_unique:
        raise "SDR data in the breast_screening_sdr.csv input file covers \
               overlapping periods. Check the file"

    # Filter just to 'Screened'
    df_expected = df[(df[measure_column] == 'Screened')]

    # Join SDR multipliers
    df_expected = df_expected.merge(df_sdr, left_on='Row_Def', right_on='Age band')
    # Add create multiplier to relevant table codes
    if table_code == ["A", "B"]:
        df_expected["Value"] = (df_expected["Value"] *
                                df_expected["Tables A and B"])/1000
    if table_code == ["C1", "C2"]:
        df_expected["Value"] = (df_expected["Value"] *
                                df_expected["Tables C1 and C2"])/1000

    # Drop fields that are no longer required
    df_expected = df_expected.drop(['Tables A and B', 'Tables C1 and C2',
                                    'Age band'], axis=1)

    # Rename Col_Def values
    df_expected[measure_column] = "SDR_expected"

    return pd.concat([df, df_expected])


def sdr(df):
    """
    Adds Standardised Detection Ratio (SDR) column to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Observed] and
        df[Expected] among the columns

    Returns
    -------
    pandas.DataFrame
        df with SDR column added
    """
    new_column_name = "SDR"
    numerator = "Invasive_total"
    denominator = "SDR_expected"
    multiplier = 1

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    # Add an extra column with the low numerator warning
    helpers.low_numerator_warning(df, new_column_name, numerator)

    return df


def percent_cyt_biop_referrals(df):
    """
    Adds percentage of referrals that are for cytology or core biopsies.
    to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Referral_cyt_bio] and df[Initial_referred] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_cyt_biop_referrals column added
    """
    new_column_name = "Percent_cyt_biop_referrals"
    numerator = "Referral_cyt_bio"
    denominator = "Initial_referred"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_open_biop_referrals(df):
    """
    Adds percentage of referrals that are for open biopsies to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Open_biop_total] and df[Initial_referred] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_open_biop_referrals column added
    """
    new_column_name = "Percent_open_biop_referrals"
    numerator = "Open_biop_total"
    denominator = "Initial_referred"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_str_referrals(df):
    """
    Adds percentage of referrals resulting in short term recalls to the dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Initial_referred] and df[Final_STR] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df With Percent_str_outcomes column added
    """
    new_column_name = "Percent_STR_referrals"
    numerator = "Final_STR"
    denominator = "Initial_referred"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_cancer_non_or_micro_invasive(df):
    """
    Adds percentage of total cancers that are non or micro invasive to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Non_or_micro_invasive] and df[Total_with_cancer] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_cancer_non_or_micro_invasive column added
    """
    new_column_name = "Percent_cancer_non_or_micro_invasive"
    numerator = "Non_or_micro_invasive"
    denominator = "Total_with_cancer"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_cancer_invasive_total(df):
    """
    Adds percentage of total cancers that invasive to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_total] and df[Total_with_cancer] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_cancer_invasive_total column added
    """
    new_column_name = "Percent_cancer_invasive_total"
    numerator = "Invasive_total"
    denominator = "Total_with_cancer"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_cancer_small_invasive(df):
    """
    Adds percentage of total cancers that are small invasive (<15mm) to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Small_invasive] and df[Total_with_cancer] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_cancer_small_invasive column added
    """
    new_column_name = "Percent_cancer_small_invasive"
    numerator = "Small_invasive"
    denominator = "Total_with_cancer"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_cancer_invasive_15mmplus(df):
    """
    Adds percentage of total cancers that are invasive (>=15mm) to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[Invasive_15mmplus] and df[Total_with_cancer] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_cancer_invasive_15mmplus column added
    """
    new_column_name = "Percent_cancer_invasive_15mmplus"
    numerator = "Invasive_15mmplus"
    denominator = "Total_with_cancer"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def percent_hr_referred_assess(df):
    """
    Adds percentage of those screened that are referred for assessment to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[HR_Total_referred] and df[HR_Total_screened] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Percent_hr_referred_assess column added
    """
    new_column_name = "Percent_hr_referred_assess"
    numerator = "HR_Total_referred"
    denominator = "HR_Total_screened"
    multiplier = 100

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def rate_hr_cancer_detected(df):
    """
    Adds rate per 1000 of those screened that had cancer detected to the
    dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[HR_Total_women_with_cancer] and df[HR_Total_screened] among the
        columns

    Returns
    -------
    pandas.DataFrame
        df with Rate_hr_cancer_detected column added
    """
    new_column_name = "Rate_hr_cancer_detected"
    numerator = "HR_Total_women_with_cancer"
    denominator = "HR_Total_screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def rate_hr_invasive_cancers(df):
    """
    Adds rate per 1000 of those screened that had invasive cancer detected to
    the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        df expects df[HR_Total_invasive_cancers] and df[HR_Total_screened] among the
        columns

    Returns
    -------
    pandas.DataFrame
       df with Rate_hr_invasive_cancers column added
    """
    new_column_name = "Rate_hr_invasive_cancers"
    numerator = "HR_Total_invasive_cancers"
    denominator = "HR_Total_screened"
    multiplier = 1000

    helpers.add_percent_or_rate(df, new_column_name, numerator,
                                denominator, multiplier)

    return df


def add_validation_columns(df, validations, measures):
    """
    Defines and adds the required validation check columns for time series
    validations outputs.

    Parameters
    ----------
    df : pandas.DataFrame
    validations: list[str]
        list of pre-defined validations to include in the output, as defined
        within this function.
    measures: list[str]
        list of measures included in the output, which will determine which
        breach parameter value to use.

    Returns
    -------
    pandas.DataFrame

    """
    # Define list of valid validation measures
    valid_list = ["YoY_change", "YoY_percent_change", "Avg_columns",
                  "Avg_change", "Avg_percent_change", "YoY_breach",
                  "Avg_breach"]

    # Check for an invalid validation type in the input argument
    for validation in validations:
        helpers.validate_value_with_list("validations", validation,
                                         valid_list)

    # Apply any validations listed in the validations argument

    validation = "YoY_change"
    if validation in validations:
        # Add Year on Year absolute change using years defined in parameters
        df = helpers.add_column_difference(df, new_column_name=validation,
                                           col1=None,  col2=None)

    validation = "YoY_percent_change"
    if validation in validations:
        # Add Year on Year percent change using years defined in parameters
        df = helpers.add_percent_change(df, validation, param.YOY_TO_YEAR,
                                        param.YOY_FROM_YEAR, 100)

    validation = "Avg_columns"
    years = param.ROLLING_AVG_YEARS
    if validation in validations:
        # Add average across number of years, as defined in parameters
        df = helpers.add_average_of_columns(df, param.YOY_TO_YEAR, years)

    validation = "Avg_change"
    if validation in validations:
        # Add absolute change from current year to average across years field
        df = helpers.add_column_difference(df, new_column_name=validation,
                                           col1="Avg_columns", col2=param.YOY_TO_YEAR)

    validation = "Avg_percent_change"
    if validation in validations:
        # Add percent change from current year to average across years field
        df = helpers.add_percent_change(df, validation, param.YOY_TO_YEAR,
                                        "Avg_columns", 100)

    validation = "YoY_breach"
    if validation in validations:
        # Add a year on year breach warning based on the measure
        if "Coverage" in measures:
            breach = param.YOY_COV_BREACH_KC63
            check_column = "YoY_change"
            change_type = "absolute"
        elif 'Rate_with_cancer' in measures:
            breach = param.YOY_RATE_BREACH_KC62
            check_column = "YoY_change"
            change_type = "absolute"
        elif ('Women_eligible' in measures) | ('Women_screened_less3yrs' in measures):
            breach = param.YOY_BREACH_KC63
            check_column = "YoY_percent_change"
            change_type = "percentage"
        elif ('Total_with_cancer' in measures) | ('Invited' in measures):
            breach = param.YOY_BREACH_KC62
            check_column = "YoY_percent_change"
            change_type = "percentage"

        df[validation] = np.where(df[check_column] > breach, "More than "
                                  + str(breach) + change_type
                                  + " difference compared to previous year",
                                  "Pass")

    validation = "Avg_breach"
    if validation in validations:
        # Add an average breach warning based on the measure
        if "Coverage" in measures:
            breach = param.AVG_COV_BREACH_KC63
            check_column = "Avg_change"
            change_type = "percentage point"
        elif ('Rate_with_cancer' in measures):
            breach = param.AVG_RATE_BREACH_KC62
            check_column = "Avg_change"
            change_type = "rate"
        elif ('Women_eligible' in measures) | ('Women_screened_less3yrs' in measures):
            breach = param.AVG_BREACH_KC63
            check_column = "Avg_percent_change"
            change_type = "percentage"
        elif ('Total_with_cancer' in measures) | ('Invited' in measures):
            breach = param.AVG_BREACH_KC62
            check_column = "Avg_percent_change"
            change_type = "percentage"

        df[validation] = np.where(df[check_column] > breach, "More than "
                                  + str(breach) + change_type
                                  + " difference compared to previous year",
                                  "Pass")

    return df
