import pandas as pd
import numpy as np
from bs_code.utilities import pre_processing


def test_combine_small_las():
    """
    Tests the combine_small_las function, which combines small LAs to
    neighbouring LAs for non-disclosure purposes (currently City of London and
    Isles of Scilly)
    """
    ORG_UPDATE = {"Org_ONSCode": ["E09000001", "E06000053"],
                  "Org_ONSCode_New": ["E09000012", "E06000052"],
                  "Org_Name": ["City of London", "Isles of Scilly"],
                  "Org_Name_New": ["Hackney", "Cornwall"]}

    input_df = pd.DataFrame(
        {
            "Org_ONSCode": ["E09000001", "E09000001", "E09000012", "E06000053",
                            "E06000052", "E06000047", "E10000006"],
            "Org_Name": ["CITY OF LONDON", "City of London", "Hackney",
                         "Isles of Scilly", "Cornwall", "County Durham",
                         "Cumbria"]
            }
        )

    expected = pd.DataFrame(
        {
            "Org_ONSCode": ["E09000012", "E09000012", "E09000012",
                            "E06000052", "E06000052", "E06000047", "E10000006"],
            "Org_Name": ["Hackney", "Hackney", "Hackney", "Cornwall",
                         "Cornwall", "County Durham", "Cumbria"]
            }
        )

    actual = pre_processing.combine_small_las(
        input_df, ORG_UPDATE
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_update_la_regions():
    """
    Tests the update la regions function
    """

    input_df = pd.DataFrame(
        {
            "CollectionYearRange": ["2011-12", "2012-13", "2013-14", "2015-16",
                                    "2011-12", "2012-13", "2013-14", "2015-16"],
            "Org_ONSCode": ["E06000001", "E06000001", "E06000001", "E06000001",
                            "E06000005", "E06000005", "E06000005", "E06000005"],
            "Parent_Org_Name": ["London", "London", "London", "London",
                                "North West", "North West", "North West", "North West"],
            "Parent_Org_Code": ["A", "A", "A", "A",
                                "C", "C", "C", "C"],
            "Parent_OrgONSCode": ["E12000001", "E12000001", "E12000001", "E12000001",
                                  "E12000009", "E12000009", "E12000009", "E12000009"]
            }
        )

    df_update_info = pd.DataFrame(
        {
            "LA_ONS_Code": ["E06000001"],
            "REP_Parent_Name": ["South West"],
            "REP_Parent_Code": ["B"],
            "REP_Parent_ONS_Code": ["E12000002"],
            "BUSINESS_START_DATE": ["01-04-2013"],
            "BUSINESS_END_DATE": ["NaT"]
            }
        )

    # Change strings to datetime objects
    df_update_info["BUSINESS_START_DATE"] = pd.to_datetime(df_update_info
                                                           ["BUSINESS_START_DATE"],
                                                           dayfirst=True)
    df_update_info["BUSINESS_END_DATE"] = pd.to_datetime(df_update_info
                                                         ["BUSINESS_END_DATE"],
                                                         dayfirst=True)

    expected = pd.DataFrame(
        {
            "CollectionYearRange": ["2011-12", "2012-13", "2013-14", "2015-16",
                                    "2011-12", "2012-13", "2013-14", "2015-16"],
            "Org_ONSCode": ["E06000001", "E06000001", "E06000001", "E06000001",
                            "E06000005", "E06000005", "E06000005", "E06000005"],
            "Parent_Org_Name": ["London", "London", "South West", "South West",
                                "North West", "North West", "North West", "North West"],
            "Parent_Org_Code": ["A", "A", "B", "B",
                                "C", "C", "C", "C"],
            "Parent_OrgONSCode": ["E12000001", "E12000001", "E12000002", "E12000002",
                                  "E12000009", "E12000009", "E12000009", "E12000009"]
            }
        )

    year_range = ["2011-12", "2012-13", "2013-14", "2015-16"]
    actual = pre_processing.update_la_regions(
        input_df,
        df_update_info,
        year_range
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))
