import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperaturePublisher(Node):
    def __init__(self):
        super().__init__('speed_publisher')
        self.publisher_ = self.create_publisher(Float32, '/robot_speed', 10)
        self.timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        msg = Float32()
        msg.data = random.uniform(0.0, 2.0)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data:.2f} m/s')

def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
