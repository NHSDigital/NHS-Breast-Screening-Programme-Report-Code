import xlwings as xw
import win32com.client as win32
import PIL
from PIL import ImageGrab, Image
import bs_code.parameters as param
import datetime
import bs_code.utilities.helpers as helpers
import logging


def define_labels(tag, year):
    """
    Creates label strings based on tag and year inputs. Used to populate labels
    in external files where the cells contain the tags defined in this function.

    Parameters
    ----------
    tag : str
        Tag that is used to lookup the required label
    year : str
        Reporting year used to populate elements of the label
    Returns
    -------
    label: str
    """

    # Create all the required year ranges
    year_previous = (str(int(year[0:4])-1)
                     + "-"
                     + str(int(year[5:7])-1))
    year_range_11 = helpers.get_year_range(year, 11)
    year_range_2 = helpers.get_year_range(year, 2)
    start_year_11 = min(year_range_11)
    start_year_2 = min(year_range_2)
    calendar_year = "20" + str(int(year[5:7]))
    calendar_year_previous = "20" + str(int(year[5:7])-1)
    calendar_year_range_11 = [str(int(x[0:4])+1) for x in year_range_11]

    # Set default label for if Excel tag does not match any of the tags below
    label = "invalid_tag"

    # Define the titles/headers based on the tag required
    if tag == "subtitle_year":
        label = "England, " + year
    if tag == "subtitle_year_end":
        label = "England, as at 31 March " + calendar_year
    if tag == "subtitle_timeseries_11":
        label = "England, " + start_year_11 + " to " + year
    if tag == "subtitle_timeseries_2":
        label = "England, " + start_year_2 + " to " + year
    if tag == 'header_year':
        label = year
    if tag == 'header_year_previous':
        label = year_previous
    if tag == 'header_year_range_11':
        label = year_range_11
    if tag == 'header_calendar_year_range_11':
        label = calendar_year_range_11
    if tag == "header_year_end":
        label = "As at 31 March " + calendar_year
    if tag == "header_year_end_previous":
        label = "As at 31 March " + calendar_year_previous
    if tag == 'header_year_change':
        label = year_previous + " to " + year

    # Define the copyright labels based on the tag required
    if tag == "copyright_ons":
        label = "Copyright © {year}, population estimates re-used with the permission of The Office for National Statistics.".format(year=str(datetime.date.today().year))
    if tag == "copyright_hscic":
        label = "Copyright © {year}, Health and Social Care Information Centre".format(year=str(datetime.date.today().year))
    if tag == "copyright_nhse":
        label = "Copyright © {year}, NHS England".format(year=str(datetime.date.today().year))
    if tag == "copyright_nhsd":
        label = "The Health and Social Care Information Centre is a non-departmental body created by statute, also known as NHS Digital."

    return label


def add_labels(filename):
    """
    Adds labels to an output file based on tags read in from cells within a
    specified range (set here as A1:P200). Checks all worksheets in the file.

    Parameters
    ----------
    filename : path
        Filepath of the Excel file that contains the cells to be updated.
    Returns
    -------
        None
    """

    logging.info(
        "Writing labels to file"
        )

    # Set the year to be used in label definitions
    year = param.YEAR

    # Load Excel template
    wb = xw.Book(filename)

    for sheet in wb.sheets:
        sht = wb.sheets[sheet]
        sht.select()
        # Define the cell range to be checked for each of the worksheets
        endrow = sht.range('A200').end('up').last_cell.row+1
        check_range = "A1:P"+str(endrow)
        cells = sht.range(check_range)
        # For each cell in the range, check for tags and apply labels
        for cell in cells:
            check = str(sht.range(cell).value)
            if check == "":
                pass
            elif check.startswith("tag_"):
                tag = check[4:]
                sht.range(cell).value = define_labels(tag, year)


def save_tables(source_file):
    """
    Save updated table template to the final data tables folder

    Parameters
    ----------
    source_file : path
        Filepath of the Excel file that contains the tables to be saved.
    Returns
    -------
        None
    """
    logging.info(
        "Saving final publication tables"
        )

    # Select the master tables file
    xw.App()
    wb = xw.books.open(source_file)

    # Save the tables to the publication folder, named as per the report year
    save_name = "breast-screening-programme-eng-" + param.YEAR + "-tab.xlsx"
    savepath = param.TAB_DIR / save_name
    wb.save(savepath)

    # Remove any worksheets that are not published based on the parameter input list
    delete_sheets = param.TABLES_REMOVE
    sheets_in_file = [sht.name for sht in wb.sheets]
    for sheet in delete_sheets:
        if sheet in sheets_in_file:
            sheet_to_delete = wb.sheets[sheet]
            sheet_to_delete.delete()

    # Add the labels to each sheet based on the tags in the master file
    add_labels(savepath)

    # Return to the title sheet, re-save and closed Excel
    sht = wb.sheets["Contents"]
    sht.select()
    wb.save()
    xw.apps.active.api.Quit()


def resize_image(image, size_factor):
    """
    Resizes a saved image based on a sizing (multiplying) factor

    Parameters
    ----------
    image : path
        Location of the image
    size_factor: int
        The factor by which the image length and width will be multiplied by
    Returns
    -------
        Resized image
    """
    # Extract the current length and width of the image
    length_x, width_y = image.size
    # Multiply the length and width by the factor
    size = int(size_factor * length_x), int(size_factor * width_y)
    # Apply the new sizing to the image
    image_resize = image.resize(size, Image.ANTIALIAS)

    return image_resize


def save_charts_as_image(source_file,
                         output_path=param.CHART_DIR, image_type="png",
                         size_factor=1.5):
    """
    Save updated charts as images to the final charts folder. The function
    will loop through all tabs / charts in the specified file and save each
    to the output folder.

    Parameters
    ----------
    source_file : path
        File location of the Excel file that contains the charts to be saved.
    output_path : path
        Folder location where the images should be saved.
    image_type: str
        Type of image file to create. Tested for jpeg (jpg) and png file types.
        Default is png.
    size_factor: int
        The factor by which the image length and width will be multiplied by.
        If set to 1 then no resizing will take place.
    Returns
    -------
        None
    """
    logging.info(
        "Saving final publication charts"
        )
    # Activate the chart master file using win32 (to allow selection of chart objects)
    app = win32.gencache.EnsureDispatch("Excel.Application")
    app.WindowState = win32.constants.xlMaximized
    wb = app.Workbooks.Open(Filename=source_file)

    # Create a list of all the worksheets in the file
    sheet_names = [sheet.Name for sheet in wb.Sheets]

    # For each worksheet, write the chart as the specified type, named as
    # per the worksheet.
    for sheet in sheet_names:
        sht = wb.Worksheets[sheet]
        for chartObject in sht.ChartObjects():
            chartObject.Copy()
            image = ImageGrab.grabclipboard()
            # Resize the image if the size factor is not 1
            if size_factor != 1:
                image = resize_image(image, size_factor)

            # Save the image to the output folder as a png, named as per the
            # source worksheet
            output_file = sheet + "." + image_type
            output_image = output_path / output_file
            image.save(output_image, 'png')
            pass
