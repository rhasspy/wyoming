"""Satellite events."""
from dataclasses import dataclass

from .event import Event, Eventable

_RUN_SATELLITE_TYPE = "run-satellite"
_STREAMING_STARTED_TYPE = "streaming-started"
_STREAMING_STOPPED_TYPE = "streaming-stopped"


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


@dataclass
class StreamingStarted(Eventable):
    """Satellite has started streaming audio to server."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _STREAMING_STARTED_TYPE

    def event(self) -> Event:
        return Event(type=_STREAMING_STARTED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "StreamingStarted":
        return StreamingStarted()


@dataclass
class StreamingStopped(Eventable):
    """Satellite has stopped streaming audio to server."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _STREAMING_STOPPED_TYPE

    def event(self) -> Event:
        return Event(type=_STREAMING_STOPPED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "StreamingStopped":
        return StreamingStopped()
