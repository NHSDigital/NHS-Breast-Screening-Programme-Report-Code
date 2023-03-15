from pathlib import Path
import pandas as pd
import numpy as np
import math
from itertools import chain, combinations
import bs_code.parameters as param
import datetime


def get_project_root() -> Path:
    """
    Return the project root path from any file in the project.

    Example:
        from parent.utilities.helpers import get_project_root
        root_path = get_project_root()
    """
    return Path(__file__).parent.parent.parent


def get_year_range(end_year: str, year_span: int):
    """
    Create list of year strings, given an end year and a number of years to go back

    Example:
        get_year_range('2020-21',2)
        returns -> ['2020-21','2019-20']
    """
    year_range = []

    for n_year in range(year_span):
        year = (str(int(end_year[0:4])-(n_year))
                + "-"
                + str(int(end_year[5:7])-(n_year)))
        year_range.append(year)
        n_year += 1

    # List oldest year first
    return year_range[::-1]


def new_column_from_lookup(df, from_column, lookup, new_column):
    """
    Add a new dataframe column by looking up values in a dictionary

    Parameters
    ----------
    df : pandas.DataFrame
    from_column: str
        name of the column containing the original values
    lookup: dict
        contains the lookup from and to values
    new_column: str
        name of the new column containing the values to added

    Returns
    -------
    df : pandas.DataFrame
        with added column
    """
    # create the lookup dataframe from the lookup input
    df_lookup = pd.DataFrame(list(lookup.items()))
    df_lookup.columns = [from_column, new_column]

    # add the new column based on the lookup df
    df = df.merge(df_lookup, how='left',
                  on=[from_column])

    return df


def new_column_from_check_list(df, check_column, check_content,
                               value_if_true, value_if_false):
    """
    Adds a new column(s) to a dataframe with the content determined by the
    result of a check of values in an existing column against a list of user
    defined values.
    The value in the new column is added on a true (exists in the check data)
    or false (does not exist in the check data) basis.

    Parameters
    ----------
    df : pandas.DataFrame
    check_column: str
        name of the existing dataframe column containing the values to be
        checked.
    check_content: dict(str, list)
        contains the new column name, and a list of values that will be
        checked against.
    value_if_true:
        value that will be applied if the check is True (value exists in the
        ref data). Mmust match the format of 'value_if_false'.
    value_if_false:
        value that will be applied if the check is False (value does not exist
        in the ref data). Must match the format of 'value_if_true'.

    Returns
    -------
    df : pandas.DataFrame
        with added column
    """
    # Check the format of the values to be applied under the true and false
    # outcome of the check
    format_if_true = type(value_if_true)
    format_if_false = type(value_if_false)

    # Raise an error if these formats do not match
    if format_if_true != format_if_false:
            raise ValueError("The value_if_true and value_if_false arguments are of different formats")

    # For each new column name specified in the input dictionary, extract the
    # new column name and reference values within it to check against
    for new_column_name, check_values in check_content.items():
        # Check that the name of the reference column exists in dataframe
        if check_column not in df:
            raise ValueError(f"The column {check_column} is needed to create {new_column_name} but is not in the dataframe")

        # Add the new column with the required true and false flag values
        df[new_column_name] = np.where(df[check_column].isin(check_values),
                                       value_if_true, value_if_false)

    return df


def replace_col_value(df, col_names, replace_value):
    """
    Will replace all values in a column(s) with a specified default value
    (is currently used for Table 14 to replace invalid regional invasive
    and non-invasive non-operative diagnosis rates)

    Parameters
    ----------
    df : pandas.DataFrame
    col_names : list[str]
        Names of columns where rate values to be replaced
    replace_value : str
        Value to replace existing rate values (e.g ":")

    Returns
    -------
    df : pandas.DataFrame
        With updated values for specified columns
    """

    for col in col_names:
        df[col] = replace_value

    return df


def remove_rows(df, remove_values):
    """
    Will remove rows from dataframe that contain the specified values

    Parameters
    ----------
    df : pandas.DataFrame
    remove_values : list[str]
        list of values based on which the rows will be removed if found
        in any df columns.

    Returns
    -------
    df : pandas.DataFrame
        With rows removed
    """
    for condition in remove_values:
        df = df[~df.eq(condition).any(axis=1)]

    return df


def excel_cell_to_row_num(cell):
    '''
    Convert Excel cell reference to Excel row number for use in
    xlwings (e.g. A1 = 1, C23 = 23).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")
    Returns
    -------
    int
        Number indicating the equivalent Excel row number
    '''
    # Convert the cell reference to row number
    row_num = int(''.join(filter(str.isdigit, cell)))

    return row_num


def excel_cell_to_col_num(cell):
    '''
    Convert Excel cell reference to Excel numeric column position for use in
    xlwings (e.g. A1 = 1, C23 = 2).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")

    Returns
    -------
    integer
        Number indicating the equivalent Excel column number
    '''
    # Convert the cell reference to column letter(s)
    col = ''.join(filter(str.isalpha, cell))

    # return the excel column number
    col_num = 0
    for c in col:
        col_num = col_num * 26 + (ord(c.upper()) - ord('A')) + 1

    return col_num


def excel_col_letter_to_col_num(col):
    '''
    Converts an Excel column letter into the Excel column number for use in
    xlwings (e.g. D = 4).

    Parameters
    ----------
    col: str
        Excel column letter

    Returns
    -------
    integer
        Number indicating the Excel column position
    '''
    col_num = ord(col[0])-ord('A') + 1
    if len(col) == 1:
        col_num
    if len(col) == 2:
        col_num = (int(math.pow(26, len(col)-1) * col_num
                       + excel_col_letter_to_col_num(col[1:])))

    return col_num


def excel_col_to_df_col(col, write_cell):
    '''
    Converts an Excel column letter into a dataframe column position based on
    an a starting cell (write_cell) in Excel e.g. if the column letter is
    D, and the write_cell is B10, then the output will be 2 (3rd column in df)

    Parameters
    ----------
    col: str
        Excel column letter
    write_cell: str
        cell that identifies start of where df will be written

    Returns
    -------
    order of letter value: int
        number indicating which position to insert new column into dataframe
    '''
    if len(col) == 1:
        return (ord(col[0])) - (ord(write_cell[0]))
    if len(col) == 2:
        return (int(math.pow(26, len(col)-1)*(ord(col[0]) - ord('A') + 1)
                    + excel_col_to_df_col(col[1:], write_cell)))


def validate_value_with_list(check_name, value, valid_values):
    """
    Checks a string against a list of strings and aborts the process if it is not
    found in the list.

    Parameters
    ----------
    check_name: str
        Name of the item being checked that will be returned in the system
        exit message.
    value: str
        Value to be checked.
    valid_values: list[str]
        Contains the valid values to check against.
    """
    if value not in valid_values:
        raise ValueError(f'An invalid value has been entered in the {check_name} input. Only {valid_values} are valid values')


def low_numerator_warning(df, calculated_column, numerator_column,
                          low=25, flag=param.LOW_NUMERATOR):
    """
    For a calculated field, checks each row of the numerator column for values
    below a defined level and flags when this condition is met, in a new column.

    Parameters
    ----------
    df : pandas.DataFrame
    calculated_column: str
        Name of the calculated field. Used for part of the naming of the new
        column.
    numerator_column: str
        Column that contains the numerator data.
    low: int
        A flag will be added if the numerator is lower than this value.
    flag: int
        The flag value that will be shown in the new column.

    Returns
    -------
    df : pandas.DataFrame
    """
    # Set the name of the new column based on the name of the calculated field
    new_column_name = calculated_column + "_warning"
    # For each row, where the condition is met, add the flag,
    # otherwise leave empty
    df[new_column_name] = np.where(df[numerator_column] < low, flag, "")

    return df


def add_percent_or_rate(df, new_column_name, numerator,
                        denominator, multiplier=1):
    """
    Adds a percent or rate to a dataframe based on specified column inputs.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column.
    numerator: str
        Name of dataframe column that contains the numerator values
    denominator: str
        Name of dataframe column that contains the denominator values
    multiplier: int
        Value by which the calculated field will be multiplied by e.g. set to
        100 for percents. If no multiplier is needed then the parameter should
        be excluded or set to 1.

    Returns
    -------
    df : pandas.DataFrame
    """
    if numerator not in df:
        raise ValueError(f"The column {numerator} is needed to create {new_column_name} but is not in the dataframe")
    if denominator not in df:
        raise ValueError(f"The column {denominator} is needed to create {new_column_name} but is not in the dataframe")

    df[new_column_name] = ((df[numerator]/df[denominator] * multiplier))

    return df


def add_column_difference(df,
                          new_column_name="Difference"):
    """
    Adds a difference column to a dataframe based on the last 2 columns.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column. Set by default to 'Difference'

    Returns
    -------
    df : pandas.DataFrame
    """
    # Select the last 2 columns in the dataframe
    df_columns = df.iloc[:, -2:]

    # Check that there are at least 2 columns to perform the calculation
    if len(df_columns.columns) < 2:
        raise ValueError("A difference calculation is being attempted on less than 2 columns")

    from_column = df_columns.iloc[:, 0]
    to_column = df_columns.iloc[:, 1]
    # Extract the column names of the 2 columns on which the calculation will
    # be performed
    from_column_name = from_column.name
    to_column_name = to_column.name

    # Check for numeric values in the 2 columns
    if from_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"add_column_difference function is being performed on column ({from_column_name}) that contains non-numeric values")
    if to_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"add_column_difference function is being performed on column ({to_column_name}) that contains non-numeric values")

    # Add a new column with the calculated difference
    df[new_column_name] = (to_column - from_column)

    return df


def add_percent_of_total(df, new_col_name, total_name="Grand_total"):
    '''
    Adds a new column which holds the percents of each value from an existing
    column as the percent of it's total (for example as used within the report
    tables). When using this function, there must be a column name ending
    of_total" (eg "Invited_of_total"). This will be used to contain the new
    percentage values and should be defined in the column_order settings in
    tables.py.

    Parameters
    ----------
    df : pandas.DataFrame
    new_col_name: str
        Name of column to be created. This should be set as the name of the
        base (numerator) column + "_of_total" and will contain the percentage
        values.
    total_name: str
        Identifies the row value that contains the base column total to be used
        as the denominator.

    Returns
    -------
    pandas.DataFrame
        with new column added
    '''
    # Creates a new numerator field
    base_col_name = new_col_name.replace("_of_total", "")
    # Creates a new dataframe containing only the total row (defined by total_name)
    df_total = df[(df.isin([total_name]).any(axis=1))]
    # Adds a new temporary column where each row contains the extracted total
    # This will be used as the denominator when calculating percentages
    df["temp_col"] = df_total[base_col_name].item()
    # Adds the new percentage_of_total column to the dataframe
    df = add_percent_or_rate(df, new_col_name,
                             base_col_name,
                             "temp_col", 100)
    # Removes the denominator column (temp_col) as this is no longer required
    df.drop(["temp_col"], axis=1, inplace=True)

    return df


def add_subtotals(df, columns,
                  total_name="Grand_total"):
    """
    Add row totals and sub-totals to a dataframe for all specified dataframe
    column combinations.

    Parameters
    ----------
    df : pandas.DataFrame
    columns: list[str]
        Columns to use in the breakdowns (e.g. age, sex, etc)
    total_name: str
        Default value to be assigned where totals are added.

    Returns
    -------
    pandas.DataFrame

    """

    # List to store the different sub-groups
    total_dfs = []

    # Combinations of columns to be replaced with total_name
    # Firstly don't replace any, then replace a single column, then 2 columns, etc
    # E.g. [[], ["sex"], ["age"], ["sex", "age"], ...]
    n_replacements = len(columns) + 1
    replace_combinations = [combinations(columns, n) for n in range(n_replacements)]
    replace_combinations = chain.from_iterable(replace_combinations)

    for columns_to_replace in replace_combinations:
        # Make a copy of df with default values for non-grouped columns
        # inserted (e.g. replace values in 'sex' with total_name)
        default_df = df.copy()

        for col in columns_to_replace:
            default_df[col] = total_name

        # Aggregate the column values / counts
        default_df = default_df.groupby(columns).sum().reset_index()

        # Add each of the subgroup datafranes just created to the total dataframe
        # list
        total_dfs.append(default_df)

    # Add each dataframe from the list of dataframes together
    return pd.concat(total_dfs, axis=0).reset_index(drop=True)


def add_subgroup_rows(df, breakdown, subgroup):
    """
    Combines groups of values in specified dataframe column into a subgroup
    and adds new rows to the datatframe with the grouped value.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with breakdowns and counts
    breakdown: list[str]
        The column(s) present in the dataframe on which the data is aggregated
        i.e. the non count/measure columns
        This can include the column to which the subgroup function is being
        applied.
    subgroup: dict(dict(str, list))
        Contains the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the new
        grouping(s), and the original subgroup values that will form the group.
        e.g. {"AgeBand": {'53<71': ['53-54', '55-59', '60-64', '65-69', '70']}}

    Returns
    -------
    pandas.DataFrame with subgroup added to target column

    """
    # Extract the target column, and the subgroup info (a 2nd dictionary nested
    # within the subgroup dictionary)
    for subgroup_column, subgroup_info in subgroup.items():
        # For each set of items in subgroup info
        for subgroup_code, subgroup_values in subgroup_info.items():
            # Then add new rows for the subgroup
            df_subgroup = df[df[subgroup_column].isin(subgroup_values)].copy(deep=True)
            df_subgroup[subgroup_column] = subgroup_code
            df_subgroup = (
                df_subgroup.groupby([*breakdown])
                .sum()
                .reset_index()
                )
            df = pd.concat([df, df_subgroup])

    return df


def add_subgroup_columns(df, subgroup):
    """
    Combines groups of specified columns into a single summed column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    subgroup: dict(str, list)
        Contains new column name that will be assigned to the grouping,
        and the columns that will form the group.

    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    for subgroup_name, subgroup_cols in subgroup.items():
        df[subgroup_name] = df[subgroup_cols].sum(axis=1)

    return df


def order_by_list(df, column, order):
    """
    Orders the dataframe based on a custom list applied to a specified column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    columm: str
        Column name to be ordered on.
    order: list[str]
        List that contains the custom order for the specified column

    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    # Create a dummy df with the required list and the column name to sort on
    dummy = pd.Series(order, name=column).to_frame()

    # Use left merge on the dummy to return a sorted df
    ordered_df = pd.merge(dummy, df, on=column, how='left')

    return ordered_df


def fyear_to_year_start_end(fyear):
    '''
    From a standard financial year (YYYY-YY) creates year start and year end
    outputs in date format (yyyy-mm-dd)

    Parameters
    ----------
    fyear : str
        Financial year in format YYYY-YY

    Returns
    -------
        tuple
    '''
    # Create fy start and end dates from the financial year input
    fy_start = datetime.date(int(fyear[:4]), 4, 1)
    fy_end = datetime.date(int(fyear[:4]) + 1, 3, 31)

    return (fy_start, fy_end)


def filter_for_year(df, year, date_start_col='Date_start', date_end_col='Date_end'):
    """
    Given a year, filters a dataframe for data where the year is between the start
    and end dates given in the dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to be filtered, must have two columns with the start and end dates
        of the dataset. Assumes dates are are datetime64[ns] format
    year : str
        Must be in format YYYY-YY (e.g. 2010-11)
    date_start_col : str, optional
        Name of the column containing the start date information.
        The default is 'Date_start'.
    date_end_col : str, optional
        Name of the column containing the end date information.
        The default is 'Date_end'.

    Returns
    -------
    df: pandas.DataFrame
        Filtered only for values valid for the year given

    """

    # Get start and end of financial year based on year input
    yr_start, yr_end = fyear_to_year_start_end(year)

    # Convert year start and end to datetime64[ns] format from date, to match csv import
    yr_start, yr_end = pd.to_datetime([yr_start, yr_end], dayfirst=True)

    # Filter dataframe to only include rows with a Date_start input of before year start
    df = df[df[date_start_col] <= yr_start]

    # If NaT values are still present, filter to only show rows with these present
    # else, filter to only show rows with a Date_end input later than the year end
    if df[date_end_col].isnull().values.any():
        df = df[df[date_end_col].isnull()]
    else:
        df = df[df[date_end_col] >= yr_end]

    # Drop date start and end columns
    df = df.drop([date_start_col, date_end_col], axis=1)

    return df
