import math
import os
import unittest
from week03_pattern.checks import command_at, endpoint, validate
from week03_pattern.pattern import build_pattern

RADIUS = 0.30
ARC_ANGLE = math.pi / 4


class MyPatternTests(unittest.TestCase):
    def setUp(self):
        self.segments = build_pattern(os.environ.get("WEEK03_ASSIGNED_PATTERN", "alternating_arcs"))

    def test_my_pattern_geometry(self):
        # Each arc: radius 0.30 +/- 0.02 m and a 45 degree turn +/- 0.04 rad.
        for segment in self.segments:
            self.assertGreater(segment.linear_x, 0)
            self.assertAlmostEqual(segment.linear_x / abs(segment.angular_z), RADIUS, delta=0.02)
            self.assertAlmostEqual(abs(segment.angular_z) * segment.duration, ARC_ANGLE, delta=0.04)

    def test_my_pattern_order(self):
        # Four arcs turning left, right, left, right (positive angular_z = left).
        self.assertEqual(len(self.segments), 4)
        signs = [math.copysign(1, segment.angular_z) for segment in self.segments]
        self.assertEqual(signs, [1, -1, 1, -1])


if __name__ == "__main__":
    unittest.main()
