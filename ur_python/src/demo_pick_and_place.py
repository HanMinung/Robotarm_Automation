#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import rospy
import moveit_commander
import moveit_msgs
import geometry_msgs

import tf

from math import pi

from move_group_python_interface import MoveGroupPythonInterface

DEG2RAD = pi/180
RAD2DEG = 180/pi

def main():
    try:
        print("grip")
        ur5e = MoveGroupPythonInterface()
        
        # ur5e.go_to_pose_rel((0.2, 0.0, 0.1), (0.0, 0.0, 90 * DEG2RAD))
        ur5e.go_to_pose_rel((-0.3, -0.1, 0.0), (0.0, 0.0, 0.0))
        ur5e.grip_off()
        
        ur5e.go_to_pose_rel((0.0, 0.0, -0.18), (0.0, 0.0, 0.0))
        ur5e.grip_on()
        
        ur5e.go_to_pose_rel((0.0, 0.0, 0.18), (0.0, 0.0, 0.0))
        ur5e.go_to_pose_rel((0.4, 0.0, 0.0), (0.0, 0.0, 0.0))
        ur5e.go_to_pose_rel((0.0, 0.0, -0.18), (0.0, 0.0, 0.0))
        ur5e.grip_off()

        ur5e.go_to_pose_rel((0.0, 0.0, 0.18), (0.0, 0.0, 0.0))
        ur5e.move_to_standby()

        print("mission 1: complete")
        rospy.sleep(3)

        ur5e.go_to_pose_rel((0.1, -0.1, 0.0), (0.0, 0.0, 0.0))
        ur5e.grip_off()
        
        ur5e.go_to_pose_rel((0.0, 0.0, -0.18), (0.0, 0.0, 0.0))
        ur5e.grip_on()
        
        ur5e.go_to_pose_rel((0.0, 0.0, 0.18), (0.0, 0.0, 0.0))
        ur5e.go_to_pose_rel((-0.4, 0.0, 0.0), (0.0, 0.0, 0.0))
        ur5e.go_to_pose_rel((0.0, 0.0, -0.18), (0.0, 0.0, 0.0))
        ur5e.grip_off()

        ur5e.go_to_pose_rel((0.0, 0.0, 0.18), (0.0, 0.0, 0.0))
        ur5e.move_to_standby()

        print("mission 2: complete")
    
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        print("Shut down by Key Interrupt")
        return


if __name__ == '__main__':
    main()