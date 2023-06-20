#!/usr/bin/env python3.9
#-*- coding:utf-8 -*- 

from projectFunctions import *
from projectjointDef import *
from std_msgs.msg import Int32

class robotProcess:

    def __init__(self):

        self.taskdonePub      = rospy.Publisher('taskfinish', Int32, queue_size = 10)
        self.modePub          = rospy.Publisher('modeSelect', Int32, queue_size = 10)
        self.taskdoneSub      = rospy.Subscriber('taskFlag', Int32, self.callback)
        self.shoeSub          = rospy.Subscriber('shoeFlag', Int32, self.shoe_callback)

        self.ser              = serial.Serial('/dev/ttyACM0', 9600)

        self.indy10_interface = MoveGroupPythonInterface()
        self.rate             = rospy.Rate(10)

        self.msg_taskFlag     = Int32()
        self.msg_modeFlag     = Int32()
      
        self.workdoneFlag     = 0
        self.modeSelection    = 0
        self.camdoneFlag      = 0
        self.cabinetSeq       = 0
        self.cabinetIdx       = [0, 0, 0, 0, 0, 0]

        self.workingFlag      = 0
        self.arduinoSend      = None
        # 로봇이 움직이기 시작하면 1
        # 로봇 구동 끝나면 0
        # 업데이트 될때마다 serial.write
        self.pickinPlan       = []
        self.placePlan        = []
        self.pickoutAvail     = []
        self.pickoutIdx       = None


    def main(self):

        input("PRESS ENTER TO INITIALIZE ROBOT STATE ...!\n\n")

        self.sendtoArduino(1)

        jointPlanning([initial_pos])

        print("INITIALIZATION COMPLETED ...!\n\n")

        self.sendtoArduino(0)

        try:

            while not rospy.is_shutdown() :

                self.getmodeInput()
                
                if(self.modeSelection == 1) :
                    
                    self.in_exceptionHandling()

                    self.findemptySpacePick()

                    self.cabinetState()

                    self.tasksendtoCam()
                    
                    # recieve task done flag from cam process
                    self.waitforClient()

                    self.placeShoes()
                    
                    self.initialization()

                    self.cabinetState()


                elif(self.modeSelection == 2) :

                    self.out_exceptionHandling()

                    self.findAvailableSpace()

                    self.selectCabinet()

                    self.cabinetState()

                    self.robotActuation()

                    self.tasksendtoCam()

                    self.waitforClient()
                    
                    self.placePlate()

                    self.initialization()

                    self.cabinetState()

        except rospy.ROSInterruptException:
            return
        
        except KeyboardInterrupt:
            return


    def sendtoArduino(self, mani) :

        if mani == 0 :

            self.workingFlag = 0

            self.arduinoSend = str(self.workingFlag) + str(self.cabinetSeq) 

            self.ser.write(self.arduinoSend.encode())

        elif mani == 1 :

            self.workingFlag = 1

            self.arduinoSend = str(self.workingFlag) + str(self.cabinetSeq) 

            self.ser.write(self.arduinoSend.encode())
            

    def getmodeInput(self):
        
        printMode()

        self.sendtoArduino(0)

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
                if   (Idx == 0) : self.pickinPlan = cabinet_0_in_planning
                elif (Idx == 1) : self.pickinPlan = cabinet_1_in_planning
                elif (Idx == 2) : self.pickinPlan = cabinet_2_in_planning
                elif (Idx == 3) : self.pickinPlan = cabinet_3_in_planning
                elif (Idx == 4) : self.pickinPlan = cabinet_4_in_planning
                elif (Idx == 5) : self.pickinPlan = cabinet_5_in_planning

                self.cabinetIdx[Idx] = 1

                break


        print(f"CABINET NUMBER '{Idx}' IS ASSIGNED ...!\n")

        self.cabinetSeq  = Idx

        self.sendtoArduino(1)

        jointPlanning(self.pickinPlan)

        jointPlanning([initial_pos])

        jointPlanning([goto_client])
        
        
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

        self.sendtoArduino(0)

        self.msg_taskFlag.data = self.workdoneFlag

        self.taskdonePub.publish(self.msg_taskFlag)


    def initialization(self) :

        self.modeSelection = 0     
        self.workdoneFlag  = 0
        self.camdoneFlag   = 0
        self.pickoutIdx    = 0
        self.pickinPlan    = []
        self.placePlan     = []

        self.sendtoArduino(1)

        jointPlanning([initial_pos])

        
    def callback(self, data):

        self.camdoneFlag = data.data

        rospy.loginfo(f"RECEIVED TASK DONE FLAG FROM CAM = {self.camdoneFlag}")


    def shoe_callback(self, data):

        self.camdoneFlag = data.data

        rospy.loginfo(f"RECEIVED TASK DONE FLAG FROM CAM = {self.camdoneFlag}")


    def waitforClient(self) :

        while(self.camdoneFlag == 0) :

            rospy.sleep(2)
            print("WAITING FOR CLIENT...!")


    def placeShoes(self) :
        
        if   (self.cabinetSeq == 0) : self.placePlan = cabinet_0_out_planning
        elif (self.cabinetSeq == 1) : self.placePlan = cabinet_1_out_planning
        elif (self.cabinetSeq == 2) : self.placePlan = cabinet_2_out_planning
        elif (self.cabinetSeq == 3) : self.placePlan = cabinet_3_out_planning
        elif (self.cabinetSeq == 4) : self.placePlan = cabinet_4_out_planning
        elif (self.cabinetSeq == 5) : self.placePlan = cabinet_5_out_planning


        self.sendtoArduino(1)

        jointPlanning([initial_pos])

        jointPlanning(self.placePlan)


    def out_exceptionHandling(self) :

        if all(space == 0 for space in self.cabinetIdx):

            print("THERE'S NO CABINET WITH SHOES...! ONLY PICK IN COMMAND IS AVAILABLE ...!")

            self.modeSelection = input("\nPLEASE INPUT MODE WHAT YOU WANT ...!\n\n")


    def findAvailableSpace(self) :

        print("--------------------------------------------------------\n")        

        for Idx, cabinet in enumerate(self.cabinetIdx):

            if cabinet == 1 :
                
                print(f"\nCANINET '{Idx}' IS AVAILABLE TO PICK OUT...!")

                self.pickoutAvail.append(Idx)
        
        
    def selectCabinet(self) :
        
        self.cabinetState()

        while True :

            self.pickoutIdx = input("PLEASE INPUT CABINET # NUMBER THAT YOU WANT TO PICK OUT...!")

            if self.pickoutIdx.isdigit() :

                self.pickoutIdx = int(self.pickoutIdx)

                if self.pickoutIdx in self.pickoutAvail :
                    
                    self.cabinetIdx[self.pickoutIdx] = 0

                    break

                else :
                    print("INVALID INPUT...! THE CABINET NUMBER YOU ENTERED DOES NOT HAVE ANY SHOES...!")
                
            else : 
                print("INVALID INPUT...! PLEASE ENTER A VALID CABINET NUMBER...!")


    def robotActuation(self) :
        
        if  (self.pickoutIdx == 0)   :   self.pickinPlan = cabinet_0_in_planning
        elif(self.pickoutIdx == 1)   :   self.pickinPlan = cabinet_1_in_planning
        elif(self.pickoutIdx == 2)   :   self.pickinPlan = cabinet_2_in_planning
        elif(self.pickoutIdx == 3)   :   self.pickinPlan = cabinet_3_in_planning
        elif(self.pickoutIdx == 4)   :   self.pickinPlan = cabinet_4_in_planning
        elif(self.pickoutIdx == 5)   :   self.pickinPlan = cabinet_5_in_planning
        
        self.cabinetSeq = self.pickoutIdx

        self.sendtoArduino(1)

        jointPlanning(self.pickinPlan)

        print("PLATE IS TRANSFERRING TO CLIENT ...!")

        jointPlanning([initial_pos])

        jointPlanning([goto_client])


    def placePlate(self) :
        
        if   (self.pickoutIdx == 0)   :   self.placePlan = cabinet_0_out_planning
        elif (self.pickoutIdx == 1)   :   self.placePlan = cabinet_1_out_planning
        elif (self.pickoutIdx == 2)   :   self.placePlan = cabinet_2_out_planning
        elif (self.pickoutIdx == 3)   :   self.placePlan = cabinet_3_out_planning
        elif (self.pickoutIdx == 4)   :   self.placePlan = cabinet_4_out_planning
        elif (self.pickoutIdx == 5)   :   self.placePlan = cabinet_5_out_planning
        
        print("ROBOT IS PLACING EMPTY PLATE TO ORIGINAL SPACE ...!")

        self.sendtoArduino(1)

        jointPlanning([initial_pos])

        jointPlanning(self.placePlan)

 
if __name__ == "__main__":
    
    robot_process = robotProcess()

    robot_process.main()
