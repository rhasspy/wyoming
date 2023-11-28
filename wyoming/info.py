"""Information about available services/artifacts."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .event import Event, Eventable
from .util.dataclasses_json import DataClassJsonMixin

DOMAIN = "info"
_DESCRIBE_TYPE = "describe"
_INFO_TYPE = "info"


@dataclass
class Describe(Eventable):
    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _DESCRIBE_TYPE

    def event(self) -> Event:
        return Event(type=_DESCRIBE_TYPE)

    @staticmethod
    def from_event(event: Event) -> "Describe":
        return Describe()


@dataclass
class Attribution(DataClassJsonMixin):
    name: str
    url: str


@dataclass
class Artifact(DataClassJsonMixin):
    name: str
    attribution: Attribution
    installed: bool
    description: Optional[str]


# -----------------------------------------------------------------------------


@dataclass
class AsrModel(Artifact):
    languages: List[str]


@dataclass
class AsrProgram(Artifact):
    models: List[AsrModel]


# -----------------------------------------------------------------------------


@dataclass
class TtsVoiceSpeaker(DataClassJsonMixin):
    name: str


@dataclass
class TtsVoice(Artifact):
    languages: List[str]
    speakers: Optional[List[TtsVoiceSpeaker]] = None


@dataclass
class TtsProgram(Artifact):
    voices: List[TtsVoice]


# -----------------------------------------------------------------------------


@dataclass
class HandleModel(Artifact):
    languages: List[str]


@dataclass
class HandleProgram(Artifact):
    models: List[HandleModel]


# -----------------------------------------------------------------------------


@dataclass
class WakeModel(Artifact):
    languages: List[str]


@dataclass
class WakeProgram(Artifact):
    models: List[WakeModel]


# -----------------------------------------------------------------------------


@dataclass
class IntentModel(Artifact):
    languages: List[str]


@dataclass
class IntentProgram(Artifact):
    models: List[IntentModel]


# -----------------------------------------------------------------------------


@dataclass
class Satellite(Artifact):
    area: Optional[str] = None


# -----------------------------------------------------------------------------


@dataclass
class Info(Eventable):
    asr: List[AsrProgram] = field(default_factory=list)
    tts: List[TtsProgram] = field(default_factory=list)
    handle: List[HandleProgram] = field(default_factory=list)
    intent: List[IntentProgram] = field(default_factory=list)
    wake: List[WakeProgram] = field(default_factory=list)
    satellite: Optional[Satellite] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _INFO_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {
            "asr": [p.to_dict() for p in self.asr],
            "tts": [p.to_dict() for p in self.tts],
            "handle": [p.to_dict() for p in self.handle],
            "intent": [p.to_dict() for p in self.intent],
            "wake": [p.to_dict() for p in self.wake],
        }

        if self.satellite is not None:
            data["satellite"] = self.satellite.to_dict()

        return Event(type=_INFO_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "Info":
        assert event.data is not None

        satellite: Optional[Satellite] = None
        satellite_data = event.data.get("satellite")
        if satellite_data is not None:
            satellite = Satellite.from_dict(satellite_data)

        return Info(
            asr=[AsrProgram.from_dict(d) for d in event.data.get("asr", [])],
            tts=[TtsProgram.from_dict(d) for d in event.data.get("tts", [])],
            handle=[HandleProgram.from_dict(d) for d in event.data.get("handle", [])],
            intent=[IntentProgram.from_dict(d) for d in event.data.get("intent", [])],
            wake=[WakeProgram.from_dict(d) for d in event.data.get("wake", [])],
            satellite=satellite,
        )
