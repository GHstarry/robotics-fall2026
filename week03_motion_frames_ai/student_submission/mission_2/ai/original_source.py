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