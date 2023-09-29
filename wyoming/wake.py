"""Wake word detection"""
from dataclasses import dataclass
from typing import List, Optional

from .event import Event, Eventable

DOMAIN = "wake"
_DETECTION_TYPE = "detection"
_DETECT_TYPE = "detect"
_NOT_DETECTED_TYPE = "not-detected"


@dataclass
class Detection(Eventable):
    """Wake word was detected."""

    name: Optional[str] = None
    """Name of model."""

    timestamp: Optional[int] = None
    """Timestamp of audio chunk with detection"""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _DETECTION_TYPE

    def event(self) -> Event:
        return Event(
            type=_DETECTION_TYPE, data={"name": self.name, "timestamp": self.timestamp}
        )

    @staticmethod
    def from_event(event: Event) -> "Detection":
        data = event.data or {}
        return Detection(name=data.get("name"), timestamp=data.get("timestamp"))


@dataclass
class Detect(Eventable):
    """Wake word detection request.

    Followed by AudioStart, AudioChunk+, AudioStop
    """

    names: Optional[List[str]] = None
    """Names of models to detect (None = any)."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _DETECT_TYPE

    def event(self) -> Event:
        return Event(type=_DETECT_TYPE, data={"names": self.names})

    @staticmethod
    def from_event(event: Event) -> "Detect":
        data = event.data or {}
        return Detect(names=data.get("names"))


@dataclass
class NotDetected(Eventable):
    """Audio stream ended before wake word was detected."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _NOT_DETECTED_TYPE

    def event(self) -> Event:
        return Event(type=_NOT_DETECTED_TYPE)

    @staticmethod
    def from_event(event: Event) -> "NotDetected":
        return NotDetected()
