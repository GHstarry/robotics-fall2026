# Mission 3

## Specification

Pattern: alternating arcs. Four forward arcs in order: left 45°, right 45°, left 45°, right 45°, each with radius 0.30 m. Robot body frame: +x forward, positive angular_z turns left.

Speeds: linear_x = 0.15 m/s for all arcs, which is below the 0.22 m/s limit. angular_z = +0.50 rad/s for left arcs and −0.50 rad/s for right arcs, which is below the 0.80 rad/s limit. Radius = v/|ω| = 0.15/0.50 = 0.30 m.

Durations: each arc turns π/4 rad, so t = (π/4)/0.50 ≈ 1.571 s per arc and ≈ 6.28 s in total. This is well under 30 s per segment and 60 s total.

Stopping: build_pattern returns only the four arc segments. The course wrapper publishes zero velocity after the last segment, so the robot should stop and stay still.

Success criteria: each arc has radius 0.30 ± 0.02 m and turns ±π/4 ± 0.04 rad with the signs +, −, +, −. The final heading is 0 rad (facing the start direction). The ideal endpoint is about (0.85, 0.35) m from the start, which fits in the 2 m × 2 m area. All speeds stay within limits, and the command after the last segment is zero. Live checkpoints fall within 0.15 m and 0.20 rad. An unknown pattern name raises ValueError.

## Saved Specification

Pattern: alternating arcs. Four forward arcs in order: left 45°, right 45°, left 45°, right 45°, each with radius 0.30 m. Robot body frame: +x forward, positive angular_z turns left.

Speeds: linear_x = 0.15 m/s for all arcs, which is below the 0.22 m/s limit. angular_z = +0.50 rad/s for left arcs and −0.50 rad/s for right arcs, which is below the 0.80 rad/s limit. Radius = v/|ω| = 0.15/0.50 = 0.30 m.

Durations: each arc turns π/4 rad, so t = (π/4)/0.50 ≈ 1.571 s per arc and ≈ 6.28 s in total. This is well under 30 s per segment and 60 s total.

Stopping: build_pattern returns only the four arc segments. The course wrapper publishes zero velocity after the last segment, so the robot should stop and stay still.

Success criteria: each arc has radius 0.30 ± 0.02 m and turns ±π/4 ± 0.04 rad with the signs +, −, +, −. The final heading is 0 rad (facing the start direction). The ideal endpoint is about (0.85, 0.35) m from the start, which fits in the 2 m × 2 m area. All speeds stay within limits, and the command after the last segment is zero. Live checkpoints fall within 0.15 m and 0.20 rad. An unknown pattern name raises ValueError.

## Assigned Pattern

alternating_arcs

## Original Prompt

Pattern: alternating arcs. Four forward arcs in order: left 45°, right 45°, left 45°, right 45°, each with radius 0.30 m. Robot body frame: +x forward, positive angular_z turns left.

Speeds: linear_x = 0.15 m/s for all arcs, which is below the 0.22 m/s limit. angular_z = +0.50 rad/s for left arcs and −0.50 rad/s for right arcs, which is below the 0.80 rad/s limit. Radius = v/|ω| = 0.15/0.50 = 0.30 m.

Durations: each arc turns π/4 rad, so t = (π/4)/0.50 ≈ 1.571 s per arc and ≈ 6.28 s in total. This is well under 30 s per segment and 60 s total.

Stopping: build_pattern returns only the four arc segments. The course wrapper publishes zero velocity after the last segment, so the robot should stop and stay still.

Success criteria: each arc has radius 0.30 ± 0.02 m and turns ±π/4 ± 0.04 rad with the signs +, −, +, −. The final heading is 0 rad (facing the start direction). The ideal endpoint is about (0.85, 0.35) m from the start, which fits in the 2 m × 2 m area. All speeds stay within limits, and the command after the last segment is zero. Live checkpoints fall within 0.15 m and 0.20 rad. An unknown pattern name raises ValueError.

This is a ROS 2 Jazzy Python package. Implement only build_pattern(pattern_name: str) -> list[Segment] for 'alternating_arcs' in the existing pattern.py.
The course-provided pattern_node.py calls this function, publishes the returned segments repeatedly through /student_cmd_vel, and sends the final zero command.
Use the existing Segment class with linear_x (m/s), angular_z (rad/s), and duration (s).
Return the ordered segments for the assigned specification and raise ValueError for an unknown pattern name.
Stay within 0.22 m/s, 0.80 rad/s, 30 seconds per segment, and 60 seconds total.
Do not replace the wrapper or course checks. Explain assumptions and propose tests.

## Original Output

Assumptions

Frame and signs. Segments are in the robot body frame: +x forward, and positive angular_z turns left (counter-clockwise), as in ROS REP 103. A left 45° arc uses ω > 0 and a right 45° arc uses ω < 0.
Arc geometry. Each arc is a single segment with constant linear_x and angular_z. Radius R = v/|ω| and turn angle Δθ = ω·t. With v = 0.15 m/s and |ω| = 0.50 rad/s, R = 0.30 m, and each 45° arc takes (π/4)/0.50 = π/2 ≈ 1.571 s.
Exact durations. The duration is computed from π, not typed as 1.571, so the ideal turn angle is exactly π/4. The rounded value would be off by about 0.0002 rad per arc, which is small but avoidable.
No stop segment. The list contains only the four arcs. The wrapper publishes zero velocity afterwards, so adding a zero segment here would duplicate its job.
Ideal model. The segments describe the ideal path. The simulated robot accelerates and decelerates, and the wrapper publishes at a fixed rate, so the measured path will differ slightly. The live tolerances (0.15 m, 0.20 rad) cover that difference.
Pattern names. build_pattern only needs to support alternating_arcs. Every other name, including the other two course patterns, raises ValueError instead of returning a guess.
pattern.py


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

    Supported assignments are ``rounded_rectangle``, ``l_path``, and
    ``alternating_arcs``. Do not include the final stop; the ROS wrapper always
    publishes it and the evaluator verifies it.
    """
    if pattern_name != "alternating_arcs":
        raise ValueError(f"Unsupported pattern: {pattern_name!r}")

    # Left, right, left, right: positive angular_z turns left.
    return [
        Segment(linear_x=ARC_SPEED, angular_z=sign * ARC_TURN_RATE, duration=ARC_DURATION)
        for sign in (1, -1, 1, -1)
    ]
Proposed tests

Segment order and signs: there are exactly 4 segments, every linear_x > 0, and the signs of angular_z are +, −, +, −.
Radius and angle: for each segment, linear_x / abs(angular_z) is 0.30 ± 0.02 m and abs(angular_z) * duration is π/4 ± 0.04 rad.
Final heading: the sum of angular_z * duration over all segments is 0 ± 0.04 rad, so the robot faces its starting direction.
Endpoint: integrating the arcs from (0, 0, 0) ends at about (0.85, 0.35) m.
Limits: every |linear_x| ≤ 0.22, every |angular_z| ≤ 0.80, every 0 < duration ≤ 30, and the total duration is at most 60 s.
Stop: command_at(segments, total_duration) from the course checks.py returns (0.0, 0.0).
Unknown pattern: build_pattern("zigzag") raises ValueError.

## Original Source

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

    Supported assignments are ``rounded_rectangle``, ``l_path``, and
    ``alternating_arcs``. Do not include the final stop; the ROS wrapper always
    publishes it and the evaluator verifies it.
    """
    if pattern_name != "alternating_arcs":
        raise ValueError(f"Unsupported pattern: {pattern_name!r}")

    # Left, right, left, right: positive angular_z turns left.
    return [
        Segment(linear_x=ARC_SPEED, angular_z=sign * ARC_TURN_RATE, duration=ARC_DURATION)
        for sign in (1, -1, 1, -1)
    ]

## Assumptions

Claude had already given the assumptions without my asking it:
Frame and signs. Segments are in the robot body frame: +x forward, and positive angular_z turns left (counter-clockwise), as in ROS REP 103. A left 45° arc uses ω > 0 and a right 45° arc uses ω < 0.

Arc geometry. Each arc is a single segment with constant linear_x and angular_z. Radius R = v/|ω| and turn angle Δθ = ω·t. With v = 0.15 m/s and |ω| = 0.50 rad/s, R = 0.30 m, and each 45° arc takes (π/4)/0.50 = π/2 ≈ 1.571 s.

Exact durations. The duration is computed from π, not typed as 1.571, so the ideal turn angle is exactly π/4. The rounded value would be off by about 0.0002 rad per arc, which is small but avoidable.

No stop segment. The list contains only the four arcs. The wrapper publishes zero velocity afterwards, so adding a zero segment here would duplicate its job.

Ideal model. The segments describe the ideal path. The simulated robot accelerates and decelerates, and the wrapper publishes at a fixed rate, so the measured path will differ slightly. The live tolerances (0.15 m, 0.20 rad) cover that difference.

Pattern names. build_pattern only needs to support alternating_arcs. Every other name, including the other two course patterns, raises ValueError instead of returning a guess.

## Problems

The first thing I checked was the names, if they were named anything other than 'alternating_arcs' it would spit out an error. 

## Test Plan

For a pattern behavior test, we run build_pattern("alternating_arcs") and check each part to compare results. Expected results have 4 segments with each linear_x at .15 > 0 and angular_z signs + then -.

For velocity-limit testing, we loop over every segment and check the limits. Expected results have linear_x <= .22 m/s as well as angular_z <= .8 rad/s for each of the 4 segments. Each duration should also be within 0 and 30 seconds.

The stop test uses the command_at(segments, t) function at the start of and after the pattern. The expected results should have the variable t = 6.2 while still returning the last arc's command and at a later time it should return (0.0, 0.0). 

## Modifications

Rewrote the docstring to only the one that is implemented and have other names raise ValueError.

## Live Pending

True

## Evidence Analysis

All tests pass. test_my_pattern_geometry shows each arc moves forward with radius .3 += .02 m and turns pi/4 += .04 rads. test_my_pattern_order shows there are four arcs turning left then right then left then right. I changed one fo the signs to see if it would catch the mistake and it indeed did. 

## Ai Disclosure

I used Claude throughout mission 3. I used it to draft up my specification as well as the student tests. I reviewed the code against the specifications as well as the course limits. I saw that it had changed the docstring to only accept alternating_arcs and verified that it was indeed correct.

## Live Issue

Similar error to what I got last time. I reopened gazebo and reran the program. 
