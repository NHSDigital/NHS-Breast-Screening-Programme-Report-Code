import pandas as pd
import numpy as np
import logging
import bs_code.parameters as param
import bs_code.utilities.helpers as helpers
import bs_code.utilities.field_definitions as definitions
from functools import reduce


logger = logging.getLogger(__name__)


def transpose_for_dashboard(df, name):
    """
    Input dataframe has regional and national level data appended to the local
    level data as part of the standard output production. This function takes
    that and adds region and national measure columns to the local level data
    by joining instead.

    Parameters
    ----------
    df : pandas.DataFrame consisting of local, regional and national level
    data (appended together). Expects CollectionYearRange, Org_ONSCode and
    Parent_OrgONSCode amongst the columns (for joining).
    name: str
        Name of the dashboard (csv) output.

    Returns
    -------
    df : pandas.DataFrame
        df with the regional and national measures now joined to local data rather
        than appended.
    """
    # Set the columns which will be used when selecting and joining the
    # regional/national data. Must be part of the output defined in dashboards.py
    # Note that breakdown is set as a list to allow multiple column inputs if
    # required. Set as [] where no breakdown is included.
    year = "CollectionYearRange"
    region = "Parent_Org_Code"
    org = "Org_Name"
    if name == "Dashboard_Coverage":
        breakdown = []
    if name == "Dashboard_Uptake":
        breakdown = ["Table_CodeDescription"]

    # Extract the local, region, and national level data to 3 seperate dataframes
    df_local = df[df[org].notnull()].dropna(axis=1)
    df_region = df[(df[org].isnull()) &
                   (df[region].notnull())].dropna(axis=1)
    df_national = df[df[region].isnull()].dropna(axis=1)

    # Set the fields to be joined on when adding the regional measure columns
    # to the local level dataframe
    join_on_region = [year, region, *breakdown]
    # Set the fields to be joined on when adding the national measure columns
    join_on_national = [year, *breakdown]

    # Join the regional measure columns to the local data
    df_loc_reg = pd.merge(df_local, df_region, how="left",
                          on=join_on_region)

    # Join the national measure columns
    df_loc_reg_nat = pd.merge(df_loc_reg, df_national, how="left",
                              on=join_on_national)

    return df_loc_reg_nat


def filter_dataframe(df, part, table_code, filter_condition, ts_years, year=param.YEAR):
    """
    Filters a dataframe by a number of parameters, including the number of years
    data required in the table, standard filters on part and table code,
    and by any additional optional filters required (e.g subsets of Row_Def
    and/or Col_Def)

    Parameters
    ----------
    df : pandas.DataFrame
    part : list[str]
        Variable name that holds the collection part.
        Accepts a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts a list of one or more.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    ts_years : Num
        Defines the number of years required in the table.

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to the conditions input to the function.

    """

    # Filter dataframe to number of years defined in ts_years
    year_range = helpers.get_year_range(year, ts_years)
    df = df[(df["CollectionYearRange"].isin(year_range))]

    # Apply pre-set filters on part and table
    if part is not None:
        df = df[df["Part"].isin(part)]
    if table_code is not None:
        df = df[df["Table_Code"].isin(table_code)]

    # Apply the optional general filter
    if filter_condition is not None:
        df = df.query(filter_condition)

    return df


def sort_for_output_defined(df, rows, row_order):
    """
    Sorts the dataframe in the user defined order required for the output.
    If there are multiple columns in the rows list, the ordering will be applied on
    the first row in the list.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list(str)
        Variable name(s) that holds the row labels to be included
        in the output
    row_order: list[str]
        List of row content that determines the inclusions and sorting.

    Returns
    -------
    df : pandas.DataFrame
    """

    # If row_order is not defined.
    # Totals are removed by default and row order is not altered
    if row_order is None:
        df = helpers.remove_rows(df, ["Grand_total"])
    # Where order has been defined.
    else:
        # Select the rows to include in table and apply the row order
        row = rows[0]
        df = df[(df[row].isin(row_order))]
        df = helpers.order_by_list(df, row, row_order)

    return df


def sort_for_output(df, sort_on, cols_to_remove=[]):
    """
    Sorts the dataframe on specified columns required for the output.
    Drops columns only used for sorting.

    Parameters
    ----------
    df : pandas.DataFrame
    sort_on: list[str]
        Columns that will be sorted on (ascending).
    cols_to_remove : list[str]
        List containing the names of any columns to be removed (i.e. those only
        used for sorting)

    Returns
    -------
    df : pandas.DataFrame
    """
    # Drop any total rows (not needed in this pipeline for variable length outputs)
    df = helpers.remove_rows(df, ["Grand_total"])

    # Sort the dataframe based on columns defined by sort_on input
    df = df.sort_values(by=sort_on, ascending=True)

    # Drop any columns only used for sorting and not output to table
    if len(cols_to_remove) > 0:
        df.drop(columns=cols_to_remove, inplace=True)

    return df


def define_org_columns(collection):
    """
    Assigns the variable/column that holds the parent/region code,
    parent/region name, organisation code and organisation name, depending on
    which collection is being processesed (KC62 or KC63). Used for
    tidy csv processing.

    Parameters
    ----------
    collection: str
        Name of the collection that is being processed.

    Returns
    ----------
    Tuple containing the four variable names
    """
    # Establish org and parent code columns to be used in csv. The parent codes
    # vary dependening on the collection)
    if collection == "KC63":
        col_parent_code = "Parent_OrgONSCode"
        col_org_code = "Org_ONSCode"
    else:
        col_parent_code = "Parent_Org_Code"
        col_org_code = "Org_Code"

    col_org_name = "Org_Name"
    col_parent_name = "Parent_Org_Name"
    col_org_type = "Org_Type"

    return (col_parent_code, col_org_code, col_parent_name, col_org_name,
            col_org_type)


def update_org_level_values(df, org_level, col_parent_code, col_org_code,
                            col_parent_name, col_org_name, col_org_type):
    """
    For organisation levels higher than local (national and regional/parents)
    this function replaces values for lower level organisation variables (codes
    and names), with the values of the higher level organisationas e.g. for
    national level data all parent and local org columns are populated with
    the default national values.

    Parameters
    ----------
    df : pandas.DataFrame
    org_level: str
        Identifies the organisation level to be returned. Accepts 'national',
        'regional' and 'local'.
    col_parent_code: str
        Name of variable/column that holds the region code.
    col_org_code: str
        Name of variable/column that holds the local organisation code.
    col_parent_name: str
        Name of variable/column that holds the region name.
    col_org_name: str
        Name of variable/column that holds the local organisation name.
    col_org_type: str
        Name of variable/column that holds the organisation type

    Returns
    -------
    df : pandas.DataFrame
    """
    # If national level data is being extracted, then replace org codes and
    # names with default national values
    if org_level == "national":
        helpers.replace_col_value(df,
                                  [col_parent_code, col_org_code],
                                  "E92000001")
        helpers.replace_col_value(df,
                                  [col_parent_name, col_org_name],
                                  "England")
        df[col_org_type] = "National"

    # If regional level data is being extracted, then replace org codes and
    # names with values from the regional columns
    if org_level == "regional":
        df[col_org_code] = df[col_parent_code]
        df[col_org_name] = df[col_parent_name]
        df[col_org_type] = "Region"

    return df


def create_output_crosstab(df, rows, columns, part, table_code,
                           sort_on, row_order, column_order, column_rename,
                           filter_condition, visible_condition, row_subgroup,
                           column_subgroup, include_row_labels,
                           measure_as_rows, ts_years=1):
    """
    Will create a crosstab output based on any breakdown, and for any number of
    years.
    Measures are added if included in the row or column order and only
    fields required in the final output are included when writing to the file.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. regions) that are
        to be included in the output.
    columns : str
        Variable name that holds the information to be displayed in the output
        column headers (i.e. the measure(s))
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on: list[str]
        List of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        Function will use either this OR row_order for sorting.
    row_order: list[str]
        List of row content that determines the order data will be presented
        in the output. Allows for full control of row ordering (can only include
        row values that exist in the collection). Function will use either this
        OR sort_on for sorting.
    column_order: list[str]
        List of column descriptions that determines the order they will be
        presented in the output.
        If set to None then the total of each year will be applied.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    visible_condition : str
        This is an optional condition, as a string.
        This is used to select rows that will not be visible (use 'not in') or
        that will be the only rows visible (use 'in') in the output. This will not
        affect totals / subgroup totals which are added before this condition
        is applied.
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    column_subgroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on column content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the 'columns' variable) that
        will form the group.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement. Any column set within the 'rows' or
        'column order' parameters can be renamed.
    include_row_labels: bool
        Determines if the row labels will be included in the output.
    measure_as_rows: bool
        Indicates if there are measures to be added as rows (will only be applied
        to the first variable held in the 'rows' input list).
    ts_years: int
        Number of years to be used in the time series.
        Default is 1.

    Returns
    -------
    df : pandas.DataFrame
        in the form of a crosstab, with aggregated counts
    """
    # Filter data to years required for timeseries
    df_filtered = filter_dataframe(df, part, table_code, filter_condition,
                                   ts_years)

    # Create list of years to use in loop
    years = helpers.create_year_list(df_filtered, 'CollectionYearRange')

    # Rename the original rows input (those to be included in output) for later
    # use in selecting index
    rows_output = rows

    # Where sort_on is being used
    if sort_on is not None:
        # Combine the rows and sort_on lists to ensure all are included for
        # processing (created as a set to remove fields that appear in both lists).
        rows_all = set(rows + sort_on)
        # Identify any columns that are only used to sort on (will not be
        # included in the final output)
        cols_to_remove = list(set(rows_all) - set(rows))
        # Now redefine rows to also include the column(s) used for sorting only
        rows = rows + cols_to_remove

    # Create an empty dataframe to store the data for each year in loop
    df_all = []

    # Loops through the processing steps for each year in the time series
    for year in years:
        # Creates dataframe for each year in the loop (oldest first)
        df_year = (df_filtered[(df_filtered["CollectionYearRange"] == year)]
                   .copy(deep=True))

        # If SDR is part of output then create the expected invasive cancers
        # required to calculate SDR and add them to the dataframe
        if column_order is not None:
            if 'SDR' in column_order:
                df_year = definitions.sdr_expected(df_year, table_code, year)

        # Pivots the dataframe into a crosstab
        df_agg = pd.pivot_table(df_year,
                                values="Value",
                                index=rows,
                                columns=columns,
                                aggfunc="sum",
                                margins=True,
                                margins_name="Grand_total").reset_index()

        # Add any required row or column subgroups to data
        if row_subgroup is not None:
            df_agg = helpers.add_subgroup_rows(df_agg, rows, row_subgroup)

        if column_subgroup is not None:
            df_agg = helpers.add_subgroup_columns(df_agg, column_subgroup)

        # This step ensures column_order it is not empty where called later.
        # If no columns and column order were defined then set it as an
        # empty list (output will be as a list with no counts).
        if (columns is None) & (column_order is None):
            column_order = []
        # Else if just no column_order was defined then set it as the total column
        # created by the pivot table function.
        elif column_order is None:
            column_order = ["Grand_total"]

        # Then add calculations that are needed from field_definitions file
        df_agg = definitions.check_measure_as_rows(df_agg, column_order,
                                                   measure_as_rows, row_order,
                                                   rows)

        # Updates national/regional invasive and non-invasive non-operative
        # rates
        if "Parent_Org_Code" in rows:
            for column in ["Non-op_diag_rate_invasive", "Non-op_diag_rate_non-invasive"]:
                if column in column_order:
                    df_agg = helpers.replace_col_value(df_agg, [column], ":")

        # Set final df column content (for now including any column that is
        # only used for sorting). Done inside the loop before column renaming.
        df_agg = df_agg[rows + column_order]

        # If more than 1 year will be run, and years will not be outputted as
        # rows then add the year to column names so that for each df in the
        # loop they have a different name # (avoids conflicts on duplicate names)
        if ("CollectionYearRange" not in rows) & (ts_years > 1):
            for col in column_order:
                df_agg = df_agg.rename(columns={col: col + " " + year})

        # Appends data to df_final data frame
        df_all.append(df_agg)

    # Appends or joins (depending on if years are in rows or columns) data for
    # all years used in the time series together, oldest first.
    if ("CollectionYearRange" in rows):
        df_joined = pd.concat(df_all)
    else:
        df_joined = (reduce(lambda left, right: pd.merge
                            (left, right, on=rows, how='outer'),
                            df_all))

    # Apply final row order and remove columns that are only used to sort on
    if sort_on is not None:
        df_sorted = sort_for_output(df_joined, sort_on, cols_to_remove)
    else:
        df_sorted = sort_for_output_defined(df_joined, rows, row_order)

    # Apply the optional row filter
    if visible_condition is not None:
        df_sorted = df_sorted.query(visible_condition)

    # Rename the user selected columns as defined in column_rename dictionary
    if column_rename is not None:
        df_sorted = df_sorted.rename(columns=column_rename)

    # If row labels are not needed then set these as the index so will be
    # excluded when writing
    if include_row_labels is False:
        df_sorted.set_index([*rows_output], inplace=True)

    return df_sorted


def create_output_measure(df, measure_column, measure,
                          rows, columns, part, table_code, sort_on,
                          row_order, column_order, column_rename,
                          filter_condition, subgroup,
                          include_row_labels, ts_years=1):
    """
    A variation on the create_output function that is only used for crosstab
    outputs where the entire output contains a single measure (e.g. uptake)
    for the single reporting year.

    Parameters
    ----------
    df : pandas.DataFrame
    measure_column: str
        Single variable name that holds the measure information (e.g. Col_Def)
    measure : str
        Name of single measure to be returned. Must be a value from the
        measure_column or a calculated field from field_definitions.
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. regions) that are
        to be included in the output.
    columns : str
        Variable name that holds the table column information (e.g. table_code)
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on: list[str]
        List of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        Function will use either this OR row_order for sorting.
    row_order: list[str]
        List of row content that determines the order data will be presented
        in the output. Allows for full control of row ordering (can only include
        row values that exist in the collection). Function will use either this
        OR sort_on for sorting.
    column_order: list[str]
        List of column descriptions that determines the order they will be
        presented in the output.
        If set to None then the total of each year will be applied.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    include_row_labels: bol
        Determines if the row labels will be included in the output.
    ts_years: int
        Number of years to be used in the time series.
        Default is 1.

    Returns
    -------
    df : pandas.DataFrame
    """
    # Filter the dataframe by filter conditions
    df_filtered = filter_dataframe(df, part, table_code, filter_condition,
                                   ts_years)

    # Rename the original rows input (those to be included in output) for later
    # use in selecting index
    rows_output = rows

    # Where sort_on is being used
    if sort_on is not None:
        # Combine the rows and sort_on lists to ensure all are included for
        # processing (created as a set to remove fields that appear in both lists).
        rows_all = set(rows + sort_on)
        # Identify any columns that are only used to sort on (will not be
        # included in the final output)
        cols_to_remove = list(set(rows_all) - set(rows))
        # Now redefine rows to also include the column(s) used for sorting only
        rows = rows + cols_to_remove

    # Create a combined list of variables that will hold the row and columns
    # information. Sets what is to be included in the dataframe alongside the
    # measure.
    rows_columns = [*rows, columns]

    # Pivot and aggregate the data with measure_column content set as columns.
    df_agg = pd.pivot_table(df_filtered,
                            values="Value",
                            index=rows_columns,
                            columns=measure_column,
                            aggfunc="sum",
                            margins=True,
                            margins_name="Grand_total").reset_index()
    # Remove the column grand total as this is added during the adding of
    # subgroups next
    df_agg = df_agg[~df_agg.eq("Grand_total").any(axis=1)]

    # Add the subtotals for each column
    df_agg = helpers.add_subtotals(df_agg, rows_columns)

    # Add any required row subgroups to the dataframe
    if subgroup is not None:
        df_agg = helpers.add_subgroup_rows(df_agg, rows_columns, subgroup)

    # If no column order was defined then assign it as Total. Ensures is not
    # empty where called later.
    if column_order is None:
        column_order = ["Grand_total"]

    # If required add the measure from field_definitions file
    df_agg = definitions.add_measures(df_agg, [measure])

    # Retain only the specified measure from the measure column
    cols_to_retain = [*rows_columns, measure]
    df_agg = df_agg[cols_to_retain]

    # Now that non-measure counts have been removed, pivot the variable
    # containing the required column information into the column headers.
    df_measure = pd.pivot_table(df_agg,
                                values=measure,
                                index=rows,
                                columns=columns).reset_index()

    # Set final df column content (for now including any column that is
    # only used for sorting). Done inside the loop before column renaming.
    df_measure = df_measure[rows + column_order]

    # Apply final row order and remove columns that are only used to sort on
    if sort_on is not None:
        df_sorted = sort_for_output(df_measure, sort_on, cols_to_remove)
    else:
        df_sorted = sort_for_output_defined(df_measure, rows, row_order)

    # Rename the user selected columns as defined in column_rename dictionary
    if column_rename is not None:
        df_sorted = df_sorted.rename(columns=column_rename)

    # If row labels are not needed then set these as the index so will be
    # excluded when writing
    if include_row_labels is False:
        df_sorted.set_index([*rows_output], inplace=True)

    return df_sorted


def create_output_csv_tidy(df, collection, org_level, breakdown,
                           measure_column, part, table_code, sort_on,
                           measure_order, column_rename, filter_condition,
                           visible_condition, breakdown_subgroup,
                           ts_years=1, year_column="CollectionYearRange",
                           not_applicable=param.NOT_APPLICABLE):
    """
    Will create an output in a csv ready tidy format based on any breakdown,
    and selection of measures (as defined in measure/measure_order) for a
    specified organisation level (national, regional or local).
    Year is included as a default.

    Parameters
    ----------
    df : pandas.DataFrame
    collection: str
        Screening collection source for the output (KC62 or KC63).
    breakdown : list[str]
        Variable name(s) that define the breakdowns to be included in the
        output.
    org_level : str
        Defines the level of organisation that the data will include.
        Valid inputs are 'national', 'regional', 'local'.
    measure_column : str
        Variable name that holds the measure information (e.g. Col_Def).
    part : list[str]
        Variable name that holds the collection part.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
    sort_on : list[str]
        List of columns names to sort on (ascending).
    measure_order: list[str]
        List of measure names from the measure_column that determines what is
        included and the order they will be presented in the output.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source version
        to output requirement.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string.
    visible_condition : str
        This is an optional condition, as a string.
        This is used to select rows that will not be visible (use 'not in') or
        that will be the only rows visible (use 'in') in the output. This will not
        affect totals / subgroup totals which are added before this condition
        is applied.
    breakdown_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    ts_years: int
        Defines the number of time series years included in the output
        Default is 1.
    year_column: str
        Column/variable name that holds the time period (year) information.
    not_applicable: str
        The text that will replace null values in the returned calculations.

    Returns
    -------
    df : pandas.DataFrame
    """
    # A check is first run to ensure that a valid value has been submitted for
    # the org_level parameter.
    org_level_valid = ["national", "regional", "local"]
    helpers.validate_value_with_list("org_level", org_level, org_level_valid)

    # Set org and parent code columns to be used in csv (the parent codes
    # vary dependening on the collection)
    col_parent_code, col_org_code, col_parent_name, col_org_name, col_org_type = (define_org_columns
                                                                                  (collection))

    # Filter data to years required for timeseries
    df_filtered = filter_dataframe(df, part, table_code, filter_condition,
                                   ts_years)

    # Where the data is to be extracted at national or regional level, lower
    # level organisation details are replaced with those from the higher level(s)
    df_updates = update_org_level_values(df_filtered, org_level,
                                         col_parent_code, col_org_code,
                                         col_parent_name, col_org_name,
                                         col_org_type)

    # Define a list of columns for the sub-national breakdowns to be included.
    # This varies depending on the collection.
    if collection == "KC63":
        org_breakdown = [col_parent_code, col_parent_name,
                         col_org_code, col_org_name, col_org_type]
    else:
        org_breakdown = [col_parent_code, col_parent_name,
                         col_org_name, col_org_type]

    # Add the year and organisation level breakdowns to the user defined
    # breakdowns to create a single list of breakdown column names to be used
    breakdown = [year_column, *org_breakdown, *breakdown]

    # Where sort_on is being used
    if sort_on is not None:
        # Combine the breakdowns and sort_on lists to ensure all are included
        # for processing (created as a set to remove fields that appear in
        # both lists).
        breakdown_all = set(breakdown + sort_on)
        # Identify any columns that are only used to sort on (will not be
        # included in the final output)
        cols_to_remove = list(set(breakdown_all) - set(breakdown))
        # Now redefine breakdowns to also include the column(s) used for
        # sorting only
        breakdown = breakdown + cols_to_remove

    # If SDR is part of output then create the expected invasive cancers
    # required to calculate SDR and add them to the dataframe
    if 'SDR' in measure_order:
        # Set up empty list
        total_dfs = []

        # Get distinct list of years from data
        years = list(df_updates["CollectionYearRange"].unique())

        for year in years:
            # Filter dataframe for each year
            df_sdr = df_updates[df_updates["CollectionYearRange"] == year]
            # Apply SDR expected function for given year
            df_sdr = definitions.sdr_expected(df_sdr, table_code, year)
            # Add new sdr dataframe to list
            total_dfs.append(df_sdr)

        # Concatenate data for all years
        df_updates = pd.concat(total_dfs).reset_index()

    # Pivots the dataframe so the measure_column content is set as columm headers
    df_agg = pd.pivot_table(df_updates,
                            values="Value",
                            index=breakdown,
                            columns=measure_column,
                            aggfunc="sum",
                            margins=True,
                            margins_name="Grand_total").reset_index()

    if breakdown_subgroup is not None:
        df_agg = helpers.add_subgroup_rows(df_agg, breakdown, breakdown_subgroup)

    # Add any calculations that are needed from field_definitions file
    df_agg = definitions.add_measures(df_agg, measure_order)

    # Updates national/regional invasive and non-invasive non-operative rates
    if org_level in ["national", "regional"]:
        for column in ["Non-op_diag_rate_invasive", "Non-op_diag_rate_non-invasive"]:
            if column in measure_order:
                df_agg = helpers.replace_col_value(df_agg, [column], ":")

    # Set final df content (for now including any column that is only used for
    # sorting).
    df_agg = df_agg[breakdown + measure_order]

    # Apply final row order and remove columns that are only used to sort on
    if sort_on is not None:
        df_sorted = sort_for_output(df_agg, sort_on, cols_to_remove)
    else:
        df_sorted = df_agg

    # Apply the optional row filter
    if visible_condition is not None:
        df_sorted = df_sorted.query(visible_condition)

    # Rename the user selected columns as defined in column_rename dictionary
    if column_rename is not None:
        df_sorted = df_sorted.rename(columns=column_rename)

    # Apply the default not applicable symbol to null values
    df_sorted = df_sorted.fillna(not_applicable)

    return df_sorted


def create_output_ts_validations(df, rows, measures, part, table_code, sort_on,
                                 filter_condition, row_subgroup, validations,
                                 ts_years, measure_column="Col_Def",
                                 ts_column="CollectionYearRange"):
    """
    Will create a crosstab output with time series set as columns, and measures
    in rows, plus any additonal required breakdowns. Can be set for any number
    of years and existing measures.
    Validation check columns are added as defined by user input.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. org names, age breakdowns)
        that are to be included in the output. Multiple variables can be used.
    measures : list[str]
        Name of measure(s) to be returned. Must be an existing value from the
        measure_column, can not be a rate/percentage calculated field
        from field_definitions.
    part : list[str]
        Variable name that holds the collection part.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
    sort_on : list[str]
        List of columns names to sort on (ascending).
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string.
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    validations: list[str]
        List of pre-defined validations to include in the output. Must
        exist in processing_steps.add_validation_columns
    ts_years: int
        Number of years to be shown in the time series.
    measure_column: str
        Single column name that holds the measure information (e.g. Col_Def)
    ts_column: str
        Single column name that holds the years for the time series.

    Returns
    -------
    df: pandas.DataFrame

    """
    # Standardardise letter casing to upper case for all LA names within KC63 data
    if ('Women_eligible' in measures) | ('Women_screened_less3yrs' in measures):
        df["Org_Name"] = df["Org_Name"].str.upper()

    # Filter data to years required for timeseries
    df_filtered = filter_dataframe(df, part, table_code, filter_condition,
                                   ts_years)

    # Filter data to measures to output
    df_filtered = df_filtered[df_filtered[measure_column].isin(measures)]

    # Pivot dataframe so that the years in the time series are presented as columns
    df_agg = pd.pivot_table(df_filtered,
                            values="Value",
                            index=rows,
                            columns=ts_column,
                            aggfunc="sum").reset_index()

    # Add any required row subgroups to the dataframe
    if row_subgroup is not None:
        df_agg = helpers.add_subgroup_rows(df_agg, rows, row_subgroup)

    # Sort rows in dataframe by order defined in sort_on
    if sort_on is not None:
        df_agg = df_agg.sort_values(by=sort_on, ascending=True)

    # Add required validation columns
    df_validations = definitions.add_validation_columns(df_agg,
                                                        validations, measures)

    # Set index ready for writing to Excel
    df_validations.set_index(rows, inplace=True)

    return df_validations


def create_output_ts_validations_measure(df, rows, measure, part, table_code,
                                         sort_on, filter_condition, subgroup,
                                         validations, ts_years,
                                         measure_column="Col_Def",
                                         ts_column="CollectionYearRange"):
    """
    A variation on the create_output_ts_validation function that is used for
    outputs where the entire crosstab contains a single measure calculated from
    2 existing measures (e.g. coverage).
    The output can be created for any number of years.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. regions) that are
        to be included in the output.
    measure : str
        Name of single measure to be returned. Must be a value from the
        measure_column or a calculated field from field_definitions.
    part : list[str]
        Variable name that holds the collection part.
        Accepts None (no filter applied) or a list of one or more.
    table_code : list[str]
        Variable name that holds the collection table code (letter).
        Accepts None (no filter applied) or a list of one or more.
    sort_on: list[str]
        Optional list of columns to sort on (ascending).
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
    validations: list[str]
        list of pre-defined validations to include in the output. Must
        exist in processing_steps.add_validation_columns
    ts_years: int
        Number of years to be shown in the time series.
    measure_column: str
        Single column name that holds the measure information (e.g. Col_Def)
    ts_column: str
        Single column name that holds the years for the time series.

    Returns
    -------
    df : pandas.DataFrame
        in the form of a crosstab, with aggregated counts
    """
    # Standardardise letter casing to upper case for all LA names within KC63 data
    if ('Coverage' in measure):
        df["Org_Name"] = df["Org_Name"].str.upper()

    # Filter data to years required for timeseries
    df_filtered = filter_dataframe(df, part, table_code, filter_condition,
                                   ts_years)

    rows_columns = [*rows, ts_column]

    # Pivot and aggregate the data with measure_column content set as columns.
    df_agg = pd.pivot_table(df_filtered,
                            values="Value",
                            index=rows_columns,
                            columns=measure_column,
                            aggfunc="sum").reset_index()

    # Add the subtotals for each column
    df_agg = helpers.add_subtotals(df_agg, rows_columns)

    # Add any required row subgroups to the dataframe
    if subgroup is not None:
        df_agg = helpers.add_subgroup_rows(df_agg, rows_columns, subgroup)

    # If required add the measure from field_definitions file
    df_agg = definitions.add_measures(df_agg, [measure])

    # Retain only the specified measure from the measure column
    cols_to_retain = [*rows_columns, measure]
    df_agg = df_agg[cols_to_retain]

    # Now that non-measure counts have been removed, pivot the variable
    # containing the required column information into the column headers.
    df_measure = pd.pivot_table(df_agg,
                                values=measure,
                                index=rows,
                                columns=ts_column).reset_index()

    # Drop the grand_total of year column
    df_measure = df_measure.drop(["Grand_total"], axis=1)

    # Add required validation columns, first adding single measure to a list
    # as required for validations function
    measures = [measure]
    df_validations = definitions.add_validation_columns(df_measure,
                                                        validations, measures)

    # Apply final row order
    if sort_on is not None:
        df_validations = sort_for_output(df_measure, sort_on)

    # Set index ready for writing to Excel
    df_validations.set_index(rows, inplace=True)

    return df_validations


def output_specific_updates(df, name):
    """
    This checks the output name and applies any transformations/updates that
    are specific to a particular output(s), that are not covered by the general
    functions.

    Parameters
    ----------
    df : pandas.DataFrame
    name: str
        Name of output. This will be the worksheet name for Excel outputs and
        the filename for csv outputs.

    Returns
    -------
    df : pandas.DataFrame
    """
    # Add last 2 years change calculation for table 12
    # (based on values in last 2 columns)
    if name == "Table 12":
        df = helpers.add_column_difference(df)

    # Transpose regional and national measures for the main dashboard outputs
    if name in ["Dashboard_Coverage", "Dashboard_Uptake"]:
        df = transpose_for_dashboard(df, name)

    # Add the BSU flag column to the BSU list for the internal BSU dashboard
    # and drop the counts column produced by the process by default.
    if name in ["Dashboard_Internal_BSU_Flagged"]:
        df = helpers.new_column_from_check_list(df, "Org_Code",
                                                param.BSU_FLAGGED,
                                                "BSU stopped 47-49 screening",
                                                "BSU - other")

    return df
