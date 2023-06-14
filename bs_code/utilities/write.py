"""
Purpose of the script: contains the Excel automation script.
"""
import pandas as pd
import xlwings as xw
import bs_code.parameters as param
from bs_code.utilities import processing, helpers
import logging


def add_footnote_refs(sheetname, start_cell, org_col_letter,
                      region_col_letter=None,
                      ref_file=param.REF_FOOTNOTES,
                      output_path=param.TABLE_TEMPLATE,
                      sheetname_column="sheetname",
                      footnote_column="footnote_ref"):
    """
    This function uses a tailored Breast Screening project reference data file to add
    footnote references to cell values in a specified sheet/column, based on input
    reference data.
    Used for organisation tables where existing footnote refs in the master file
    are over-written when writing the output.

    Parameters
    ----------
    sheetname : str
        Name of the destination Excel worksheet.
    start_cell: str
        Identifies the cell location in the Excel worksheet that contains the
        start position of the values to be checked.
    org_col_letter: str
        Excel column letter that contains the organisation names requiring
        footnote refs to be added, which will be matched against details in
        the ref_file.
    region_col_letter: str
        Excel column letter that contains the region details (code or name)
        that can be used in addition to the organisation name for matching
        with details in the ref_file. Optional input.
    ref_file : Path
        Filepath of the csv that contains reference data with the footnotes
        to be added. Expects the file to contain the sheetname that is
        to be updated, lookup columns used to locate the organisation to be
        updated, and a 'footnote_ref' column containing the footnote reference
        to be added to the organisation name.
    output_path : Path
        Filepath of the Excel file that contains the cells to be updated.
    sheetname_column: str
        Name of the column in the csv reference file that contains the worksheet
        name that identifies which set of footnotes from the ref file are to be
        added (will be cross checked against the sheetname parameter)
    footnote_column: str
        Name of the column in the csv reference file that contains the footnote
        reference.
    Returns
    -------
    None
    """
    logging.info(f"Updating footnote references in {sheetname}")

    # Import the reference data to be imported
    df_ref_data = pd.read_csv(ref_file, index_col=None)
    # Filter the reference data dataframe based on the sheet to be updated
    df_ref_data = df_ref_data[df_ref_data[sheetname_column] == sheetname]

    # Select the workbook and worksheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Check if there is a region column to also check when assigning footnotes
    if region_col_letter is not None:
        region_check = True
    else:
        region_check = False

    # Select the Excel column numbers that hold the organisation names (and
    # region if applicable) that are to be checked and edited.
    org_col_num = helpers.excel_col_letter_to_col_num(org_col_letter)
    if region_check:
        region_col_num = helpers.excel_col_letter_to_col_num(region_col_letter)

    # Select the start row number based on the start cell
    row_start = helpers.excel_cell_to_row_num(start_cell)
    # Working down from the start cell, find the last cell that contains data
    row_stop = sht.range(start_cell).end('down').last_cell.row + 1

    # For each row in the data range, check if the values in the columns to be
    # checked are present in the reference file.
    # Where there is no region to be checked, then only the org value will
    # be used
    for row in range(row_start, row_stop):
        values_to_update = df_ref_data.copy()
        check_org = sht.range(row, org_col_num).value
        if region_check:
            check_region = sht.range(row, region_col_num).value
        else:
            check_region = check_org
        values_to_update = values_to_update[(values_to_update.isin([check_org])
                                             .any(axis=1)) &
                                            (values_to_update.isin([check_region])
                                             .any(axis=1))]
        # If they are present then add the superscripted footnote ref
        if values_to_update.empty:
            pass
        else:
            # Extract the footnote reference value and check its length
            fn_ref = values_to_update[footnote_column].values[0]
            fn_length = len(fn_ref)
            # Add the footnote ref to the organisation name and replace the
            # original Excel value
            org_with_fn = check_org + fn_ref
            sht.range(row, org_col_num).value = org_with_fn
            # Use the original string length to check the footnote ref start position
            fn_start = len(org_with_fn) - fn_length
            # Update the footnote ref to superscript
            sht.range(row, org_col_num).characters[fn_start:fn_start+fn_length].api.Font.Superscript = True


def insert_empty_columns(df, empty_cols, write_cell):
    '''
    Inserts empty columns into the dataframe based on where any empty columns
    are located in Excel.
    When inserting columns, the function exludes the index so the index should
    only include columns that are not to be pasted into Excel.

    Parameters
    ----------
    df : pandas.DataFrame
    empty_cols: list[str]
        A list of letters representing any empty Excel columns in the target
        worksheet.
        Default is None
    write_cell: str
        Cell where the dataframe content will be writen to, used for reference
        when coverting the column letter to a dataframe column number.

    Returns
    -------
    df : pandas.DataFrame
    '''

    # For each Excel column letter, convert to a relative numeric dataframe position
    # and insert an empty column in the dataframe.
    # The function takes into account the starting column in Excel (based on write_cell)
    # as its base (0)
    for col in empty_cols:
        col_num = helpers.excel_col_to_df_col(col, write_cell)
        df.insert(col_num, col_num, "")

    return df


def write_to_excel_static(df, output_path, sheetname, write_cell,
                          empty_cols=None):
    """
    Write data to an excel template. Assumes the table length remains constant.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        Identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
    empty_cols: list[str]
        A list of letters representing any empty (section separator) Excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.

    Returns
    -------
    None
    """

    logging.info(f"Writing data to {sheetname}")
    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = insert_empty_columns(df, empty_cols, write_cell)

    # Write to the specified cell
    sht.range(write_cell).value = df.values


def write_to_excel_variable(df, output_path, sheetname, write_cell,
                            empty_cols=None):
    """
    Write data to an Excel template. Can accommodate dataframes where the
    number of rows may change e.g. LA data where the number of LAs may change
    each year.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        Identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
        This should be the first cell in the master file where the variable
        data currently exists, as it also determines which row to delete first
        e.g. for LAs would be the first cell of the first row of LA data
    empty_cols: list[str]
        A list of letters representing any empty (section separator) Excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.
    Returns
    -------
    None
    """

    logging.info(f"Writing data to {sheetname}")
    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = insert_empty_columns(df, empty_cols, write_cell)

    # Get Excel row number of write cell
    firstrownum = helpers.excel_cell_to_row_num(write_cell)

    # Get Excel row number of last row of existing data
    lastrownum_current = sht.range(write_cell).end('down').row

    # Clear all existing data rows from write_cell to end of data
    delete_rows = str(firstrownum) + ":" + str(lastrownum_current)
    sht.range(delete_rows).delete()

    # Count number of rows in dataframe
    df_rowcount = len(df)

    # Create range for new set of rows and insert into sheet
    lastrownnum_new = firstrownum + df_rowcount - 1
    df_rowsrange = str(firstrownum) + ":" + str(lastrownnum_new)

    sht.range(df_rowsrange).insert(shift='down')

    # Write dataframe to the Excel sheet starting at the write_cell reference
    sht.range(write_cell).value = df.values


def write_to_excel_sheet(df, output_path, sheetname):
    """
    Writes a dataframe to cell A1 of an existing Excel worksheet, clearing any
    existing data first.

    Parameters
    ----------
    df :pandas.DataFrame
    output_path: Path
        Folder path where output will be written.
    sheetname: str
        Name of worksheet to be written to.

    Returns
    -------
    None

    """
    logging.info(f"Writing data to {sheetname}")

    # Load Excel template
    wb = xw.Book(output_path)

    # Select the required sheet and clear the contents
    sht = wb.sheets[sheetname]
    sht.select()
    sht.clear_contents()

    # Write the dataframe to cell A1
    sht.range('A1').value = df


def write_csv(df, output_path, output_name):
    """
    Writes a dataframe to a csv

    Parameters
    ----------
    df :pandas.DataFrame
    output_path: Path
        Folder path where output will be written.
    output_name: str
        Name to be asssigned to output file name.

    Returns
    -------
    .csv file

    """
    # Set full file path / name
    file_name = output_name + ".csv"
    save_path = output_path / file_name

    # Save dataframe to csv
    df.to_csv(save_path, index=False)


def select_write_type(df, write_type, output_path, output_name,
                      write_cell=None, empty_cols=None):
    """
    Determines which type of write function is needed and performs that
    function.

    Parameters
    ----------
    df :pandas.DataFrame
    write_type: str
        Determines the method of writing the output.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    output_name: str
        Name of the worksheet to be written to (for Excel) or to be asssigned
        as the name of the output file (for csv's).
    write_cell: str
        Identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data). Not required if the write_type is
        csv.
    empty_cols: list[str]
        A list of letters representing any empty (section separator) Excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Not required if the write_type is
        csv.

    Returns
    -------
    .csv file

    """
    # Check for invalid write_type agrument
    valid_values = ["csv", "excel_static", "excel_variable", "excel_sheet"]
    helpers.validate_value_with_list("write_type", write_type, valid_values)

    # If write_type is csv, then write the output to a csv
    if write_type == "csv":
        write_csv(df, output_path, output_name)

    # If write_type is excel_variable, then use the variable write to Excel method
    elif write_type == "excel_variable":
        write_to_excel_variable(df, output_path, output_name,
                                write_cell, empty_cols)
    # If write_type is excel_static, then use the static write to Excel method
    elif write_type == "excel_static":
        write_to_excel_static(df, output_path, output_name,
                              write_cell, empty_cols)

    # If write_type is excel_sheet, then use the write to Excel worksheet method
    elif write_type == "excel_sheet":
        write_to_excel_sheet(df, output_path, output_name)


def write_outputs(df, output_args, output_path,
                  not_applicable=param.NOT_APPLICABLE):
    """
    Processes and writes the data for each function to the output location
    as defined by parameters taken from the output_args dictionary.

    Parameters
    ----------
    df :pandas.DataFrame
    output_args: dictionary
        Provides all the required arguments needed to run and write each
        output: name, write_type, write_cell, empty_cols and the function(s)
        that create the data.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    not_applicable: str
        Replacement value for nulls created during the concatenation of
        multiple dataframes for one output. Default is the project default.

    Returns
    -------
    None

    """
    # For each item in the output_args dictionary
    for output in output_args:
        # Extract all the required arguments from the output_args dictionary
        # Some arguments are not needed if the write_type is csv
        name = output["name"]
        write_type = output["write_type"]

        if write_type == "csv":
            write_cell = None
            empty_cols = None
        if write_type == "excel_sheet":
            write_cell = "A1"
            empty_cols = None
        else:
            write_cell = output["write_cell"]
            empty_cols = output["empty_cols"]

        logging.info(f"Running {output['contents']} to {name}")

        # Run the function(s) in the contents item.
        # Where there are multiple functions in the contents for one output,
        # the returned dataframes are concatenated. For unmatched columns null
        # values will be created (e.g. for tidy csvs where different measures
        # are presented at different org levels)
        df_output = pd.concat([content(df) for content in output["contents"]])

        # Perform any final updates to the dataframe for specific outputs
        df_final = processing.output_specific_updates(df_output, name)

        # Replace remaining nulls with the required 'not_applicable' replacement
        # value.
        df_final = df_final.fillna(not_applicable)

        # Write the output as per the selected write type
        select_write_type(df_final, write_type, output_path,
                          name, write_cell, empty_cols)
