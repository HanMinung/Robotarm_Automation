#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from projectFunctions import *


global modeInfo 
global lastmodeInfo

modeInfo = 0
lastmodeInfo = 0

taskdoneFlag = Int32()
taskdoneFlag.data = 0

pubTask = rospy.Publisher('taskFlag', Int32, queue_size = 10)


def callback(data):
        
        global modeInfo
        modeInfo = data.data

        rospy.loginfo(f"     - Received flag = {modeInfo}")

        if modeInfo == 1 :

            if input("      - Press 'ENTER' to change taskFlag...") == '' :

                print("      - Client put the shoes on the plate...!")
                taskdoneFlag.data = 1
                pubTask.publish(taskdoneFlag)


        elif modeInfo == 2 :

            if input("      - Press 'ENTER' to change taskFlag...") == '' :

                print("      - Client pick out the shoes...!")
                taskdoneFlag.data = 1
                pubTask.publish(taskdoneFlag)

        



def main():
            
    print("     - Cam process is initialized ...!")
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("modeSelect", Int32, callback)

    rospy.spin()


if __name__ == '__main__':

    main()
