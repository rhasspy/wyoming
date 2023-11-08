"""Intent recognition and handling."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import Event, Eventable

DOMAIN = "handle"
_HANDLED_TYPE = "handled"
_NOT_HANDLED_TYPE = "not-handled"


@dataclass
class Handled(Eventable):
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _HANDLED_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {}
        if self.text is not None:
            data["text"] = self.text
        if self.context is not None:
            data["context"] = self.context

        return Event(type=_HANDLED_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "Handled":
        assert event.data is not None
        return Handled(text=event.data.get("text"), context=event.data.get("context"))


@dataclass
class NotHandled(Eventable):
    text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _NOT_HANDLED_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {}
        if self.text is not None:
            data["text"] = self.text
        if self.context is not None:
            data["context"] = self.context

        return Event(type=_NOT_HANDLED_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "NotHandled":
        assert event.data is not None
        return NotHandled(
            text=event.data.get("text"), context=event.data.get("context")
        )
