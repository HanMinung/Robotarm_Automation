import rospy
from move_group_python_interface import MoveGroupPythonInterface
from math import tau
from std_msgs.msg import Int32MultiArray, Int32
import math
import time

DEG2RAD = math.pi/180
RAD2DEG = 180/math.pi

mm2meter = 0.001

def absCoord(absList) :

    """
        - input parameter : 1D list
        - sequence : x, y, z, roll, pitch, yaw
    """

    # poseXYZ = [absList[0] , absList[1] , absList[2]]
    poseXYZ = [-absList[1] * mm2meter , absList[0] * mm2meter , absList[2] * mm2meter]
    poseRPY = [absList[3] * DEG2RAD   , absList[4] * DEG2RAD  , absList[5] * DEG2RAD ]

    return poseXYZ, poseRPY


def jointSet(jointList) : 

    targetJoint = [jointList[0]*DEG2RAD, jointList[1]*DEG2RAD, jointList[2]*DEG2RAD , jointList[3]*DEG2RAD , jointList[4]*DEG2RAD , jointList[5]*DEG2RAD]

    return targetJoint


def absPlanning(planning) :
    
    """
        - 전체 경로 계획을 담당하는 함수
        - 입력 인자 예시 : [[100,200,300,0,0,0], [200,100,300,0,0,0]]
    """
    
    rate = rospy.Rate(5)

    indy10_interface = MoveGroupPythonInterface()

    for action in planning : 
        
        indy10_interface.go_to_pose_abs(*absCoord(action))

        rate.sleep()
    

def jointPlanning(planning) :

    rate = rospy.Rate(10)
    
    indy10_interface = MoveGroupPythonInterface()
        
    for action in planning : 
        
        indy10_interface.go_to_joint_state(jointSet(action))

        time.sleep(2)



def printMode() :

    print("\n----------------------------------------------------------------------------------")
    print("|                     MODE 1 : PICK IN   (PRESS '1')                              |")                                       
    print("|                     MODE 2 : PICK OUT  (PRESS '2')                              |")     
    print("----------------------------------------------------------------------------------\n")