import logging
import bs_code.parameters as param
import bs_code.utilities.data_connections as dbc
import pandas as pd

logger = logging.getLogger(__name__)


def import_asset_data(collection, year_range: list = [param.YEAR]):
    """
    This function will import data filtered by a given year_range from
    the Breast Screening asset SQL database.
    Uses the df_from_sql function

    Parameters
    ----------
    collection : str
        The collection reference (KC62 or KC63)
    year_range: list
        The list of years to return
        defaults to returning YEAR from parameters.py

    Returns
    -------
    pandas.DataFrame

    """
    # Load our parameters
    server = param.SERVER
    database = param.DATABASE
    table = param.TABLE

    sql_folder = r'bs_code\sql_code'

    with open(sql_folder + '\query_asset.sql', 'r') as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<Collection>", collection)
    data = data.replace("<YearRange>", "','".join(year_range))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # If KC63 data for 2012-13 is included, then the LA level data for that
    # year has to be removed (pubished data for that year was based on PCTs but
    # the asset has data for both org types)
    if (collection == "KC63") & ("2012-13" in year_range):
        df = drop_la_data_201213(df)

    return df


def drop_la_data_201213(df):
    """
    The source data asset has data for both Local Authorities and PCTs
    for 2012-13 as it was uploaded for both organisation types.
    This function removes the LA data for that year (published data was based
    on PCT's')

    Parameters
    ----------
    df : pandas.DataFrame that includes org type and collection year.

    Returns
    -------
    pandas.DataFrame

    """
    # Filter out LA data for 2012-13
    df = df[((df["CollectionYearRange"] == "2012-13")
             & (df["Org_Type"] != "LA"))
            | (df["CollectionYearRange"] != "2012-13")]

    return df


def import_la_update_info():
    """
    This function will import data from the LA region file.

    Returns
    -------
    pandas.DataFrame

    """
    # Import excel file
    ref_file = param.LA_UPDATES
    df = pd.read_csv(ref_file, index_col=None,
                     parse_dates=["BUSINESS_START_DATE", "BUSINESS_END_DATE"],
                     dayfirst=True)

    return df
