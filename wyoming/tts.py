"""Text to speech."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import Event, Eventable

DOMAIN = "tts"
_SYNTHESIZE_TYPE = "synthesize"


@dataclass
class SynthesizeVoice:
    """Information about the desired voice for synthesis."""

    name: Optional[str] = None
    """Voice name from tts info (overrides language)."""

    language: Optional[str] = None
    """Voice language from tts info."""

    speaker: Optional[str] = None
    """Voice speaker from tts info."""

    def to_dict(self) -> Dict[str, str]:
        if self.name is not None:
            voice = {"name": self.name}
            if self.speaker is not None:
                voice["speaker"] = self.speaker
        elif self.language is not None:
            voice = {"language": self.language}
        else:
            voice = {}

        return voice

    @staticmethod
    def from_dict(voice: Dict[str, Any]) -> "Optional[SynthesizeVoice]":
        if "name" in voice:
            return SynthesizeVoice(
                name=voice["name"],
                speaker=voice.get("speaker"),
            )

        if "language" in voice:
            return SynthesizeVoice(name=voice["language"])

        return None


@dataclass
class Synthesize(Eventable):
    """Request to synthesize audio from text."""

    text: str
    """Text to synthesize."""

    voice: Optional[SynthesizeVoice] = None
    """Voice to use during synthesis."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _SYNTHESIZE_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {"text": self.text}
        if self.voice is not None:
            data["voice"] = self.voice.to_dict()

        return Event(type=_SYNTHESIZE_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "Synthesize":
        assert event.data is not None
        return Synthesize(
            text=event.data["text"],
            voice=SynthesizeVoice.from_dict(event.data.get("voice", {})),
        )
