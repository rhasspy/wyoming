"""Support for voice timers."""

from dataclasses import dataclass
from typing import Optional

from .event import Event, Eventable

DOMAIN = "timer"
_STARTED_TYPE = "timer-started"
_UPDATED_TYPE = "timer-updated"
_CANCELLED_TYPE = "timer-cancelled"
_FINISHED_TYPE = "timer-finished"


@dataclass
class TimerStarted(Eventable):
    """New timer was started."""

    id: str
    """Unique id of timer."""

    total_seconds: int
    """Total number of seconds the timer will run for."""

    name: Optional[str] = None
    """Optional name provided by user."""

    start_hours: Optional[int] = None
    """Number of hours users requested the timer to run for."""

    start_minutes: Optional[int] = None
    """Number of minutes users requested the timer to run for."""

    start_seconds: Optional[int] = None
    """Number of minutes users requested the timer to run for."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _STARTED_TYPE

    def event(self) -> Event:
        data = {"id": self.id, "total_seconds": self.total_seconds}
        if self.name is not None:
            data["name"] = self.name

        if self.start_hours is not None:
            data["start_hours"] = self.start_hours

        if self.start_minutes is not None:
            data["start_minutes"] = self.start_minutes

        if self.start_seconds is not None:
            data["start_seconds"] = self.start_seconds

        return Event(
            type=_STARTED_TYPE,
            data=data,
        )

    @staticmethod
    def from_event(event: Event) -> "TimerStarted":
        return TimerStarted(
            id=event.data["id"],
            total_seconds=event.data["total_seconds"],
            name=event.data.get("name"),
            start_hours=event.data.get("start_hours"),
            start_minutes=event.data.get("start_minutes"),
            start_seconds=event.data.get("start_seconds"),
        )


@dataclass
class TimerUpdated(Eventable):
    """Existing timer was paused, resumed, or had time added or removed."""

    id: str
    """Unique id of timer."""

    is_active: bool
    """True if timer is running."""

    total_seconds: int
    """Number of seconds left on the timer."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _UPDATED_TYPE

    def event(self) -> Event:
        return Event(
            type=_UPDATED_TYPE,
            data={
                "id": self.id,
                "is_active": self.is_active,
                "total_seconds": self.total_seconds,
            },
        )

    @staticmethod
    def from_event(event: Event) -> "TimerUpdated":
        return TimerUpdated(
            id=event.data["id"],
            is_active=event.data["is_active"],
            total_seconds=event.data["total_seconds"],
        )


@dataclass
class TimerCancelled(Eventable):
    """Existing timer was cancelled."""

    id: str
    """Unique id of timer."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _CANCELLED_TYPE

    def event(self) -> Event:
        return Event(
            type=_CANCELLED_TYPE,
            data={"id": self.id},
        )

    @staticmethod
    def from_event(event: Event) -> "TimerCancelled":
        return TimerCancelled(id=event.data["id"])


@dataclass
class TimerFinished(Eventable):
    """Existing timer finished without being cancelled."""

    id: str
    """Unique id of timer."""

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _FINISHED_TYPE

    def event(self) -> Event:
        return Event(
            type=_FINISHED_TYPE,
            data={"id": self.id},
        )

    @staticmethod
    def from_event(event: Event) -> "TimerFinished":
        return TimerFinished(id=event.data["id"])
