import inspect
import os
from collections.abc import Callable

import pandas as pd

from .constants import EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, EVENT_TEXT_COLUMN

# Controls whether DataFrame validation is enabled (default: enabled unless explicitly turned off)
DF_VALIDATION_ENABLED = os.getenv("DF_VALIDATION_ENABLED", "1") == "1"


def validate_df_columns(df_arg: str, required_columns: set[str]):
    """
    Decorator factory to validate that a DataFrame argument contains required columns.

    This is useful for catching errors early in functions that operate on DataFrames
    with expected structure (e.g., for event processing or analytics pipelines).

    Args:
        df_arg (str): Name of the argument in the target function that refers to the DataFrame.
        required_columns (set[str]): A set of column names expected in the DataFrame.

    Returns
    -------
        Callable: A decorator that wraps the target function and performs validation.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if not DF_VALIDATION_ENABLED:
                return func(*args, **kwargs)

            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            if df_arg not in bound.arguments:
                raise ValueError(f"DataFrame argument '{df_arg}' not found in function call.")

            df = bound.arguments[df_arg]
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"Argument '{df_arg}' is not a pandas DataFrame.")

            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing expected columns: {', '.join(missing_columns)}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_event_df_columns(df_arg: str):
    """
    Decorator to validate that an event DataFrame contains required standard columns.

    Specifically, it checks for:
      - EVENT_ASAT_COLUMN (e.g., timestamp)
      - EVENT_CATEGORY_COLUMN (e.g., group or type)
      - EVENT_TEXT_COLUMN (e.g., description or payload)

    This is a specialized version of `validate_df_columns` for event processing pipelines.

    Args:
        df_arg (str): Name of the DataFrame argument in the target function.

    Returns
    -------
        Callable: A decorator that validates the presence of standard event columns.
    """
    return validate_df_columns(
        df_arg=df_arg, required_columns={EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, EVENT_TEXT_COLUMN}
    )
