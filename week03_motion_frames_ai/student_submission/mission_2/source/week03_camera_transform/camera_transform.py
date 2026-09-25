"""Mission 2 student implementation.

Complete only ``transform_camera_point`` after preserving the initial AI output
in the guide. Course tests supply both real and simulated TF buffers.
"""
from geometry_msgs.msg import PointStamped
from tf2_ros import TransformException
import tf2_geometry_msgs  # noqa: F401  registers PointStamped with tf2_ros

SOURCE_FRAME = "hall_camera"
TARGET_FRAME = "base_link"

def transform_camera_point(tf_buffer, point: PointStamped) -> PointStamped | None:
    """Return a hall_camera point expressed in base_link, or None if unavailable."""
    # raise NotImplementedError("Mission 2: revise the AI-generated camera transform")

    if point.header.frame_id != SOURCE_FRAME:
        raise ValueError(
            f"Expected a point in '{SOURCE_FRAME}', got '{point.header.frame_id}'"
        )

    try:
        # transform() looks up TF at point.header.stamp, so the result matches
        # the robot pose at the time of the observation.
        return tf_buffer.transform(point, TARGET_FRAME)
    except TransformException:
        return None
