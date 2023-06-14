import pandas as pd
import numpy as np
import logging
import bs_code.parameters as param
import bs_code.utilities.field_definitions as definitions
from bs_code.utilities import load, helpers


logger = logging.getLogger(__name__)


def update_la_regions(df, df_la_updates, year_range):
    """
    Will make regional updates to LAs based on the year,
    using information from an imported dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
    df_la_updates : pandas.DataFrame
        Imported dataframe containing updates to be made to LAs
    year_range : list['str']
        List of years to be checked for changes to be applied against

    Returns
    -------
    df : pandas.DataFrame

    """
    logging.info("Applying user defined updates to LA region data ")

    for year in year_range:
        # Filter to find updates relevant to the current year
        df_filt = helpers.filter_for_year(df_la_updates, year,
                                          "BUSINESS_START_DATE",
                                          "BUSINESS_END_DATE")

        if df_filt.empty:
            pass
        else:
            for row in range(len(df_filt)):
                # Obtain the relevant LA_ONS_Code for each row in the dataframe,
                # and update rows which match the current year and LA_ONS_Code with
                # data from the filtered update dataframe
                selection = df_filt.iloc[row]
                la = selection["LA_ONS_Code"]

                df.loc[(df["CollectionYearRange"] == year) & (df["Org_ONSCode"] == la),
                       ["Parent_Org_Name",
                        "Parent_Org_Code",
                        "Parent_OrgONSCode"]] = [df_filt["REP_Parent_Name"].iloc[row],
                                                 df_filt["REP_Parent_Code"].iloc[row],
                                                 df_filt["REP_Parent_ONS_Code"].iloc[row]]

    return df


def combine_small_las(df, lookup):
    """
    Combines small LAs to neighbouring LAs for non-
    disclosive purposes, using a dictionary of old to new org codes and names
    from the paramaters file.
    As they sit in the same region, the parent details do not require updating.
    Replace function uses regex which allows for non direct matching, in this
    case applying the non-case sensitive option.

    Parameters
    ----------
    df : pandas.DataFrame that includes an org code as a variable
    lookup: dict(str, list)
        Dictionary containing the original org code, and the org code and name
        to replace.

    Returns
    -------
    df : pandas.DataFrame
        df with the org codes and names updated as per the values in the
        input dictionary.
    """
    logging.info("Combining small LA's")

    # Create a dataframe from the reference data input
    df_org_update = pd.DataFrame(data=lookup)
    # Add case insensitive prefix used by regex. This ensures that when
    # applying the replace function using regex, it will not be case sensitive
    df_org_update["Org_Name"] = "(?i)" + df_org_update["Org_Name"]
    df_org_update["Org_ONSCode"] = "(?i)" + df_org_update["Org_ONSCode"]

    # Create separate dictionaries for the org code and org name lookups
    df_code_update = dict(zip(df_org_update["Org_ONSCode"],
                              df_org_update["Org_ONSCode_New"]))
    df_name_update = dict(zip(df_org_update["Org_Name"],
                              df_org_update["Org_Name_New"]))

    # Use the dictionaries to update the codes and names in the input dataframe
    df.replace({"Org_ONSCode": df_code_update}, inplace=True, regex=True)
    df.replace({"Org_Name": df_name_update}, inplace=True, regex=True)

    return df


def update_kc63_data(df):
    """
    Applies all pre-processing functions to KC63 data needed prior to creating
    publication outputs (e.g. standardising region names, appending region order
    used in data tables)

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        df with all pre-processing applied to data.

    """
    logging.info("Applying pre-processng updates to KC63 data")

    year_list = helpers.create_year_list(df, "CollectionYearRange")

    # Import data for LA region updates
    df_la_updates = load.import_la_update_info()
    # Update LA region info
    df = update_la_regions(df, df_la_updates, year_list)

    # Update kc63 org names based on dictionary in parameters file
    df.replace({"Org_Name": param.ORG_NAME_UPDATE_KC63}, inplace=True)

    # Update small LA org codes and names as per parameters input
    df = combine_small_las(df, param.ORG_UPDATE_KC63)

    # Add any additional measures (counts) required from field definitions
    df = definitions.add_measures_counts(df, "KC63")

    return df


def update_kc62_data(df):
    """
    Applies all pre-processing functions to KC62 data needed prior to creating
    publication outputs (e.g. standardising region names, appending region order
    used in data tables)

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        df with all pre-processing applied to data.

    """
    logging.info("Applying pre-processng updates to KC62 data")

    # Update old KC62 Q region codes to their equivalent R region
    # codes based on the dictionary in the parameters file
    df.replace({"Parent_Org_Code": param.REGION_UPDATE_KC62}, inplace=True)

    # Update old KC62 region names to their new region names based on the
    # dictionary in the parameters file
    df.replace({"Parent_Org_Name": param.REGION_NAME_UPDATE_KC62}, inplace=True)

    # Update KC62 org names based on dictionary in parameters file
    df.replace({"Org_Name": param.ORG_NAME_UPDATE_KC62}, inplace=True)

    # Add a region order column based on the parameters input that determines
    # how BSU data is ordered.
    df = helpers.new_column_from_lookup(df, "Parent_Org_Code", param.REGION_ORDER_KC62,
                                        "Parent_Org_Order")

    # Add any additional measures (counts) required from field definitions
    df = definitions.add_measures_counts(df, "KC62")

    return df
