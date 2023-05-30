#!/usr/bin/env python3
#-*- coding:utf-8 -*- 
import rospy

from move_group_python_interface import MoveGroupPythonInterface
from math import tau

def main():
    try:

        #ur5e = MoveGroupPythonInterface(real="sim")
        ur5e = MoveGroupPythonInterface()
        # input("============ Press `Enter` to execute a movement using a joint state goal ...")
        # ur5e.move_to_standby()

        input("============ Press `Enter` to execute a movement using a joint state goal ...")
        target_joints = [-tau/4, -tau/4, -tau/4, -tau/4, tau/4, 0.0]          # tau = 2 * pi
        ur5e.go_to_joint_state(target_joints)

        input("============ Press `Enter` to execute a movement using a relative pose ...")
        target_pose_rel_xyz = [-.2, -0.1, 0.0]
        target_pose_rel_rpy = [0, 0, 0]
        ur5e.go_to_pose_rel(target_pose_rel_xyz, target_pose_rel_rpy)

        # input("============ Press `Enter` to execute a movement using a absolute pose ...")
        # target_pose_abs_xyz = [0.0, 0.52, 0.54]
        # target_pose_abs_rpy = [0, 0, 0]
        # ur5e.go_to_pose_abs(target_pose_abs_xyz, target_pose_abs_rpy)


        print("============ Python tutorial demo complete!")

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        print("Shut down by Key Interrupt")
        return

if __name__ == "__main__":
    main()