"""Audio output to speakers."""
from dataclasses import dataclass

from .event import Event, Eventable

_PLAYED_TYPE = "played"


@dataclass
class Played(Eventable):
    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _PLAYED_TYPE

    def event(self) -> Event:
        return Event(type=_PLAYED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "Played":
        return Played()
