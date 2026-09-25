"""AI-assisted motion pattern implementation.

Preserve the original AI response in Streamlit. Review it, then implement a safe
version here. The node accepts only segments returned by ``build_pattern``.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Segment:
    linear_x: float
    angular_z: float
    duration: float

ARC_SPEED = 0.15          # m/s, below the 0.22 m/s limit
ARC_TURN_RATE = 0.50      # rad/s, below the 0.80 rad/s limit
ARC_ANGLE = math.pi / 4   # 45 degrees per arc
ARC_DURATION = ARC_ANGLE / ARC_TURN_RATE  # about 1.571 s; radius = 0.15 / 0.50 = 0.30 m

def build_pattern(pattern_name: str) -> list[Segment]:
    """Return ordered, bounded motion segments for the assigned pattern.

    Only ``alternating_arcs`` (this student's assignment) is implemented:
    four forward arcs of radius 0.30 m turning +45, -45, +45, -45 degrees.
    Any other name, including the other course patterns, raises ValueError.
    Do not include the final stop; the ROS wrapper always publishes it and
    the evaluator verifies it.
    """
    if pattern_name != "alternating_arcs":
        raise ValueError(f"Unsupported pattern: {pattern_name!r}")

    # Left, right, left, right: positive angular_z turns left.
    return [
        Segment(linear_x=ARC_SPEED, angular_z=sign * ARC_TURN_RATE, duration=ARC_DURATION)
        for sign in (1, -1, 1, -1)
    ]
