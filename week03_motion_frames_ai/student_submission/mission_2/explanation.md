# Mission 2

## Frame Context

The rear-camera transform stays fixed because it is bolted to the robot's body so it moves with 'base_link'. The relation between the two don't change. The hallway camera is fixed somewhere in the environment and the transform changes whenever the robot moves because the hallway camera is following the robot.

## Initial Prompt

Write ROS 2 Python code that converts a point detected by the hallway camera into the robot's base_link frame.

## Initial Output

Here's a ROS 2 Python node that subscribes to points detected by the hallway camera and uses tf2 to convert them into the robot's base_link frame.


import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs  # registers PointStamped with tf2


class HallwayCameraToBaseLink(Node):
    def __init__(self):
        super().__init__('hallway_camera_to_base_link')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.subscription = self.create_subscription(
            PointStamped,
            '/hallway_camera/detected_point',
            self.point_callback,
            10,
        )
        self.publisher = self.create_publisher(
            PointStamped,
            '/detected_point/base_link',
            10,
        )

    def point_callback(self, msg: PointStamped):
        try:
            transformed = self.tf_buffer.transform(
                msg,
                'base_link',
                timeout=Duration(seconds=0.1),
            )
        except Exception as e:
            self.get_logger().warn(f'Could not transform point: {e}')
            return

        p = transformed.point
        self.get_logger().info(
            f'Point in base_link: x={p.x:.2f}, y={p.y:.2f}, z={p.z:.2f}'
        )
        self.publisher.publish(transformed)


def main(args=None):
    rclpy.init(args=args)
    node = HallwayCameraToBaseLink()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
How it works

The TransformListener fills the Buffer with transforms published on /tf and /tf_static.
Each incoming PointStamped carries its source frame in header.frame_id, for example hall_camera.
tf_buffer.transform() finds the chain of transforms from the camera frame to base_link and applies it to the point.
The node logs the converted point and publishes it on /detected_point/base_link.
To run it, add it to a package, register it as a console_scripts entry point in setup.py, build the workspace, and run:

ros2 run <your_package> hallway_camera_to_base_link
You can test it by publishing a point by hand:


ros2 topic pub --once /hallway_camera/detected_point geometry_msgs/msg/PointStamped \
  "{header: {frame_id: 'hall_camera'}, point: {x: 1.0, y: 0.0, z: 0.0}}"

## Initial Source

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs  # registers PointStamped with tf2


class HallwayCameraToBaseLink(Node):
    def __init__(self):
        super().__init__('hallway_camera_to_base_link')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.subscription = self.create_subscription(
            PointStamped,
            '/hallway_camera/detected_point',
            self.point_callback,
            10,
        )
        self.publisher = self.create_publisher(
            PointStamped,
            '/detected_point/base_link',
            10,
        )

    def point_callback(self, msg: PointStamped):
        try:
            transformed = self.tf_buffer.transform(
                msg,
                'base_link',
                timeout=Duration(seconds=0.1),
            )
        except Exception as e:
            self.get_logger().warn(f'Could not transform point: {e}')
            return

        p = transformed.point
        self.get_logger().info(
            f'Point in base_link: x={p.x:.2f}, y={p.y:.2f}, z={p.z:.2f}'
        )
        self.publisher.publish(transformed)


def main(args=None):
    rclpy.init(args=args)
    node = HallwayCameraToBaseLink()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

## Snapshot

{'schema_version': 2, 'captured_at': '2026-09-25T03:58:57.887011+00:00', 'frames': ['odom', 'base_link', 'base_scan', 'rear_camera_link', 'hall_camera'], 'frame_chain': ['hall_camera', 'odom', 'base_link', 'base_scan', 'rear_camera_link'], 'transforms': {'base_scan_to_base_link': {'translation': {'x': -0.032, 'y': 0.0, 'z': 0.172}, 'yaw': 0.0}, 'rear_camera_to_base_link': {'translation': {'x': -0.18, 'y': 0.0, 'z': 0.22}, 'yaw': -3.1415926535795866}, 'hall_camera_to_base_link': {'translation': {'x': -1.3137233340063073, 'y': 2.2896418604499855, 'z': 1.1900000000000002}, 'yaw': -0.9475771532331756}}, 'point_prompts': {'hall_camera_point': 'Transform point (0.5, 0.0, 0.0) from hall_camera to base_link.'}, 'transformed_points': {'scan_point_in_base': {'x': 0.968, 'y': 0.0}, 'rear_camera_point_in_base': {'x': -1.18, 'y': -1.0206624774663903e-11}, 'hall_camera_point_in_base': {'x': -1.021897253322135, 'y': 1.883639965586778}}, 'source': 'live'}

## Initial Analysis

The code never checks that the header.frame_id is a hall_camera. The assumes to use the message's timestamp. The node also creates its own buffer and does not take on the fact that odometer may drift. Doesn't publish to /cmd_vel and assumes to make a publisher.

## Improved Changes

It now requires the source frame to be 'hall_camera' and raises 'ValueError' otherwise. It also keeps its own timestamp. Requires it to use the supplied tf_buffer with no hard-coded offsets and returns 'None' when the transform is unavailable. 

## Live Pending

True

## Synthesis

The initial AI output assumed many things in order to get the job done. It invented input and output topic names. It never made sure that the point came from 'hall_camera' as well as creating its own buffer which is empty on start. its test command sent a 0 timestamp so tf2 would use the most recent timestamp rather than the one that it should have. The improved prompt narrowed the code to just one function. It rejected any frame other than 'hall_camera' and returned 'ValueError'. If the wrong transform were to be used around people, a person that is detected by the hallway camera could be placed in the incorrect spot and as such, the robot could believe that where the person is is open space. 'test_uses_buffer_result_including_rotation', 'test_uses_camera_as_source_and_body_as_target', and 'test_rejects_wrong_source_frame' detects these problems. The robot should slow down or stop until it begins to receive valid transforms again as well as logging what went wrong.

## Live Issue

The five course tests pass however running 'ros2 topic echo /clock --once' shows that the simulator uses sim time (sec : 14726). 
