#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # ROS-Kafka Bridge for topic 1: single_ros_kafka_bridge_topic_2.py
    # V.2.0.0.
#----------------------------------------------------------------------------------------

import time
import json
import rospy
import roslib
import socket
from std_msgs.msg import String
from kafka import KafkaProducer
from kafka import KafkaConsumer

class single_ros_kafka_bridge_topic_2():

    def __init__(self):

        rospy.init_node('single_ros_kafka_bridge_topic_2', anonymous=False)

        self.publisher2 = rospy.Publisher('bridge_to_ros_topic_2', String, queue_size=10)

        rospy.Subscriber("ros_to_bridge_topic_2", String, self.ros_to_bridge_topic_2_callback)

        self.producer2 = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

        self.consumer2 = KafkaConsumer('kafka_to_bridge_topic_2',
                                    bootstrap_servers='localhost:9092',
                                    value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                    auto_offset_reset='latest',
                                    consumer_timeout_ms=2000)
        
        self.rate = rospy.Rate(25)
        self.main()

    def ros_to_bridge_topic_2_callback(self, topic_2_data):
        self.producer2.send('bridge_to_kafka_topic_2', {"data": topic_2_data.data})

    def kafka_to_bridge_topic_2_callback(self, topic_2_data):
        self.publisher2.publish(topic_2_data["data"])
    
    def main(self):
        while not rospy.is_shutdown():
            for message in self.consumer2:
                self.kafka_to_bridge_topic_2_callback(message.value)
        rospy.spin()

if __name__ == '__main__':
    try:
        single_ros_kafka_bridge_topic_2()
    except KeyboardInterrupt:
        pass
