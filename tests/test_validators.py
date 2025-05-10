from datetime import datetime

import pandas as pd
import pytest

from chronai.core.constants import EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, EVENT_TEXT_COLUMN
from chronai.core.validators import validate_df_columns, validate_event_df_columns


def test_validate_df_columns_allows_nans():
    df = pd.DataFrame(
        {"integers": [1, None, 3], "strings": ["a", "b", "c"], "datetimes": [datetime.now(), None, datetime.now()]}
    )

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_df_columns_missing_column():
    df = pd.DataFrame({"integers": [1, None, 3], "strings": ["a", "b", "c"]})

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    with pytest.raises(ValueError):
        fn(df)


def test_validate_df_columns_extra_column():
    df = pd.DataFrame(
        {
            "integers": [1, 2, 3],
            "strings": ["a", "b", "c"],
            "datetimes": [datetime.now(), datetime.now(), datetime.now()],
            "extra_column": [10, 20, 30],
        }
    )

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_df_columns_missing_multiple_columns():
    df = pd.DataFrame({"strings": ["a", "b", "c"]})

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    with pytest.raises(ValueError):
        fn(df)


def test_validate_df_columns_empty_dataframe():
    df = pd.DataFrame()

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    with pytest.raises(ValueError):
        fn(df)


def test_validate_df_columns_correct_columns_no_type_validation():
    df = pd.DataFrame(
        {
            "integers": [1, 2, 3],
            "strings": ["a", "b", "c"],
            "datetimes": [datetime.now(), datetime.now(), datetime.now()],
        }
    )

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_df_columns_none_values():
    df = pd.DataFrame({"integers": [None, None, None], "strings": [None, None, None], "datetimes": [None, None, None]})

    @validate_df_columns("df", {"integers", "strings", "datetimes"})
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_event_df_columns_valid():
    df = pd.DataFrame(
        {
            EVENT_ASAT_COLUMN: [1, 2, 3],
            EVENT_CATEGORY_COLUMN: ["A", "B", "C"],
            EVENT_TEXT_COLUMN: ["text1", "text2", "text3"],
        }
    )

    @validate_event_df_columns("df")
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_event_df_columns_missing_column():
    df = pd.DataFrame({EVENT_ASAT_COLUMN: [1, 2, 3], EVENT_CATEGORY_COLUMN: ["A", "B", "C"]})

    @validate_event_df_columns("df")
    def fn(df: pd.DataFrame):
        return True

    with pytest.raises(ValueError):
        fn(df)


def test_validate_event_df_columns_extra_column():
    df = pd.DataFrame(
        {
            EVENT_ASAT_COLUMN: [1, 2, 3],
            EVENT_CATEGORY_COLUMN: ["A", "B", "C"],
            EVENT_TEXT_COLUMN: ["text1", "text2", "text3"],
            "extra_column": [10, 20, 30],
        }
    )

    @validate_event_df_columns("df")
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)


def test_validate_event_df_columns_empty_dataframe():
    df = pd.DataFrame()

    @validate_event_df_columns("df")
    def fn(df: pd.DataFrame):
        return True

    with pytest.raises(ValueError):
        fn(df)


def test_validate_event_df_columns_none_values():
    df = pd.DataFrame(
        {
            EVENT_ASAT_COLUMN: [None, None, None],
            EVENT_CATEGORY_COLUMN: [None, None, None],
            EVENT_TEXT_COLUMN: [None, None, None],
        }
    )

    @validate_event_df_columns("df")
    def fn(df: pd.DataFrame):
        return True

    assert fn(df)
