"""Public filtering API backed by the frozen preprocessing implementation."""

from .variability_analysis.signal_processing import (
    ProcessedRecording,
    central_difference,
    preprocess_recording,
    zero_phase_bandpass,
)

__all__ = [
    "ProcessedRecording",
    "central_difference",
    "preprocess_recording",
    "zero_phase_bandpass",
]

