import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('temperature_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        temp = msg.data

        if temp > 75:
            self.get_logger().error(f'CRITICAL ALERT! {temp:.2f} °C')
        elif temp > 60:
            self.get_logger().warn(f'WARNING! {temp:.2f} °C')
        else:
            self.get_logger().info(f'Normal: {temp:.2f} °C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
