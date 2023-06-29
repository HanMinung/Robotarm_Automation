

# Shoebot : operation manual

@ Date : Spring semester, 2023

@ Part : Automation part in Industrial AI & Automation class

@ Project #2

@ Instructor : prof. Young-Keun Kim

@ github : https://github.com/HanMinung/Robotarm_Automation

------

[TOC]

## 1. Operation environment

python	 :     3.9

CUDA 	  :     11.3.1

cuDNN 	:     8.2.1

pyTorch    :     1.12.1

detailed environment setting is specified in other md file : **project description.md** (link : [click here to view](https://github.com/HanMinung/Robotarm_Automation/blob/main/md%20files/project%20description.md))



## 2. Pre-work

​			All the packages and codes constructed while conducting the project were managed in catkin_ws path. Therefore, basic settings for catkin_ws are essential first. After that, it will be explained step by step on how to insert the packages. 

* First, go to the following link (industrial AI automation: automation part github) and download the Github material as a zip file, as shown in the figure below. 

  link : [click here to go to github](https://github.com/hyKangHGU/Industrial-AI-Automation_HGU)

  <img src="https://github.com/HanMinung/DLIP/assets/99113269/24bc197d-fb8a-40d6-822f-8ae862d4f597" alt="image" style="zoom:67%;" />

* Next, in the Ubuntu environment, the home-catkin-ws path is created by default. In that path, there is a folder called `'src'` in catkin_ws. If users copy and paste the downloaded file into that path as shown below, the basic setting is completed.

  <img src="https://github.com/HanMinung/DLIP/assets/99113269/7fc7929e-e8cb-41f2-b6f1-258bc61a3447" alt="image" style="zoom: 67%;" />

* The compressed file contains various configuration files for operating the indy10 and ur5e robots, so the user can freely construct and operate the code for the project. If you've pasted the file correctly as shown in the figure below, you need to open the terminal window by pressing `ctrl+alt+t` and save the changes by entering the following commands and doing catkin_make.

  ```bash
  # setting path
  cd catkin_ws
  
  # build
  catkin_make
  ```

  



## 3. Robot speed control

​			To adjust the driving speed of the robot, user needs to execute the `set_velocity.py` Python file in the terminal first. To set the speed limit for the  robot's movement, following parameters need to modified within the code:

- `indy.set_joint_vel_level`
- `indy.set_task_vel_level`

These parameters can be set to levels 1 to 9, where higher numbers allow for faster movement. The IP address of the Indy 10 robot  used is **"192.168.0.18."**

- set_velocity.py file description

```python
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
```

Please provide the IP address of the robot in the `robot_ip` field.

Create the above Python code in the following file path. ( **catkin_ws  -  src  -  indy_utils** )

Grant file permissions to this file

```shell
# path setting
cd catkin_ws/src/indy_utils

# file permission grant
chmod +x set_velocity.py
```



## 4. File download & implementation

download link : [click here to download](https://github.com/HanMinung/Robotarm_Automation)

Go to above link and download zip file.

- best.pt : trained model file with YOLO V5 (to detect shoes)
  - reference : best.pt file is not uploaded with github source since it has too large size to upload.
  - Download link : [click here to download](https://drive.google.com/file/d/1lZzz0lrPWlCPxpHgDw0iMKY6-9MfmjVg/view?usp=sharing)
- Those are with `.py` extension files are main code for for manipulation.
- Extract zip file in the path (**indy_driver   -  src**)
- Arduino process is for just for reference. It is embedded in the UNO board.

[![image](https://user-images.githubusercontent.com/99113269/247136502-875d885f-71b0-451b-b30e-923c5fee7839.png)](https://user-images.githubusercontent.com/99113269/247136502-875d885f-71b0-451b-b30e-923c5fee7839.png)



module installation

Install modules to run code

- Install psutil

```bash
pip install --ignore-installed psutil
```

- Reinstall Kiwisolver

```shell
# remove
sudo rm -r /usr/lib/python3/dist-packages/kiwisolver-1.0.1.egg-info

# install
pip install kiwisolver
```

- Download package

```bash
# setting path
cd catkin_ws/src

# download
git clone https://github.com/mats-robotics/detection_msgs.git
```

- And please type below commands to terminal for adjustment.

```bash
# setting path
cd catkin_ws

# build
catkin_make
```

camera.py modification

Check your webcam device number

```bash
ls -ltr /dev/video*
```

<img src="https://github.com/HanMinung/NumericalProgramming/assets/99113269/28858d15-3b86-4fe7-84f5-8f907b0e9234" alt="image" style="zoom:50%;" />

Enter the confirmed number in camera.py

![image](https://github.com/HanMinung/NumericalProgramming/assets/99113269/edf9284a-7d31-4eca-8a81-dfecb197e96e)





## 5. yolov5_ros.py modification

[![image](https://user-images.githubusercontent.com/99113269/247138596-c7178007-f5ec-44ff-9fb2-e182df793b04.png)](https://user-images.githubusercontent.com/99113269/247138596-c7178007-f5ec-44ff-9fb2-e182df793b04.png)

In the `yolov5_ros.py` code, specify the folder path where your own yolov5 exists.

![image](https://github.com/HanMinung/NumericalProgramming/assets/99113269/18562979-7c2b-4110-807a-d8f0ede903de)

Change the path of the weights to the path where you have downloaded the `best.pt` file.

Change the path of data to the path where you have downloaded the `data.yaml` file.



## 6. Code implementation

Prepare five terminals and enter the following commands in each of them.

- Terminal 1

```bash
# setting path
cd catkin_ws/src/indy_utils

# setting velocity limiation 
python3.9 set_velocity.py
```

- Terminal 2

```bash
# setting path
cd catkin_ws

# robot connection
source devel/setup.bash
roslaunch indy10_moveit_config moveit_planning_execution.launch robot_ip:=192.168.0.18
```

- Terminal 3

```bash
# setting path
cd catkin_ws

# camera process implementation
source devel/setup.bash
rosrun indy_driver camera.py
```

- Terminal 4

```bash
# setting path
cd catkin_ws

# main process implementation
source devel/setup.bash
rosrun indy_driver projectRobotactual.py
```

- Terminal 5

```bash
# setting path
cd catkin_ws

# deep learning object detection process implementation
source devel/setup.bash
rosrun indy_driver yolov5_ros.py
```

Execute each terminal command in order.

The progress of the program will be carried out in Terminal 4, which corresponds to the red-boxed terminal below.

[![image](https://user-images.githubusercontent.com/99113269/247140715-71057e7d-716a-41c1-93e1-5658c76e572e.png)](https://user-images.githubusercontent.com/99113269/247140715-71057e7d-716a-41c1-93e1-5658c76e572e.png)

All the steps mentioned above can be managed together  using a bash shell script. The instructions for creating the bash script and executing all the steps at once are provided in another Markdown  file named `project description.md.`



### 6.1. Implementation sequence

**[Caution]**

- When the LED is **red**, it means the robot is in motion, so do not place or remove the shoes and do not enter any commands in the terminal.
- Only when the LED is **green**, enter commands in the terminal and place or remove the shoes.

1. **Robot state initialization**

- Press enter to initialize robot state when program is initialized.

[![image](https://user-images.githubusercontent.com/99113269/247142342-cc0d4e1a-94c4-4f7a-80df-926b516b00b8.png)](https://user-images.githubusercontent.com/99113269/247142342-cc0d4e1a-94c4-4f7a-80df-926b516b00b8.png)

1. **Mode selection**

- Press 1 : shoes pickin mode
- Press 2 : shoes pickout mode
- If '1' is selected, empty cabinet is automatically assigned and the  robot manipulation is started and the LED turns on with red light.

[![image](https://user-images.githubusercontent.com/99113269/247143401-7e4772ad-b34d-4171-8c1f-8a2462f653f6.png)](https://user-images.githubusercontent.com/99113269/247143401-7e4772ad-b34d-4171-8c1f-8a2462f653f6.png)

1. **Shoes detection**

[![image](https://user-images.githubusercontent.com/99113269/247144189-27ab34fd-b90d-4600-b2f6-253877c2e877.png)](https://user-images.githubusercontent.com/99113269/247144189-27ab34fd-b90d-4600-b2f6-253877c2e877.png)

- Bring an empty plate and wait for the client to place the shoes  completely. During the waiting period, the message "waiting for client"  will be displayed. Once the shoes are placed, it will be detected, and  the plate with the shoes will be placed back.

1. **Pick out mode**

![image](https://github.com/HanMinung/Robotarm_Automation/assets/99113269/768fa249-96a5-4c23-8c91-81b9a1d311ba)

Once the final operation is completed, the process of  selecting the mode is repeated. If option 2 (Shoe Retrieval Mode) is  selected, the user will be prompted to choose which cabinet to retrieve  shoes from.

In contrast to the Shoe Placement Mode, in this case, the  user will input the index of the cabinet from which to retrieve shoes.  The system will then detect the disappearance of the shoes from the  camera's view.