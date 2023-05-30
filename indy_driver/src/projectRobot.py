#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from functions import *
from tkinter import *

def taskCallback(data):

    global workdoneFlag
    workdoneFlag = data.data

# sending taskFlag
rospy.Subscriber('taskFlag', Int32, taskCallback)

def main():

    global workdoneFlag
    workdoneFlag = 0


    """
        Initialization process
        - node initialization (communication)
        - robot initialization
        - Publisher (mode selection)
    """

    rospy.init_node('move_group_python_interface', anonymous = True)
    
    indy10_interface = MoveGroupPythonInterface()
    
    pub = rospy.Publisher('modeInfo', Int32, queue_size = 10)

    rate = rospy.Rate(10)

    msg = Int32()
    resetMsg = Int32() # for resetting taskFlag
    resetMsg.data = 0

    print("----------------------------------------------------------------------------------")
    print("|                                                                                |")
    print("|                          SHOEBOT PROGRAM STARTS ...!                           |")
    print("|                                                                                |")
    print("----------------------------------------------------------------------------------")

    input("\n           Press 'ENTER' to initialize state of robot ...!      ")
    
    indy10_interface.go_to_joint_state(jointSet(0,0,0,0,0,0))

    print("\n           Robot initialization complete ...!")
    print("\n----------------------------------------------------------------------------------")
    
    while not rospy.is_shutdown():
        
        print("\n----------------------------------------------------------------------------------")
        print("|                            MODE 1 : PICK IN                                    |")                                       
        print("|                            MODE 2 : PICK OUT                                   |")     
        print("----------------------------------------------------------------------------------\n")
        modeFlag = int(input("          - Please enter mode what you want :"))
        msg.data = modeFlag
        
        # Shoes pick in mode
        if modeFlag == 1 :

            indy10_interface.go_to_pose_abs(*absCoord([0.5, 0, 0.5, 0, 0, 0]))
            pub.publish(msg)
            print("      - Plate is transffered to client...!")

            while workdoneFlag == 0 :
                rate.sleep()
            
            print("      - Client completed putting shoes on plate...!")
            indy10_interface.go_to_pose_abs(*absCoord([0.2, 0.3, 0.5, 0, 0, 0])) 
            workdoneFlag = 0
            
            
        # Shoes pickout mode
        elif modeFlag == 2 :

            indy10_interface.go_to_pose_abs(*absCoord([0.5, 0, 0.5, 0, 0, 0]))
            pub.publish(msg)

            while workdoneFlag == 0 :
                rate.sleep()
            
            print("      - Client completed picking out shoes...!")
            print("      - Cam task finished ...!")
            indy10_interface.go_to_pose_abs(*absCoord([0.2, 0.3, 0.5, 0, 0, 0])) 
            workdoneFlag = 0



        elif modeFlag == 0 :
            
            pub.publish(msg)
            indy10_interface.go_to_joint_state(jointSet(0,0,0,0,0,0))
           
        rate.sleep()



if __name__ == '__main__':

    try:
        main()

    except rospy.ROSInterruptException:
        pass
