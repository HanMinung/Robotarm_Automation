# Shoebot : operation manual

@ Date : Spring semester, 2023

@ Part : Automation part in Industrial AI & Automation class

@ Project #2

@ Instructor : prof. Young-Keun Kim

@ github : https://github.com/HanMinung/Robotarm_Automation

------------

[TOC]

## 1. Operation environment

python		3.9

CUDA 		 11.3.1

cuDNN 	   8.2.1

pyTorch      1.12.1

detailed environment setting is specified in other md file : **project description.md**



## 2. Robot speed control

​			To adjust the driving speed of the robot, user needs to execute the `set_velocity.py` Python file in the terminal first. To set the speed limit for the robot's movement, following parameters need to modified within the code:

- `indy.set_joint_vel_level`
- `indy.set_task_vel_level`

These parameters can be set to levels 1 to 9, where higher numbers allow for faster movement. The IP address of the Indy 10 robot used is **"192.168.0.18."**

- set_velocity.py file description

```````python
#!/usr/bin/env python3.9
#-*- coding:utf-8 -*- 

import indydcp_client as client
import copy

def main():
    
    robot_ip = "192.168.0.18"    						# 예시 STEP IP 주소
    robot_name = "NRMK-Indy10"   						# IndyRP2의 경우 "NRMK-IndyRP2"
    indy = client.IndyDCPClient(robot_ip, robot_name) 	# indy 객체 생성

    indy.connect()

    indy.set_joint_vel_level(9)     # 1 ~ 9
    indy.set_task_vel_level(9)      # 1 ~ 9

    indy.disconnect() 				# 연결 해제


if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        print("[ERROR]", e)
```````

Please provide the IP address of the robot in the `robot_ip` field.

Create the above Python code in the following file path. ( **catkin_ws  -  src  -  indy_utils** )

Grant file permissions to this file

``````shell
# path setting
cd catkin_ws/src/indy_utils

# file permission grant
chmod +x set_velocity.py
``````





## 3. File download & implementation

download link : [click here to download](https://github.com/HanMinung/Robotarm_Automation)

Go to above link and download zip file.

* best.pt : trained model file with YOLO V5 (to detect shoes)
  * reference : best.pt file is not uploaded with github source since it has too large size to upload.
  * Download link : [click here to download](https://drive.google.com/file/d/1lZzz0lrPWlCPxpHgDw0iMKY6-9MfmjVg/view?usp=sharing)
* Those are with `.py` extension files are main code for for manipulation. 
* Extract zip file in the path (**indy_driver   -  src**) 
* Arduino process is for just for reference. It is embedded in the UNO board.

![image](https://github.com/HanMinung/NumericalProgramming/assets/99113269/875d885f-71b0-451b-b30e-923c5fee7839)

* And please type below commands to terminal for adjustment.

```shell
# setting path
cd catkin_ws

# build
catkin_make
```



## 4. yolov5_ros.py modification

![image](https://github.com/HanMinung/NumericalProgramming/assets/99113269/c7178007-f5ec-44ff-9fb2-e182df793b04)

In the `yolov5_ros.py` code, specify the folder path where your own yolov5 exists.

![image](https://github.com/HanMinung/EmbeddedController/assets/99113269/093a788c-8752-4226-8510-0680efbeb5c0)

Change the path of the weights to the path where you have downloaded the `best.pt` file.



## 5. Code implementation

Prepare five terminals and enter the following commands in each of them.

* Terminal 1

```shell
# setting path
cd catkin_ws/src/indy_utils

# setting velocity limiation 
python3.9 set_velocity.py
```

* Terminal 2

```shell
# setting path
cd catkin_ws

# robot connection
source devel/setup.bash
roslaunch indy10_moveit_config moveit_planning_execution.launch robot_ip:=192.168.0.18
```

* Terminal 3

```shell
# setting path
cd catkin_ws

# camera process implementation
source devel/setup.bash
rosrun indy_driver camera.py
```

* Terminal 4

```shell
# setting path
cd catkin_ws

# main process implementation
source devel/setup.bash
rosrun indy_driver projectRobotactual.py
```

* Terminal 5

```shell
# setting path
cd catkin_ws

# deep learning object detection process implementation
source devel/setup.bash
rosrun indy_driver yolov5_ros.py
```

Execute each terminal command in order.

The progress of the program will be carried out in Terminal 4, which corresponds to the red-boxed terminal below.

![image](https://github.com/HanMinung/EmbeddedController/assets/99113269/71057e7d-716a-41c1-93e1-5658c76e572e)

All the steps mentioned above can be managed together using a bash shell script. The instructions for creating the bash script and executing all the steps at once are provided in another Markdown file named `project description.md.`



### 5.1. Implementation sequence

**[Caution]**

- When the LED is **red**, it means the robot is in motion, so do not place or remove the shoes and do not enter any commands in the terminal.

- Only when the LED is **green**, enter commands in the terminal and place or remove the shoes.



1) **Robot state initialization**

* Press enter to initialize robot state when program is initialized.

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/cc0d4e1a-94c4-4f7a-80df-926b516b00b8" alt="image" style="zoom: 80%;" />



2. **Mode selection**

* Press 1 : shoes pickin mode
* Press 2 : shoes pickout mode
* If '1' is selected, empty cabinet is automatically assigned and the robot manipulation is started and the LED turns on with red light.

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/7e4772ad-b34d-4171-8c1f-8a2462f653f6" alt="image" style="zoom: 80%;" />



3. **Shoes detection**

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/27ab34fd-b90d-4600-b2f6-253877c2e877" alt="image" style="zoom:80%;" />

* Bring an empty plate and wait for the client to place the shoes completely. During the waiting period, the message "waiting for client" will be displayed. Once the shoes are placed, it will be detected, and the plate with the shoes will be placed back.



4. **Pick out mode**

<img src="C:\Users\hanmu\AppData\Roaming\Typora\typora-user-images\image-20230620232221435.png" alt="image-20230620232221435" style="zoom:80%;" />

Once the final operation is completed, the process of selecting the mode is repeated. If option 2 (Shoe Retrieval Mode) is selected, the user will be prompted to choose which cabinet to retrieve shoes from.

In contrast to the Shoe Placement Mode, in this case, the user will input the index of the cabinet from which to retrieve shoes. The system will then detect the disappearance of the shoes from the camera's view.