import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from fig_data_challenge.main import (
    correct_mispellings,
    drop_rows_blank_or_null,
    return_42,
)


def test_main():
    value = return_42()
    assert value == 42


def test_drop_rows_blank_or_null():
    df_input = pd.DataFrame(
        {
            "column_1": ["1", "2", "3"],
            "column_2": ["4", np.nan, "6"],
            "column_3": ["7", "8", ""],
        }
    )
    df_expected = pd.DataFrame({"column_1": ["1"], "column_2": ["4"], "column_3": ["7"]})

    df_actual = drop_rows_blank_or_null(
        df=df_input, cols=["column_1", "column_2", "column_3"]
    )

    assert_frame_equal(df_expected, df_actual)


def test_correct_mispellings():
    df_input = pd.DataFrame({"column_1": ["hello", "hello", "hwllo"]})
    df_expected = pd.DataFrame({"column_1": ["hello", "hello", "hello"]})

    df_actual = correct_mispellings(
        df=df_input, col="column_1", corrections={"hwllo": "hello"}
    )

    assert_frame_equal(df_expected, df_actual)
