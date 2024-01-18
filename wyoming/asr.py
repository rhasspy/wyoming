"""Speech to text."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import Event, Eventable

DOMAIN = "asr"
_TRANSCRIPT_TYPE = "transcript"
_TRANSCRIBE_TYPE = "transcribe"


@dataclass
class Transcript(Eventable):
    """Transcription response from ASR system"""

    text: str
    """Text transcription of spoken audio"""

    context: Optional[Dict[str, Any]] = None
    """Context for next interaction."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _TRANSCRIPT_TYPE

    def event(self) -> Event:
        return Event(type=_TRANSCRIPT_TYPE, data={"text": self.text})

    @staticmethod
    def from_event(event: Event) -> "Transcript":
        assert event.data is not None
        return Transcript(text=event.data["text"])


@dataclass
class Transcribe(Eventable):
    """Transcription request to ASR system.

    Followed by AudioStart, AudioChunk+, AudioStop
    """

    name: Optional[str] = None
    """Name of ASR model to use"""

    language: Optional[str] = None
    """Language of spoken audio to follow"""

    context: Optional[Dict[str, Any]] = None
    """Context from previous interactions."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _TRANSCRIBE_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {}
        if self.name is not None:
            data["name"] = self.name

        if self.language is not None:
            data["language"] = self.language

        return Event(type=_TRANSCRIBE_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "Transcribe":
        data = event.data or {}
        return Transcribe(name=data.get("name"), language=data.get("language"))
