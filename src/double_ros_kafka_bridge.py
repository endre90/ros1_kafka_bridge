#!/usr/bin/env python

#----------------------------------------------------------------------------------------
# authors, description, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # ROS-Kafka Bridge for 2 Kafka and 2 ROS topics: double_ros_kafka_bridge.py
    # V.2.0.0.
#----------------------------------------------------------------------------------------

import time
import json
import rospy
import roslib
import socket
import threading
from std_msgs.msg import String
from kafka import KafkaProducer
from kafka import KafkaConsumer

class double_ros_kafka_bridge():

    def __init__(self):

        rospy.init_node('double_ros_kafka_bridge', anonymous=False)

        self.publisher1 = rospy.Publisher('bridge_to_ros_topic_1', String, queue_size=10)
        self.publisher2 = rospy.Publisher('bridge_to_ros_topic_2', String, queue_size=10)

        rospy.Subscriber("ros_to_bridge_topic_1", String, self.ros_to_bridge_topic_1_callback)
        rospy.Subscriber("ros_to_bridge_topic_2", String, self.ros_to_bridge_topic_2_callback)

        self.producer1 = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.producer2 = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: json.dumps(m).encode('ascii'))

        self.consumer1 = KafkaConsumer('kafka_to_bridge_topic_1',
                                  bootstrap_servers='localhost:9092',
                                  value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                  auto_offset_reset='latest',
                                  consumer_timeout_ms=2000)
        
        self.consumer2 = KafkaConsumer('kafka_to_bridge_topic_2',
                                  bootstrap_servers='localhost:9092',
                                  value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                  auto_offset_reset='latest',
                                  consumer_timeout_ms=2000)
                                  
        
        self.rate = rospy.Rate(50)
        self.reader1()
        self.reader2()
        self.main()

    def ros_to_bridge_topic_1_callback(self, topic_1_data):
        self.producer1.send('bridge_to_kafka_topic_1', {"data": topic_1_data.data})

    def ros_to_bridge_topic_2_callback(self, topic_2_data):
        self.producer2.send('bridge_to_kafka_topic_2', {"data": topic_2_data.data})

    def kafka_to_bridge_topic_1_callback(self, topic_1_data):
        self.publisher1.publish(topic_1_data["data"])
    
    def kafka_to_bridge_topic_2_callback(self, topic_2_data):
        self.publisher2.publish(topic_2_data["data"])

    def reader1(self):
        def reader1_callback_local():
            while not rospy.is_shutdown():
                for message in self.consumer1:
                    self.kafka_to_bridge_topic_1_callback(message.value)
        t1 = threading.Thread(target=reader1_callback_local)
        t1.daemon = True
        t1.start()
    
    def reader2(self):
        def reader2_callback_local():
            while not rospy.is_shutdown():
                for message in self.consumer2:
                    self.kafka_to_bridge_topic_2_callback(message.value)
        t2 = threading.Thread(target=reader2_callback_local)
        t2.daemon = True
        t2.start()
    
    def main(self):
        while not rospy.is_shutdown():
            pass
        rospy.spin()

if __name__ == '__main__':
    try:
        double_ros_kafka_bridge()
    except KeyboardInterrupt:
        pass
