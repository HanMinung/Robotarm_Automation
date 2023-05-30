#!/usr/bin/env python3
#-*- coding:utf-8 -*- 

from projectFunctions import *
from projectjointDef import *

def main():
    try:

        indy10_interface = MoveGroupPythonInterface()

        input("============ Press `Enter` to execute a movement using a joint state goal ...")

        caninet4_planning = [caninet_4_pickin_0, caninet_4_pickin_1]
        
        jointPlanning(caninet4_planning)

        print("============ Python tutorial demo complete!")

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()