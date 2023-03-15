import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import bs_code.utilities.helpers as helpers


def test_replace_col_value():
    """Tests the replace_col_value function, create replaces all values within a
    column with another value
    """

    input_df = pd.DataFrame(
        {
            "Screened": [100, 200, 100, 500, 800],
            "Non-op_diag_rate_invasive": [0, 1000, 5000, 250, 2000],
            "Non-op_diag_rate_non-invasive": [0, 2000, 2000, 500, 8000],
            "Assement_rate": [98.8, 67.8, 56.8, 100.0, 87.6]
            }
        )

    expected = pd.DataFrame(
        {
            "Screened": [100, 200, 100, 500, 800],
            "Non-op_diag_rate_invasive": [":", ":", ":", ":", ":"],
            "Non-op_diag_rate_non-invasive": [":", ":", ":", ":", ":"],
            "Assement_rate": [98.8, 67.8, 56.8, 100.0, 87.6]
            }
        )

    actual = helpers.replace_col_value(
        input_df,
        col_names=["Non-op_diag_rate_invasive", "Non-op_diag_rate_non-invasive"],
        replace_value=":",
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_remove_rows():
    """Tests the remove rows function, which removes rows from dataframe where
    any column contains a specified value(s)
    """
    input_df = pd.DataFrame(
        {
            "BreakdownA": ["Total", "Group1", "Group2", "Group1", "Group2", "Group2"],
            "BreakdownB": ["Total", "Total", "Total", "Group1", "Group1", "Group2"],
            "MeasureA": [200, 100, 200, 100, 50, 100],
            "MeasureB": [450, 500, 300, 10, 20, 100],
            }
        )

    expected = pd.DataFrame(
        {
            "BreakdownA": ["Group2"],
            "BreakdownB": ["Group2"],
            "MeasureA": [100],
            "MeasureB": [100],
            }
        )

    actual = helpers.remove_rows(
        input_df,
        remove_values=["Total", "Group1"]
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_excel_cell_to_col_num():
    """
   Tests that the excel_cell_to_col_num function works as expected

    """

    cells = ["A1", "D8", "AA1"]

    actual = []
    for cell in cells:
        a = helpers.excel_cell_to_col_num(cell)
        actual.append(a)

    expected = [1, 4, 27]

    assert actual == expected, f"When checking excel_cell_to_col_num expected to find {expected} but found {actual}"


def test_excel_col_letter_to_col_num():
    """
   Tests that the excel_col_letter_to_col_num function works as expected

    """

    letters = ["A", "D", "AA"]

    actual = []
    for letter in letters:
        a = helpers.excel_col_letter_to_col_num(letter)
        actual.append(a)

    expected = [1, 4, 27]

    assert actual == expected, f"When checking excel_col_letter_to_col_num expected to find {expected} but found {actual}"


def test_excel_col_to_df_col():
    """
   Tests that the excel_col_to_df_col function works as expected

    """
    write_cell = "B10"
    cols = ["C", "E", "AA"]

    actual = []
    for col in cols:
        a = helpers.excel_col_to_df_col(col, write_cell)
        actual.append(a)

    expected = [1, 3, 25]

    assert actual == expected, f"When checking excel_col_to_df_col expected to find {expected} but found {actual}"


def test_low_numerator_warning():
    """
    Tests the low_numerator warning function, which adds a flag column when
    the numerator for a calculated field is below a defined level. New column
    is named as per the calculated field + "_warning".
    """

    input_df = pd.DataFrame(
        {
            "Rate_benign_biopsy": [np.nan, 0.8, 0.2, 1.5],
            "Benign_biopsy": [0, 15, 25, 200],
            }
        )

    expected = pd.DataFrame(
        {
            "Rate_benign_biopsy": [np.nan, 0.8, 0.2, 1.5],
            "Benign_biopsy": [0, 15, 25, 200],
            "Rate_benign_biopsy_warning": ["!", "!", "", ""]
            }
        )

    actual = helpers.low_numerator_warning(
        input_df,
        calculated_column="Rate_benign_biopsy",
        numerator_column="Benign_biopsy",
        low=25,
        flag="!",
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_add_percent_or_rate():
    """
    Tests the add_percent_or_rate function, which adds a calculated percentage
    or rate to the dataframe based on defined inputs.
    """

    input_df = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0]
            }
        )

    expected = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0],
            "New_Col_Name": [50, 12.5, 25, np.nan]}
        )

    actual = helpers.add_percent_or_rate(
        input_df,
        new_column_name="New_Col_Name",
        numerator="Numerator_Col",
        denominator="Denominator_Col",
        multiplier=100)

    pd.testing.assert_frame_equal(actual, expected)


def test_add_percent_or_rate_no_multiplier():
    """
    Tests the add_percent_or_rate function, which adds a calculated percentage
    or rate to the dataframe based on defined inputs. This version tests the
    function when no multiplier is supplied.
    """

    input_df = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0]
            }
        )

    expected = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0],
            "New_Col_Name": [0.5, 0.125, 0.25, np.nan]}
        )

    actual = helpers.add_percent_or_rate(
        input_df,
        new_column_name="New_Col_Name",
        numerator="Numerator_Col",
        denominator="Denominator_Col")

    pd.testing.assert_frame_equal(actual, expected)


def test_add_column_difference():
    """
    Tests the add_column_difference function, which adds a column with the
    difference between the last 2 columns in the dataframe.
    """

    input_df = pd.DataFrame(
        {
            "Region": ["A", "B", "C", "D", "E"],
            "Col1": [100, 800, 100, 0, 5],
            "Col2": [100, 0, 10, np.nan, 3],
            "Col3": [100, 50, 5, 5, np.nan]
            }
        )

    expected = pd.DataFrame(
        {
            "Region": ["A", "B", "C", "D", "E"],
            "Col1": [100, 800, 100, 0, 5],
            "Col2": [100, 0, 10, np.nan, 3],
            "Col3": [100, 50, 5, 5, np.nan],
            "New_Col_Name": [0, 50, -5, np.nan, np.nan]}
        )

    actual = helpers.add_column_difference(input_df,
                                           new_column_name="New_Col_Name",)

    pd.testing.assert_frame_equal(actual, expected)


def test_new_column_from_check_list():
    """
    Tests the new_column_from_check_list function, which adds a column with the
    content determined by checking the content of an existing column against
    a user defined input.
    """

    input_df = pd.DataFrame(
        {
            "Org_Code": ["AGA", "DCB", "AAA", "DCB", "BLJ"],
            }
        )

    expected = pd.DataFrame(
        {
            "Org_Code": ["AGA", "DCB", "AAA", "DCB", "BLJ"],
            "New_Col_Name": ["True value", "True value", "False value",
                             "True value", "False value"]}
        )

    check_dict = {"New_Col_Name": ["AGA", "DCB", "DZZ"]}

    actual = helpers.new_column_from_check_list(input_df,
                                                check_column="Org_Code",
                                                check_content=check_dict,
                                                value_if_true="True value",
                                                value_if_false="False value")

    pd.testing.assert_frame_equal(actual, expected)


def test_add_percent_of_total():
    """
    Tests the add_percent_of_total function, which adds a new percentage column
    to a column, which contains row based percentage values.
    """

    input_df = pd.DataFrame(
        {
            "Region": ["Grand_total", "A", "B", "C", "D"],
            "Invited": [250, 100, 100, 50, 0]
            }
        )

    expected = pd.DataFrame(
        {
            "Region": ["Grand_total", "A", "B", "C", "D"],
            "Invited": [250, 100, 100, 50, 0],
            "Invited_of_total": [100.0, 40.0, 40.0, 20.0, 0.0]}
        )

    actual = helpers.add_percent_of_total(input_df,
                                          new_col_name="Invited_of_total")

    pd.testing.assert_frame_equal(actual, expected)


def test_add_subtotals():
    """Tests the add_subtotals function, which adds row totals and sub-totals
    to a dataframe for all specified dataframe column combinations.
    """
    input_df = pd.DataFrame(
        {
            "CollectionYearRange": ["2019-20", "2019-20", "2019-20", "2019-20",
                                    "2020-21", "2020-21", "2020-21", "2020-21"],
            "Table_Code": ["A", "B", "C", "D", "A", "B", "C", "D"],
            "Value": [10, 50, 50, 100, 10, 50, 20, 100],
            }
        )

    expected = pd.DataFrame(
        {
            "CollectionYearRange": ["2019-20", "2019-20", "2019-20", "2019-20",
                                    "2020-21", "2020-21", "2020-21", "2020-21",
                                    "Total", "Total", "Total", "Total",
                                    "2019-20", "2020-21",
                                    "Total"],
            "Table_Code": ["A", "B", "C", "D",
                           "A", "B", "C", "D",
                           "A", "B", "C", "D",
                           "Total", "Total",
                           "Total"],
            "Value": [10, 50, 50, 100,
                      10, 50, 20, 100,
                      20, 100, 70, 200,
                      210, 180,
                      390]
            })

    actual = helpers.add_subtotals(
        df=input_df,
        columns=["CollectionYearRange", "Table_Code"],
        total_name="Total"
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_add_subgroup_rows():
    """Tests add_subgroup_rows, which adds extra subgroup rows
    based on the subgroup input. This tests the function using age groups.
    """
    input_df = pd.DataFrame(
        {
            "Parent_Code": ["ENG", "ENG", "ENG", "ENG", "ENG", "ENG"],
            "Row_Def": ["50", "51-52", "60", "65-69", "70", "71-73"],
            "Total": [10, 10, 10, 20, 30, 10]
        }
    )

    expected = pd.DataFrame(
        {
            "Parent_Code": ["ENG", "ENG", "ENG", "ENG", "ENG", "ENG", "ENG", "ENG"],
            "Row_Def": ["50", "51-52", "60", "65-69", "70", "71-73", "50-52", "65-70"],
            "Total": [10, 10, 10, 20, 30, 10, 20, 50]
        }
    )

    actual = helpers.add_subgroup_rows(
        input_df,
        breakdown=["Parent_Code", "Row_Def"],
        subgroup={"Row_Def": {"50-52": ["50", "51-52"],
                              "65-70": ["65-69", "70"]}},
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_add_subgroup_columns():
    """Tests add_subgroup_columns function, which combines groups of columns
    into a single summed column. This tests the function using Table Code
    """
    input_df = pd.DataFrame(
        {
           "A": [0, 10, 10, 20],
           "B": [0, 20, 10, 0],
           "C1": [0, 15, 5, 10],
           "C2": [0, 5, 50, 100],
           "D": [0, 10, 10, 0],
           }
        )

    expected = pd.DataFrame(
        {
            "A": [0, 10, 10, 20],
            "B": [0, 20, 10, 0],
            "C1": [0, 15, 5, 10],
            "C2": [0, 5, 50, 100],
            "D": [0, 10, 10, 0],
            "A and C1": [0, 25, 15, 30],
            "A to C2": [0, 50, 75, 130],
            }
        )

    actual = helpers.add_subgroup_columns(
        input_df,
        subgroup={'A and C1': ['A', 'C1'],
                  'A to C2': ['A', 'B', 'C1', 'C2']
                  }
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_order_by_list():
    """Tests the order_by_list function, which orders a dataframe by a customer
    list based on a specified column within the dataframe.  Tested using region
    codes.
    """
    input_df = pd.DataFrame(
        {
            "Parent_Org_Code": ["A", "B", "D", "E", "F", "G", "H", "J", "K"],
            "Total": [10, 10, 20, 20, 30, 10, 50, 100, 50],
            }
        )

    expected = pd.DataFrame(
        {
            "Parent_Org_Code": ["A", "D", "B", "E", "F", "H", "G", "K", "J"],
            "Total": [10, 20, 10, 20, 30, 50, 10, 50, 100],
            }
        )

    actual = helpers.order_by_list(
        input_df,
        column="Parent_Org_Code",
        order=["A", "D", "B", "E", "F", "H", "G", "K", "J"],
       )

    pd.testing.assert_frame_equal(actual, expected)


def test_fyear_to_year_start_end():
    """
   Tests that the fyear_to_year_start_end function works as expected

    """
    input_value = "2019-20"

    actual_start, actual_end = helpers.fyear_to_year_start_end(input_value)

    expected_start = datetime.strptime("2019-04-01", '%Y-%m-%d').date()
    expected_end = datetime.strptime("2020-03-31", '%Y-%m-%d').date()

    assert actual_start == expected_start, f"When checking fyear_to_year_start_end\
        expected to find {expected_start} but found {actual_start}"
    assert actual_end == expected_end, f"When checking fyear_to_year_start_end\
        expected to find {expected_end} but found {actual_end}"


def test_filter_for_year():
    """
    Tests that the filter_for_year function works as expected

    """

    input_df = pd.DataFrame(
        {
            "Age_band": ["<=44", "45-49", "50-52", "<=44", "45-49", "50-52", "<=44",
                         "45-49", "50-52"],
            "Multiplier": [1, 2, 2, 10, 20, 20, 100, 200, 200],
            "Date_start": ["01-04-2000", "01-04-2000", "01-04-2000", "01-04-2010",
                           "01-04-2010", "01-04-2010", "01-04-2020", "01-04-2020",
                           "01-04-2020"],
            "Date_end": ["31-03-2009", "31-03-2009", "31-03-2009", "31-03-2019",
                         "31-03-2019", "31-03-2019", "NaT", "NaT", "NaT"]
            }
        )

    # Change strings to datetime objects
    input_df["Date_start"] = pd.to_datetime(input_df["Date_start"], dayfirst=True)
    input_df["Date_end"] = pd.to_datetime(input_df["Date_end"], dayfirst=True)

    expected = pd.DataFrame(
        {
            "Age_band": ["<=44", "45-49", "50-52"],
            "Multiplier": [100, 200, 200]
            }
        )

    actual = helpers.filter_for_year(input_df, "2021-22")

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))
