#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # ROS-Kafka Bridge for topic 1: single_ros_kafka_bridge_topic_1.py
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

class single_ros_kafka_bridge_topic_1():

    def __init__(self):

        rospy.init_node('single_ros_kafka_bridge_topic_1', anonymous=False)

        self.publisher1 = rospy.Publisher('bridge_to_ros_topic_1', String, queue_size=10)

        rospy.Subscriber("ros_to_bridge_topic_1", String, self.ros_to_bridge_topic_1_callback)

        self.producer1 = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

        self.consumer1 = KafkaConsumer('kafka_to_bridge_topic_1',
                                    bootstrap_servers='localhost:9092',
                                    value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                    auto_offset_reset='latest',
                                    consumer_timeout_ms=2000)
        
        self.rate = rospy.Rate(50)
        self.main()

    def ros_to_bridge_topic_1_callback(self, topic_1_data):
        self.producer1.send('bridge_to_kafka_topic_1', {"data": topic_1_data.data})

    def kafka_to_bridge_topic_1_callback(self, topic_1_data):
        self.publisher1.publish(topic_1_data["data"])
    
    def main(self):
        while not rospy.is_shutdown():
            for message in self.consumer1:
                self.kafka_to_bridge_topic_1_callback(message.value)
        rospy.spin()

if __name__ == '__main__':
    try:
        single_ros_kafka_bridge_topic_1()
    except KeyboardInterrupt:
        pass
