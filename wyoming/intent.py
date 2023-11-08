"""Intent recognition and handling."""
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from .event import Event, Eventable

DOMAIN = "intent"
_RECOGNIZE_TYPE = "recognize"
_INTENT_TYPE = "intent"
_NOT_RECOGNIZED_TYPE = "not-recognized"


@dataclass
class Entity:
    name: str
    value: Optional[Any] = None


@dataclass
class Recognize(Eventable):
    text: str
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _RECOGNIZE_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {"text": self.text}
        if self.context is not None:
            data["context"] = self.context
        return Event(type=_RECOGNIZE_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "Recognize":
        assert event.data is not None
        return Recognize(text=event.data["text"], context=event.data.get("context"))


@dataclass
class Intent(Eventable):
    name: str
    entities: List[Entity] = field(default_factory=list)
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _INTENT_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {"name": self.name}
        if self.entities:
            data["entities"] = [asdict(entity) for entity in self.entities]
        if self.text is not None:
            data["text"] = self.text
        if self.context is not None:
            data["context"] = self.context

        return Event(type=_INTENT_TYPE, data=data)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Intent":
        entity_dicts = data.get("entities")
        if entity_dicts:
            entities: List[Entity] = [
                Entity(**entity_dict) for entity_dict in entity_dicts
            ]
        else:
            entities = []

        return Intent(
            name=data["name"],
            entities=entities,
            text=data.get("text"),
            context=data.get("context"),
        )

    @staticmethod
    def from_event(event: Event) -> "Intent":
        assert event.data is not None
        return Intent.from_dict(event.data)

    def to_rhasspy(self) -> Dict[str, Any]:
        return {
            "intent": {
                "name": self.name,
            },
            "entities": [
                {"entity": entity.name, "value": entity.value}
                for entity in self.entities
            ],
            "slots": {entity.name: entity.value for entity in self.entities},
        }


@dataclass
class NotRecognized(Eventable):
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _NOT_RECOGNIZED_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {}
        if self.text is not None:
            data["text"] = self.text
        if self.context is not None:
            data["context"] = self.context

        return Event(type=_NOT_RECOGNIZED_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "NotRecognized":
        assert event.data is not None
        return NotRecognized(
            text=event.data.get("text"), context=event.data.get("context")
        )
