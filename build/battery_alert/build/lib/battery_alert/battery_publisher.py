import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class BatteryPublisher(Node):
   def __init__(self):
       super().__init__('battery_publisher')
       self.publisher_ = self.create_publisher(Int32, '/battery_level', 10)
       self.timer = self.create_timer(1.0, self.publish_battery)
       self.battery_level = 100


   def publish_battery(self):
       if self.battery_level >= 0:
           msg = Int32()
           msg.data = self.battery_level
           self.publisher_.publish(msg)


           self.get_logger().info(f'Battery Level: {self.battery_level}%')
           self.battery_level -= 1
       else:
           self.get_logger().info('Battery fully drained')


def main(args=None):
   rclpy.init(args=args)
   node = BatteryPublisher()
   rclpy.spin(node)
   node.destroy_node()
   rclpy.shutdown()
