import pandas as pd
import numpy as np
import bs_code.utilities.field_definitions as field_definitions


def test_women_eligible():
    """
   Tests women_eligible derivation has been implemented correctly

    """

    input_df = pd.DataFrame({"Women_resident": [60, 10, 90, 30, 100],
                             "Women_ineligible": [45, 10, 33, 10, 25]})

    return_df = field_definitions.women_eligible(input_df)

    expected = [15, 0, 57, 20, 75]

    actual = list(return_df['Women_eligible'])

    assert actual == expected, f"When checking for women_eligible expected to find {expected} but found {actual}"


def test_women_never_screened():
    """
   Tests women_never_screened derivation has been implemented correctly

    """

    input_df = pd.DataFrame({"Women_selected_no_screen": [60, 10, 90, 30, 100],
                             "Women_not_selected_not_screened": [45, 10, 33, 10, 25]})

    return_df = field_definitions.women_never_screened(input_df)

    expected = [105, 20, 123, 40, 125]

    actual = list(return_df['Women_never_screened'])

    assert actual == expected, f"When checking for women_never_screened expected to find {expected} but found {actual}"


def test_small_invasive():
    """
    Tests the small_invasive function.
    This function requires "Invasive_lessthan10mm" and "Invasive_10mmto15mm"
    to be included within the columns.
    """

    input_df = pd.DataFrame(
        {
            "Invasive_lessthan10mm": [0, 8, 10, 900, 500],
            "Invasive_10mmto15mm": [0, 300, 400, 600, 300],
            }
        )

    return_df = field_definitions.small_invasive(input_df)

    expected = [0, 308, 410, 1500, 800]

    actual = list(return_df['Small_invasive'])

    assert actual == expected, f"When checking for small_invasive expected to find {expected} but found {actual}"


def test_non_or_micro_invasive():
    """Tests the non_or_micro_invasive function.
    This function requires "Cancer_non_microinvasive" and
    "Cancer_microinvasive" to be included within the columns.
    """

    input_df = pd.DataFrame(
        {
            "Cancer_non_microinvasive": [50, 360, 360, 480, 195],
            "Cancer_microinvasive": [1000, 3000, 4000, 6000, 3000],
            }
        )

    return_df = field_definitions.non_or_micro_invasive(input_df)

    expected = [1050, 3360, 4360, 6480, 3195]

    actual = list(return_df['Non_or_micro_invasive'])

    assert actual == expected, f"When checking for rate non or micro invasive expected to find {expected} but found {actual}"

    
def test_benign_biopsy():
    """
    Tests the total benign biopsy function.
    """

    input_df = pd.DataFrame(
        {
            "Open_biop_RR": [0, 360, 360, 480, 195],
            "Open_biop_STR": [0, 3000, 4000, 6000, 3000],
            }
        )

    return_df = field_definitions.benign_biopsy(input_df)

    expected = [0, 3360, 4360, 6480, 3195]

    actual = list(return_df['Benign_biopsy'])

    assert actual == expected, f"When checking for total benign biopsy expected to find {expected} but found {actual}"


def test_cancers_diagnosed():
    """
    Tests the cancers diagnosed function.
    """

    input_df = pd.DataFrame(
        {
            "Cyt_bio_cancer": [0, 3, 36, 7],
            "Open_biop_cancer": [0, 3, 40, 0],
            }
        )

    return_df = field_definitions.cancers_diagnosed(input_df)

    expected = [0, 6, 76, 7]

    actual = list(return_df['Cancers_diagnosed'])

    assert actual == expected, f"When checking for total cancers diagnosed expected to find {expected} but found {actual}"


def test_sdr_expected():
    """
    Tests the sdr_expected function, which calculates and appends
    SDR_expected values using SDR multiplier ratios from a csv file provided
    by NHSE
    """

    input_df = pd.DataFrame(
        {
            "Table_code": ["A", "B", "A", "B"],
            "Row_Def": ["50-52", "65-69", "70", "70"],
            "Col_Def": ["Screened", "Screened", "Invited", "Invited"],
            "Value": [100, 200, 400, 50]
            }
        )

    expected = pd.DataFrame(
        {
            "Table_code": ["A", "B", "A", "B", "A", "B"],
            "Row_Def": ["50-52", "65-69", "70", "70", "50-52", "65-69"],
            "Col_Def": ["Screened", "Screened", "Invited", "Invited",
                        "SDR_expected", "SDR_expected"],
            "Value": [100, 200, 400, 50, 0.364, 2.152]
            })

    actual = field_definitions.sdr_expected(
        input_df,
        table_code=["A", "B"],
        year="2019-20")

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))
