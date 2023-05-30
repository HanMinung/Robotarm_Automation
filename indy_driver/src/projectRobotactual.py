#!/usr/bin/env python3
#-*- coding:utf-8 -*- 

from projectFunctions import *
from projectjointDef import *
from std_msgs.msg import Int32

class robotProcess:

    def __init__(self):

        self.taskdonePub      = rospy.Publisher('taskfinish', Int32, queue_size = 10)
        self.modePub          = rospy.Publisher('modeSelect', Int32, queue_size = 10)
        self.taskdoneSub      = rospy.Subscriber('taskFlag', Int32, self.callback)

        self.indy10_interface = MoveGroupPythonInterface()
        self.rate             = rospy.Rate(10)

        self.msg_taskFlag     = Int32()
        self.msg_modeFlag     = Int32()
      
        self.workdoneFlag     = 0
        self.modeSelection    = 0
        self.camdoneFlag      = 0
        self.cabinetIdx       = [0, 0, 0, 0, 0, 0]
        self.pickoutFlag      = 0

        self.pickinPlan       = []
        self.pickoutAvail     = []
        self.pickout          = None


    def main(self):

        input("PRESS ENTER TO INITIALIZE ROBOT STATE ...!\n\n")

        jointPlanning([initial_pos])

        print("INITIALIZATION COMPLETED ...!\n\n")

        try:

            while not rospy.is_shutdown() :

                self.getmodeInput()
                
                if(self.modeSelection == 1) :
                    
                    self.in_exceptionHandling()

                    self.findemptySpacePick()

                    # jointPlanning(self.pickinPlan)

                    self.cabinetState()

                    self.tasksendtoCam()
                    
                    # recieve task done flag from cam process
                    self.waitforClient()

                    # 다시 신발 넣는 구동넣기
                    
                    self.initialization()


                elif(self.modeSelection == 2) :

                    self.out_exceptionHandling()

                    self.findAvailableSpace()

                    self.selectCabinet()

        except rospy.ROSInterruptException:
            return
        
        except KeyboardInterrupt:
            return


    def getmodeInput(self):

        printMode()

        while True :  
            
            self.modeSelection = input("\nPLEASE INPUT MODE WHAT YOU WANT ...!\n\n")

            if self.modeSelection.isdigit():

                self.modeSelection = int(self.modeSelection)

                if self.modeSelection in [1, 2]:
                    break

                else:
                    print("INVALID INPUT ! PLEASE ENTER EITHER 1 OR 2.")

        self.msg_modeFlag.data = self.modeSelection

        # Publish flag to cam process
        self.modePub.publish(self.msg_modeFlag)


    def findemptySpacePick(self) :
    
        for Idx, cabinet in enumerate(self.cabinetIdx) :

            if cabinet == 0 :

                # # Robot manipulating part
                if   (Idx == 0) : self.pickinPlan = cabinet_0_planning
                elif (Idx == 1) : self.pickinPlan = cabinet_1_planning
                elif (Idx == 2) : self.pickinPlan = cabinet_2_planning
                elif (Idx == 3) : self.pickinPlan = cabinet_3_planning
                elif (Idx == 4) : self.pickinPlan = cabinet_4_planning
                elif (Idx == 5) : self.pickinPlan = cabinet_5_planning

                self.cabinetIdx[Idx] = 1

                break
        
        print(f"CABINET NUMBER '{Idx}' IS ASSIGNED ...!\n")
        
        self.modeSelection = 0


    def cabinetState(self) :
        
        print("--------------------------   CABINET STATE  ----------------------------")
        print(f"|\t\tCABINET 0 : {self.cabinetIdx[0]}      |       CABINET 3 : {self.cabinetIdx[3]}\t\t|")
        print(f"|\t\tCABINET 1 : {self.cabinetIdx[1]}      |       CABINET 4 : {self.cabinetIdx[4]}\t\t|")
        print(f"|\t\tCABINET 2 : {self.cabinetIdx[2]}      |       CABINET 5 : {self.cabinetIdx[5]}\t\t|")
        print("------------------------------------------------------------------------")


    def in_exceptionHandling(self) :

        if all(space == 1 for space in self.cabinetIdx):

            print("ALL CABINETS IS FILLED...! ONLY PICKING OUT COMMAND IS AVAILABLE...!")

            self.modeSelection = input("\nPLEASE INPUT MODE WHAT YOU WANT ...!\n\n")


    def tasksendtoCam(self) :

        self.workdoneFlag = 1

        self.msg_taskFlag.data = self.workdoneFlag

        self.taskdonePub.publish(self.msg_taskFlag)


    def initialization(self) :

        self.modeSelection = 0     
        self.workdoneFlag = 0
        self.camdoneFlag = 0

        jointPlanning([initial_pos])

        
    def callback(self, data):

        self.camdoneFlag = data.data

        rospy.loginfo(f"RECEIVED TASK DONE FLAG FROM CAM = {self.camdoneFlag}")


    def waitforClient(self) :

        while(self.camdoneFlag == 0) :

            rospy.sleep(2)
            print("WAITING FOR CLIENT...!")



    def out_exceptionHandling(self) :

        if all(space == 0 for space in self.cabinetIdx):

            print("THERE'S NO CABINET WITH SHOES...! ONLY PICK IN COMMAND IS AVAILABLE ...!")

            self.modeSelection = input("\nPLEASE INPUT MODE WHAT YOU WANT ...!\n\n")


    def findAvailableSpace(self) :
        
        for Idx, cabinet in enumerate(self.cabinetIdx):

            if cabinet == 1 :

                print(f"CANINET '{Idx}' IS AVAILABLE TO PICK OUT...!")

                self.pickoutAvail.append(Idx)
        

    def selectCabinet(self) :
        
        self.cabinetState()

        while True :

            self.pickout = input("PLEASE INPUT CABINET # NUMBER THAT YOU WANT TO PICK OUT...!")

            if self.pickout.isdigit() :

                self.pickout = int(self.pickout)

                if self.pickout in self.pickoutAvail :
                    
                    self.cabinetIdx[self.pickout] = 0

                    break

                else :
                    print("INVALID INPUT...! THE CABINET NUMBER YOU ENTERED DOES NOT HAVE ANY SHOES...!")
                
            else : 
                print("INVALID INPUT...! PLEASE ENTER A VALID CABINET NUMBER...!")


        
                
        
        
        
        
                




 
if __name__ == "__main__":

    robot_process = robotProcess()

    robot_process.main()
