"""Satellite events."""
from dataclasses import dataclass

from .event import Event, Eventable

_RUN_SATELLITE_TYPE = "run-satellite"
_PAUSE_SATELLITE_TYPE = "pause-satellite"
_STREAMING_STARTED_TYPE = "streaming-started"
_STREAMING_STOPPED_TYPE = "streaming-stopped"
_SATELLITE_CONNECTED_TYPE = "satellite-connected"
_SATELLITE_DISCONNECTED_TYPE = "satellite-disconnected"


@dataclass
class RunSatellite(Eventable):
    """Informs the satellite that the server is ready to run a pipeline."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _RUN_SATELLITE_TYPE

    def event(self) -> Event:
        return Event(type=_RUN_SATELLITE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "RunSatellite":
        return RunSatellite()


@dataclass
class PauseSatellite(Eventable):
    """Informs the satellite that the server is not ready to run a pipeline."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _PAUSE_SATELLITE_TYPE

    def event(self) -> Event:
        return Event(type=_PAUSE_SATELLITE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "PauseSatellite":
        return PauseSatellite()


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


@dataclass
class SatelliteConnected(Eventable):
    """Satellite has connected to server."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _SATELLITE_CONNECTED_TYPE

    def event(self) -> Event:
        return Event(type=_SATELLITE_CONNECTED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "SatelliteConnected":
        return SatelliteConnected()


@dataclass
class SatelliteDisconnected(Eventable):
    """Satellite has disconnected from server."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _SATELLITE_DISCONNECTED_TYPE

    def event(self) -> Event:
        return Event(type=_SATELLITE_DISCONNECTED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "SatelliteDisconnected":
        return SatelliteDisconnected()
