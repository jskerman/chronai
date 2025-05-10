import random
from datetime import datetime, timedelta
from uuid import UUID

import pandas as pd
import pytest

from chronai.core.constants import EVENT_ASAT_COLUMN, EVENT_CATEGORY_COLUMN, EVENT_TEXT_COLUMN, SESSION_ID_COLUMN
from chronai.sessionization._core import _BaseConsecutiveSessionization


class RandomConsecutiveSessionizer(_BaseConsecutiveSessionization):
    """
    Simple implementation: starts a new session randomly with a 50% chance
    """

    def _is_in_same_session(self, *, event_a: pd.Series, event_b: pd.Series) -> bool:
        return random.random() > 0.5


@pytest.fixture
def sample_events():
    base_time = datetime(2024, 1, 1, 12, 0, 0)
    return pd.DataFrame(
        [
            {EVENT_ASAT_COLUMN: base_time, EVENT_CATEGORY_COLUMN: "A", EVENT_TEXT_COLUMN: "Text"},
            {
                EVENT_ASAT_COLUMN: base_time + timedelta(minutes=10),
                EVENT_CATEGORY_COLUMN: "A",
                EVENT_TEXT_COLUMN: "Text",
            },
            {
                EVENT_ASAT_COLUMN: base_time + timedelta(minutes=40),
                EVENT_CATEGORY_COLUMN: "A",
                EVENT_TEXT_COLUMN: "Text",
            },  # new session
            {
                EVENT_ASAT_COLUMN: base_time + timedelta(minutes=50),
                EVENT_CATEGORY_COLUMN: "A",
                EVENT_TEXT_COLUMN: "Text",
            },
        ]
    )


def test_sessionize_adds_column(sample_events):
    sessionizer = RandomConsecutiveSessionizer()
    result = sessionizer.sessionize(events_df=sample_events)

    assert SESSION_ID_COLUMN in result.columns
    assert len(result) == 4


def test_session_ids_are_valid_uuids(sample_events):
    sessionizer = RandomConsecutiveSessionizer()
    result = sessionizer.sessionize(events_df=sample_events)

    for sid in result[SESSION_ID_COLUMN]:
        UUID(sid)  # Will raise ValueError if not a valid UUID


def test_does_not_mutate_input_df(sample_events):
    original_df = sample_events.copy(deep=True)
    sessionizer = RandomConsecutiveSessionizer()
    _ = sessionizer.sessionize(events_df=sample_events)

    pd.testing.assert_frame_equal(sample_events, original_df)
