from typing import List
from .status_event import StatusEvent

_event_history: List[StatusEvent] = []


def add_event(event: StatusEvent):

    _event_history.append(event)


def get_events():

    return _event_history