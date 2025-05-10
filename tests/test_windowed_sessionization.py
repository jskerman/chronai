from datetime import datetime

import pandas as pd
import pytest

from chronai.core.constants import EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, EVENT_TEXT_COLUMN
from chronai.sessionization.windowed import WindowedSessionization


@pytest.fixture
def sample_events():
    """Fixture to generate a sample DataFrame of events."""
    data = [
        {
            EVENT_CATEGORY_COLUMN: 1,
            EVENT_TEXT_COLUMN: "blah",
            EVENT_ASAT_COLUMN: datetime(2025, 5, 8, 9, 0, 0),
        },
        {
            EVENT_CATEGORY_COLUMN: 1,
            EVENT_TEXT_COLUMN: "blah",
            EVENT_ASAT_COLUMN: datetime(2025, 5, 8, 9, 30, 0),
        },
        {
            EVENT_CATEGORY_COLUMN: 1,
            EVENT_TEXT_COLUMN: "blah",
            EVENT_ASAT_COLUMN: datetime(2025, 5, 8, 10, 31, 45),
        },
    ]
    return pd.DataFrame(data)


def test_windowed_sessionization_default_window(sample_events):
    """Test the default 30-minute window for sessionization using sessionize."""
    sessionizer = WindowedSessionization(window_size_seconds=1800)

    # Apply sessionization to the sample events
    sessionized_df = sessionizer.sessionize(events_df=sample_events)

    # Check that the session IDs are assigned as expected
    assert sessionized_df.loc[0, "session_id"] == sessionized_df.loc[1, "session_id"]
    assert sessionized_df.loc[1, "session_id"] != sessionized_df.loc[2, "session_id"]
