#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from std_msgs.msg import Int32MultiArray, Int32

def callback(data):
    rospy.loginfo("Received msg = %d", data.data)

def main():
    rospy.init_node('talker', anonymous=True)

    # Publisher
    pub = rospy.Publisher('array_chatter', Int32MultiArray, queue_size=10)

    # Subscriber
    rospy.Subscriber("int_chatter", Int32, callback)

    rate = rospy.Rate(10)
    msg = Int32MultiArray()

    while not rospy.is_shutdown():
        msg.data = [1, 2, 3, 4, 5, 6]

        rospy.loginfo("Sending msg = %s", str(msg.data))

        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
