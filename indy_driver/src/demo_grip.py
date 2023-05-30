#!/usr/bin/env python3
#-*- coding:utf-8 -*- 

from move_group_python_interface import MoveGroupPythonInterface
from math import tau
import rospy

def main():
    try:

        indy10_interface = MoveGroupPythonInterface(real=True, gripper="Vaccum")

        input("============ Press `Enter` to execute a movement using a joint state goal ...")
        target_joints = [0, 0, tau/4, 0, tau/4, 0]          # tau = 2 * pi
        indy10_interface.go_to_joint_state(target_joints)

        input("============ Press `Enter` to grip on ...")
        indy10_interface.grip_on()

        input("============ Press `Enter` to grip off ...")
        indy10_interface.grip_off()
        
        print("============ Python tutorial demo complete!")

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()