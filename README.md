# ros1_kafka_bridge
Package with examples on how to make a ROS-Kafka bridge. This is the version 2 (no ROS-Bridge Server). 

1. Download Confluent and unpack it somewhere
2. install kafka-python with: pip instal kafka-python
3. Might need bson: sudo pip install pymongo
4. export PATH=/path-to-confluent/bin:$PATH
5. Make sure that you have java 1.8
6. If not java 1.8, install it and change to it with: sudo update-alternatives –config java
7. confluent start
8. roscore

# Examples:
1. roslaunch ros_kafka_bridge demo_joined.launch
2. roslaunch ros_kafka_bridge demo_separated.launch

