"""Satellite events."""
from dataclasses import dataclass

from .event import Event, Eventable

_RUN_SATELLITE_TYPE = "run-satellite"


@dataclass
class RunSatellite(Eventable):
    """Tell satellite to start running."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _RUN_SATELLITE_TYPE

    def event(self) -> Event:
        return Event(type=_RUN_SATELLITE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "RunSatellite":
        return RunSatellite()
