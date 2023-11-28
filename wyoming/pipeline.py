"""Pipeline events."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from .event import Event, Eventable

_RUN_PIPELINE_TYPE = "run-pipeline"


class PipelineStage(str, Enum):
    """Stages of a pipeline."""

    WAKE = "wake"
    ASR = "asr"
    INTENT = "intent"
    HANDLE = "handle"
    TTS = "tts"


@dataclass
class RunPipeline(Eventable):
    """Run a pipeline"""

    start_stage: PipelineStage
    end_stage: PipelineStage

    name: Optional[str] = None
    """Name of pipeline to run"""

    def __post_init__(self) -> None:
        start_valid = True
        end_valid = True

        if self.start_stage == PipelineStage.WAKE:
            if self.end_stage not in (
                PipelineStage.WAKE,
                PipelineStage.ASR,
                PipelineStage.INTENT,
                PipelineStage.HANDLE,
                PipelineStage.TTS,
            ):
                end_valid = False
        elif self.start_stage == PipelineStage.ASR:
            if self.end_stage not in (
                PipelineStage.ASR,
                PipelineStage.INTENT,
                PipelineStage.HANDLE,
                PipelineStage.TTS,
            ):
                end_valid = False
        elif self.start_stage == PipelineStage.INTENT:
            if self.end_stage not in (
                PipelineStage.INTENT,
                PipelineStage.HANDLE,
                PipelineStage.TTS,
            ):
                end_valid = False
        elif self.start_stage == PipelineStage.HANDLE:
            if self.end_stage not in (
                PipelineStage.HANDLE,
                PipelineStage.TTS,
            ):
                end_valid = False
        elif self.start_stage == PipelineStage.TTS:
            if self.end_stage not in (PipelineStage.TTS,):
                end_valid = False
        else:
            start_valid = False

        if not start_valid:
            raise ValueError(f"Invalid start stage: {self.start_stage}")

        if not end_valid:
            raise ValueError(f"Invalid end stage: {self.end_stage}")

    @staticmethod
    def is_type(event_type: str) -> bool:
        return event_type == _RUN_PIPELINE_TYPE

    def event(self) -> Event:
        data: Dict[str, Any] = {
            "start_stage": self.start_stage.value,
            "end_stage": self.end_stage.value,
        }

        if self.name is not None:
            data["name"] = self.name

        return Event(type=_RUN_PIPELINE_TYPE, data=data)

    @staticmethod
    def from_event(event: Event) -> "RunPipeline":
        assert event.data is not None
        return RunPipeline(
            start_stage=PipelineStage(event.data["start_stage"]),
            end_stage=PipelineStage(event.data["end_stage"]),
            name=event.data.get("name"),
        )
