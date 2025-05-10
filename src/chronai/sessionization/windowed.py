from datetime import timedelta

from pandas.core.api import Series as Series

from chronai.core.constants import EVENT_ASAT_COLUMN
from chronai.sessionization._core import _BaseConsecutiveSessionization


class WindowedSessionization(_BaseConsecutiveSessionization):
    """
    Sessionization strategy based on a fixed time window.

    This class implements a windowed sessionization approach where
    two consecutive events are considered to be in the same session
    if the time difference between them is less than or equal to a
    configurable time window.

    This is useful for time series data such as user search histories
    where temporal proximity indicates related intent.

    Attributes
    ----------
        window_size_seconds (int): Duration (in seconds) to define the session window.
    """

    def __init__(self, window_size_seconds: int = 1800):
        """
        Initialize the sessionizer with a time window.

        Args:
            window_size_seconds (int): Number of seconds defining the maximum
                allowed time gap between consecutive events in the same session.
                Defaults to 1800 seconds (30 minutes).
        """
        self.window = timedelta(seconds=window_size_seconds)

    def _is_in_same_session(self, *, event_a: Series, event_b: Series) -> bool:
        """
        Determine whether two events occur within the same session window.

        Two events are considered to be part of the same session if the time
        difference between them is less than or equal to the configured time window.

        Args:
            event_a (Series): The current event.
            event_b (Series): The previous event.

        Returns
        -------
            bool: True if the events are within the configured time window,
                  False otherwise.
        """
        delta = event_b[EVENT_ASAT_COLUMN] - event_a[EVENT_ASAT_COLUMN]
        return delta <= self.window
