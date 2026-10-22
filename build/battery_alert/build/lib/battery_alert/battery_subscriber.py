import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class BatterySubscriber(Node):
   def __init__(self):
       super().__init__('battery_subscriber')
       self.subscription = self.create_subscription(
           Int32,
           '/battery_level',
           self.listener_callback,
           10
       )


   def listener_callback(self, msg):
       level = msg.data


       if level < 10:
           self.get_logger().error(f'CRITICAL! Battery = {level}%')
       elif level < 30:
           self.get_logger().warn(f'LOW BATTERY! = {level}%')
       else:
           self.get_logger().info(f'Battery OK: {level}%')


def main(args=None):
   rclpy.init(args=args)
   node = BatterySubscriber()
   rclpy.spin(node)
   node.destroy_node()
   rclpy.shutdown()
