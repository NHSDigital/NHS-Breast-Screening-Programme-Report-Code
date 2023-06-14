import pandas as pd
import numpy as np
from bs_code.utilities import processing


def test_filter_dataframe():
    """Tests the filter_dataframe function, which filters at dataframe by
    mandatory filters (e.g part and collection), the number of years data to be
    used and any additional optional filters (e.g by age).
    """
    input_df = pd.DataFrame(
        {
            "CollectionYearRange": ["2019-20", "2020-21", "2020-21", "2020-21",
                                    "2020-21", "2020-21", "2020-21", "2020-21"],
            "Part": ["1", "1", "1", "2", "1", "1", "1", "1"],
            "Table_Code": ["U", "U", "D", "U", "D", "U", "U", "U"],
            "Row_Def": ["50", "51-52", "60", "50", "51-52", "60", "<45", ">=75"],
            "Total": [10, 50, 50, 100, 10, 50, 20, 100],
            }
        )

    expected = pd.DataFrame(
        {
            "CollectionYearRange": ["2020-21", "2020-21"],
            "Part": ["1", "1"],
            "Table_Code": ["U", "U"],
            "Row_Def": ["51-52", "60"],
            "Total": [50, 50],
            })

    actual = processing.filter_dataframe(
        input_df,
        part=["1"],
        table_code=["U"],
        filter_condition="(Row_Def not in['<45','>=75'])",
        ts_years=1,
        year="2020-21"
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_sort_for_output_defined():
    """
    Tests the sort for output_defined function, which sorts a dataframe
    by the order required for Excel tables.
    """
    input_df = pd.DataFrame(
        {
            "RowDef": ["<45", "45-49", "50-52", "53-54", "55-59", "60-64", "65-69",
                       "70", "71-74", "50-74", "65-70", "53<71"],
            "A": [200, 100, 200, 50, 100, 500, 300, 200, 150, 2350, 500, 1150],
            "B": [450, 500, 300, 100, 50, 250, 600, 100, 60, 1460, 700, 1100],
            }
        )

    expected = pd.DataFrame(
        {
            "RowDef": ["50-74", "65-70", "53<71", "45-49", "50-52", "53-54",
                       "55-59", "60-64", "65-69", "70", "71-74"],
            "A": [2350, 500, 1150, 100, 200, 50, 100, 500, 300, 200, 150],
            "B": [1460, 700, 1100, 500, 300, 100, 50, 250, 600, 100, 60],
            }
        )

    actual = processing.sort_for_output_defined(
        input_df,
        rows=["RowDef"],
        row_order=["50-74", "65-70", "53<71", "45-49", "50-52", "53-54",
                   "55-59", "60-64", "65-69", "70", "71-74"],
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_sort_for_output():
    """
    Tests the sort for output function
    """

    input_df = pd.DataFrame(
        {
            "Org_Name": ["Bolton", "Bradford", "Camden", "Cumbria", "Gateshead",
                         "Hartlepool", "Islington", "Leeds", "Liverpool",
                         "Rotherham", "Tameside", "Westminster"],
            "Parent_OrgONSCode": ["E12000002", "E12000003", "E12000007",
                                  "E12000001", "E12000001", "E12000001",
                                  "E12000007", "E12000003", "E12000002",
                                  "E12000003", "E12000002", "E12000007"],
            "A": [150, 300, 500, 800, 50, 100, 700, 350, 960, 10, 200, 750],
            }
        )

    expected = pd.DataFrame(
        {
            "Org_Name": ["Cumbria", "Gateshead", "Hartlepool", "Bolton",
                         "Liverpool", "Tameside", "Bradford", "Leeds",
                         "Rotherham", "Camden", "Islington", "Westminster"],
            "A": [800, 50, 100, 150, 960, 200, 300, 350, 10, 500, 700, 750],
            }
        )

    actual = processing.sort_for_output(
        input_df,
        sort_on=["Parent_OrgONSCode", "Org_Name"],
        cols_to_remove=['Parent_OrgONSCode'],
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_transpose_for_dashboard():
    """
    Tests transpose_for_dashboard, which splits a dataframe containing local,
    regional and national level measures (previously appended), and instead
    applies the regional and national measures to the local level measures as
    extra columns.
    """
    input_df = pd.DataFrame(
        {
            "CollectionYearRange": ["2020-21", "2020-21", "2020-21", "2020-21",
                                    "2020-21", "2020-21", "2020-21", "2020-21",
                                    "2020-21", "2020-21", "2020-21", "2020-21",
                                    "2020-21", "2020-21"],
            "Parent_Org_Code": ["R1", "R1", "R1", "R1",
                                "R2", "R2", "R2", "R2",
                                "R1", "R1", "R2", "R2",
                                np.nan, np.nan],
            "Org_Name": ["Gateshead", "Gateshead", "Newcastle", "Newcastle",
                         "Crewe", "Crewe", "Liverpool", "Liverpool",
                         np.nan, np.nan, np.nan, np.nan,
                         np.nan, np.nan],
            "Table_CodeDescription": ["First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening"],
            "Uptake": [60.6, 70.4, 75.2, 41.7,
                       70.9, 58.2, 76.7, 54.6,
                       np.nan, np.nan, np.nan, np.nan,
                       np.nan, np.nan],
            "REG_Uptake": [np.nan, np.nan, np.nan, np.nan,
                           np.nan, np.nan, np.nan, np.nan,
                           65.1, 76.5, 56.9, 68.3,
                           np.nan, np.nan],
            "NAT_Uptake": [np.nan, np.nan, np.nan, np.nan,
                           np.nan, np.nan, np.nan, np.nan,
                           np.nan, np.nan, np.nan, np.nan,
                           69.4, 72.8],
        }
    )

    expected = pd.DataFrame(
        {
            "CollectionYearRange": ["2020-21", "2020-21", "2020-21", "2020-21",
                                    "2020-21", "2020-21", "2020-21", "2020-21"],
            "Parent_Org_Code": ["R1", "R1", "R1", "R1",
                                "R2", "R2", "R2", "R2"],
            "Org_Name": ["Gateshead", "Gateshead", "Newcastle", "Newcastle",
                         "Crewe", "Crewe", "Liverpool", "Liverpool"],
            "Table_CodeDescription": ["First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening",
                                      "First and all routine invitations",
                                      "First invitation for routine screening"],
            "Uptake": [60.6, 70.4, 75.2, 41.7,
                       70.9, 58.2, 76.7, 54.6],
            "REG_Uptake": [65.1, 76.5, 65.1, 76.5,
                           56.9, 68.3, 56.9, 68.3],
            "NAT_Uptake": [69.4, 72.8, 69.4, 72.8,
                           69.4, 72.8, 69.4, 72.8],
        }
    )

    actual = processing.transpose_for_dashboard(
        input_df,
        name="Dashboard_Uptake",
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))
