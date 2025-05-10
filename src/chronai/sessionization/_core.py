import abc
import uuid

import pandas as pd
from tqdm import tqdm

from chronai.core.constants import EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, SESSION_ID_COLUMN
from chronai.core.validators import validate_event_df_columns


class _BaseConsecutiveSessionization(abc.ABC):
    """
    Abstract base class for consecutive sessionization of events.

    This class provides the shared logic for assigning session IDs to a sorted
    sequence of events, based on customizable rules for determining whether
    two consecutive events belong to the same session.

    Subclasses must implement `_is_in_same_session`, which defines the session boundary logic.
    """

    @abc.abstractmethod
    def _is_in_same_session(self, *, event_a: pd.Series, event_b: pd.Series) -> bool:
        """
        Determine whether two events belong to the same session.

        Parameters
        ----------
            event_a (pd.Series): The earlier event.
            event_b (pd.Series): The later event.

        Returns
        -------
            bool: True if the events should be in the same session, False otherwise.
        """
        ...

    @validate_event_df_columns("events_df")
    def sessionize(self, *, events_df: pd.DataFrame, split_by_category: bool = True) -> pd.DataFrame:
        """
        Assigns session IDs to a DataFrame of events based on consecutive logic.

        Events are sorted chronologically (and optionally grouped by category), then
        scanned in order to assign a session ID to each event. A new session starts
        whenever `_is_in_same_session` returns False.

        Parameters
        ----------
            events_df (pd.DataFrame): Input DataFrame with event rows. Must include at least
                the columns defined in EVENT_ASAT_COLUMN and optionally EVENT_CATEGORY_COLUMN.
            split_by_category (bool): Whether to group and sessionize events separately
                by their category (default is True).

        Returns
        -------
            pd.DataFrame: A copy of the input DataFrame with an additional SESSION_ID_COLUMN.
        """
        sort_columns = ([EVENT_CATEGORY_COLUMN] if split_by_category else []) + [EVENT_ASAT_COLUMN]

        sorted_events_df = events_df.sort_values(sort_columns, ascending=True).reset_index(drop=True)
        num_events = len(sorted_events_df)

        session_id = str(uuid.uuid4())
        session_ids = [session_id]

        for index in tqdm(range(1, num_events), desc="Assigning Sessions"):
            previous_event = sorted_events_df.iloc[index - 1]
            current_event = sorted_events_df.iloc[index]

            if not self._is_in_same_session(event_a=previous_event, event_b=current_event):
                session_id = str(uuid.uuid4())
            session_ids.append(session_id)

        sorted_events_df[SESSION_ID_COLUMN] = session_ids
        return sorted_events_df
