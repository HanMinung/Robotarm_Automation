#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from std_msgs.msg import Int32MultiArray, Int32

def callback(data):
    rospy.loginfo("Received msg = %s", str(data.data))

def main():
    rospy.init_node('listener', anonymous=True)

    # Publisher
    pub = rospy.Publisher('int_chatter', Int32, queue_size=10)

    # Subscriber
    rospy.Subscriber("array_chatter", Int32MultiArray, callback)

    rate = rospy.Rate(10)
    msg = Int32()

    while not rospy.is_shutdown():
        msg.data = 10

        rospy.loginfo("Sending msg = %d", msg.data)

        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    main()
