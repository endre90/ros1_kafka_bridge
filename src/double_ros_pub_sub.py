#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # Dummy ROS 2 Publisher - 2 Subscriber example: double_ros_pub_sub.py
    # V.2.0.0.
#----------------------------------------------------------------------------------------

import time
import rospy
import roslib
import threading
from std_msgs.msg import String

class double_ros_pub_sub():

    def __init__(self):

        time.sleep(1) #Wait for the bridge to start
        # Maybe use timed roslaunch in order to do this

        rospy.init_node('double_ros_pub_sub', anonymous=False)

        self.pub = rospy.Publisher('ros_to_bridge_topic_1', String, queue_size=10)
        self.pub2 = rospy.Publisher('ros_to_bridge_topic_2', String, queue_size=10)

        rospy.Subscriber("bridge_to_ros_topic_1", String, self.bridge_to_ros_1_callback)
        rospy.Subscriber("bridge_to_ros_topic_2", String, self.bridge_to_ros_2_callback)

        self.i = 0
        self.j = 0

        self.rate = rospy.Rate(50)
        self.rate2 = rospy.Rate(25)
        self.topic1()
        self.topic2()
        self.main()

    def bridge_to_ros_1_callback(self, topic_1_data):
        rospy.loginfo("I heard %s", topic_1_data.data)
    
    def bridge_to_ros_2_callback(self, topic_2_data):
        rospy.loginfo("I heard %s", topic_2_data.data)

    def topic1(self):
        def topic1_callback_local():
            while not rospy.is_shutdown():
                msg = 'ROS: Hello World A: {0}'.format(self.i)
                self.i += 1
                self.pub.publish(msg)
                self.rate.sleep()
        t = threading.Thread(target=topic1_callback_local)
        t.daemon = True
        t.start()
    
    def topic2(self):
        def topic2_callback_local():
            while not rospy.is_shutdown():
                msg = 'ROS: Hello World B: {0}'.format(self.j)
                self.j += 1
                self.pub2.publish(msg)
                self.rate2.sleep()
        t = threading.Thread(target=topic2_callback_local)
        t.daemon = True
        t.start()

    def main(self):
        while not rospy.is_shutdown():
            pass
        rospy.spin()

if __name__ == '__main__':
    try:
        double_ros_pub_sub()
    except rospy.ROSInterruptException:
        pass
