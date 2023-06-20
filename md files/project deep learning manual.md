# Deep learning in ROS guide

@ Date : Spring semester, 2023

@ Part : Automation part in Industrial AI & Automation class

@ Project #2

@ Instructor : prof. Young-Keun Kim

@ github : https://github.com/HanMinung/Robotarm_Automation

----------

[TOC]

## 1. Python 3.9 installation

By entering the following command in the terminal, user can update the package list and install the necessary components.

```shell
sudo apt update
sudo apt install software-properties-common
```



Add the PPA to the system's source list.

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
```



Install python 3.9 version with below command in the terminal.

```shell
sudo apt install python3.9
```



Version verification using below command in the terminal.

```shell
python3.9 --version
```



## 2. CUDA installation

1) Check the installation of the NVIDIA driver

```shell
nvidia-smi
```

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/24ffa407-69cb-4960-ab56-0931dcfed954" alt="image" style="zoom:80%;" />

2) Check the compatibility between the NVIDIA driver and CUDA version in the link attached below.

link : [CIDA version](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/757ce96a-8ac7-4a9b-a45c-eca28c6032b0" alt="image" style="zoom:80%;" />



3) User can enter the following command to check your CPU architecture.

```shell
uname -m
```



4. **cuda toolkit 다운**

cuda toolkit installation link : [click here to download](https://developer.nvidia.com/cuda-downloads)

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/cdca0885-e528-4a9e-9742-9d748fcbb890" alt="image" style="zoom: 67%;" />



```shell
wget https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_530.30.02_linux.run

sudo sh cuda_12.1.1_530.30.02_linux.run
```



5. Version verification after installing CUDA toolkit

* Installed version : CUDA 11.3

```shell
nvcc -V
```

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/9450b2f8-fba6-4866-8cc5-3a51cb4be48d" alt="image" style="zoom:80%;" />





## 3. cuDNN, pytorch installation

1. nvidia login for installing cuDNN

* link : [download link](https://developer.nvidia.com/login)



2. After logging in, install cuDNN compatible with the CUDA version.

* link : [download link](https://developer.nvidia.com/rdp/cudnn-archive)
* click archieve cuDNN release

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/81524d4c-baba-4837-84fa-f618537cf2e2" alt="image" style="zoom:80%;" />

3. Unzip downloaded file

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/774d5615-b3e7-47ef-8910-d675022e31b9" alt="image" style="zoom: 50%;" />



4. Copy the unzipped file with below commands in the terminal

- command to copy : `cp [복사할 디렉토리/파일] [복사될 디렉토리/파일]`
- command to unzip : `tar xvzf [압축 파일명]`

```shell
tar xvzf cudnn-11.3-linux-x64-v8.2.1.32.tgz
sudo cp cuda/include/cudnn* /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_adv_train.so.8.2.1 /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_adv_train.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_ops_infer.so.8.2.1  /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_ops_infer.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_cnn_train.so.8.2.1  /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_cnn_train.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_adv_infer.so.8.2.1  /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_adv_infer.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_ops_train.so.8.2.1  /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_ops_train.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_cnn_infer.so.8.2.1 /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn_cnn_infer.so.8

sudo ln -sf /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn.so.8.2.1 /usr/local/cuda-11.3/targets/x86_64-linux/lib/libcudnn.so.8
```

* version verification of cuDNN with below command in the terminal

```shell
cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
```



5. pytorch version verification

* link : [click here to view](https://pytorch.org/get-started/previous-versions/)



6. pyTorch installation


<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/954dd81b-60a3-4f04-894f-432b650af563" alt="image" style="zoom:80%;" />

```shell
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
```



7. pytorch version verification

* Type below commands in the terminal for installed pytorch version verification

```python
python

import torch

print(torch.__version__)
```

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/276065c2-3895-43fc-9de6-963a7ea3b4f1" alt="image" style="zoom:80%;" />





## 4. Yolov5 implementation

* Type below commands in the terminal 

```shell
git clone https://github.com/ultralytics/yolov5  # clone

cd yolov5	

pip install -r requirements.txt                  # install
```



* Training process

There are various methods for data labeling, but in this project, Roboflow was used to facilitate the process of data labeling. After the labeling, download the datasets.

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/2d27e3d5-1cd3-41b6-8153-937826bc3077" alt="image" style="zoom:80%;" />



Modify the data.yaml file to match the data format you want to train. In this project, only shoe objects are detected, so set the class to 1.

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/b344691c-1bef-4009-b75d-9da5f52f0c6e" alt="image" style="zoom:80%;" />



train, val data location verification

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/80e11977-826d-4f78-8500-955766f02e1c" alt="image" style="zoom: 67%;" />

```shell
python train.py --batch 16--epochs 10--data "자신의것\data.yaml"--weights yolov5s.pt
```



Train the model by specifying the batch size and number of epochs, matching the weights file and data.yaml file. The best.pt file in yolov5/runs/train/exp contains the trained weights.

<img src="https://github.com/HanMinung/EmbeddedController/assets/99113269/2fcaef72-9a05-4fa6-8394-8be4996d528d" alt="image" style="zoom:67%;" />





















reference
https://jjeongil.tistory.com/2066

https://ingu627.github.io/tips/install_cuda_linux/