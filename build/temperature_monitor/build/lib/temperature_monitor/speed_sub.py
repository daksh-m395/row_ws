import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('speed_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            '/robot_speed',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        speed = msg.data

        if speed > 1.5:
            self.get_logger().info(f'FAST! {speed:.2f} m/s')
        elif speed >= 0.5 or speed <=1.5:
            self.get_logger().info(f'NORMAL! {speed:.2f} m/s')
        else:
            self.get_logger().info(f'SLOW: {speed:.2f} m/s')

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
