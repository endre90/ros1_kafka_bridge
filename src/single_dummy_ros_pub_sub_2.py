#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # Dummy ROS Publisher - Subscriber example: single_dummy_ros_pub_sub_2.py
    # V.2.0.0.
#----------------------------------------------------------------------------------------

import time
import rospy
import roslib
from std_msgs.msg import String

class single_dummy_ros_pub_sub_2():

    def __init__(self):

        time.sleep(1) # Wait for the bridge to start

        rospy.init_node('single_dummy_ros_pub_sub_2', anonymous=False)

        self.pub = rospy.Publisher('ros_to_bridge_topic_2', String, queue_size=10)

        rospy.Subscriber("bridge_to_ros_topic_2", String, self.bridge_to_ros_2_callback)

        self.i = 0

        self.rate = rospy.Rate(25)
        self.main()

    def bridge_to_ros_2_callback(self, topic_2_data):
        rospy.loginfo("I heard %s", topic_2_data.data)

    def main(self):
        while not rospy.is_shutdown():
            msg = 'ROS: Hello World B: {0}'.format(self.i)
            self.i += 1
            self.pub.publish(msg)
            self.rate.sleep()
        rospy.spin()

if __name__ == '__main__':
    try:
        single_dummy_ros_pub_sub_2()
    except rospy.ROSInterruptException:
        pass
