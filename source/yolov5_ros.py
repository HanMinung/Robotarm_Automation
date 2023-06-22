#!/usr/bin/env python3.9
#-*- coding:utf-8 -*- 

import rospy
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from cv_bridge import CvBridge
from pathlib import Path
import os
import sys
import platform
from rostopic import get_topic_type
from projectFunctions import *

from sensor_msgs.msg import Image, CompressedImage
from detection_msgs.msg import BoundingBox, BoundingBoxes
from indy_driver.msg import object_info, robot_state
from std_msgs.msg import Int32

# add yolov5 submodule to path
ROOT = Path("/home/tk032/catkin_ws/src/yolov5")  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative path


# import from yolov5 submodules
from models.common import DetectMultiBackend
from utils.general import (
    check_img_size,
    check_requirements,
    non_max_suppression,
    scale_boxes
)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
#from utils.augmentations import letterbox
from utils.dataloaders import letterbox


@torch.no_grad()
class Yolov5Detector:
    # initial value
    shoe_detect         = False
    num_shoes           = 0
    shoes_frame         = 0
    frame_continue      = 0
    taskdone            = 0
    modeInfo            = 0
    workdoneFlag        = Int32()
    shoeflag            = Int32()
    def __init__(self):
        self.conf_thres         = rospy.get_param("~confidence_threshold",0.7)
        self.iou_thres          = rospy.get_param("~iou_threshold",0.8)
        self.agnostic_nms       = rospy.get_param("~agnostic_nms",False)
        self.max_det            = rospy.get_param("~maximum_detections",5)
        self.classes            = rospy.get_param("~classes", None)
        self.line_thickness     = rospy.get_param("~line_thickness",1)
        self.view_image         = rospy.get_param("~view_image",True)
        # Initialize weights 
        weights                 = rospy.get_param("~weights","/home/tk032/catkin_ws/src/yolov5/runs/train/Slippers/weights/best.pt")
        # Initialize model
        self.device             = select_device(str(rospy.get_param("~device","")))
        self.model              = DetectMultiBackend(weights, device=self.device, dnn=rospy.get_param("~dnn",True), data=rospy.get_param("~data","home/tk032/catkin_ws/src/yolov5/shoes/data.yaml"))
        self.stride, self.names, self.pt, self.jit, self.onnx, self.engine = (
            self.model.stride,
            self.model.names,
            self.model.pt,
            self.model.jit,
            self.model.onnx,
            self.model.engine,
        )

        # Setting inference size
        self.img_size           = [rospy.get_param("~inference_size_w", 640), rospy.get_param("~inference_size_h",480)]
        self.img_size           = check_img_size(self.img_size, s=self.stride)

        # Half
        self.half               = rospy.get_param("~half", False)
        self.half &= (
            self.pt or self.jit or self.onnx or self.engine
        ) and self.device.type != "cpu"  # FP16 supported on limited backends with CUDA
        if self.pt or self.jit:
            self.model.model.half() if self.half else self.model.model.float()
        bs = 1  # batch_size
        cudnn.benchmark = True  # set True to speed up constant image size inference
        self.model.warmup()  # warmup        
        
        # Initialize subscriber to Image/CompressedImage topic
        #input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param("~input_image_topic"), blocking = True)
        input_image_type, input_image_topic, _ = get_topic_type(rospy.get_param("~input_image_topic","/camera/image_raw"), blocking = True)
        self.compressed_input = input_image_type == "sensor_msgs/CompressedImage"

        if self.compressed_input:
            self.image_sub = rospy.Subscriber(
                input_image_topic, CompressedImage, self.callback, queue_size=1
            )
        else:
            self.image_sub = rospy.Subscriber(
                input_image_topic, Image, self.callback, queue_size=1
            )

        # Initialize prediction publisher
        self.pred_pub = rospy.Publisher(
            rospy.get_param("~output_topic","bounding_boxes"), BoundingBoxes, queue_size=10
        )
        # Initialize image publisher
        self.publish_image = rospy.get_param("~publish_image",False)
        if self.publish_image:
            self.image_pub = rospy.Publisher(
                rospy.get_param("~output_image_topic"), Image, queue_size=10
            )

        # Publisher, Subscriber
        self.shoePub            = rospy.Publisher('shoeFlag', Int32, queue_size = 10)
        self.modeSub            = rospy.Subscriber('modeSelect',Int32, self.mode_callback)
        self.taskSub            = rospy.Subscriber('taskfinish',Int32, self.task_callback)
        self.flag_send_msg      = False
        self.workdoneFlag       = False
        self.shoeflag           = False

        # Initialize CV_Bridge
        self.bridge             = CvBridge()

    def callback(self, data):
        """adapted from yolov5/detect.py"""

        # print(data.header)
        if self.compressed_input:
            im = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding="bgr8")
        else:
            im = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        
        im, im0 = self.preprocess(im)
        # print(im.shape)
        # print(img0.shape)
        # print(img.shape)

        # Run inference
        im = torch.from_numpy(im).to(self.device) 
        im = im.half() if self.half else im.float()
        im /= 255
        if len(im.shape) == 3:
            im = im[None]

        pred = self.model(im, augment=False, visualize=False)
        pred = non_max_suppression(
            pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det
        )

        ### To-do move pred to CPU and fill BoundingBox messages
        
        # Process predictions 
        det = pred[0].cpu().numpy()

        bounding_boxes = BoundingBoxes()
        bounding_boxes.header = data.header
        bounding_boxes.image_header = data.header
        
        annotator = Annotator(im0, line_width=self.line_thickness, example=str(self.names))

        # reset
        self.num_shoes = 0
        
        if self.taskdone == 1:
            if len(det):
                if self.modeInfo == 1:
                    self.frame_continue = 0

                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    bounding_box = BoundingBox()
                    c = int(cls)
                    # Fill in bounding box message
                    bounding_box.Class = self.names[c]
                    bounding_box.probability = conf 
                    bounding_box.xmin = int(xyxy[0])
                    bounding_box.ymin = int(xyxy[1])
                    bounding_box.xmax = int(xyxy[2])
                    bounding_box.ymax = int(xyxy[3])

                    bounding_boxes.bounding_boxes.append(bounding_box)

                    # Annotate the image
                    if self.publish_image or self.view_image:  # Add bbox to image
                        # integer class
                        label = f"{self.names[c]} {conf:.2f}"
                        annotator.box_label(xyxy, label, color=colors(c, True))       
                    self.num_shoes += 1
                    
                        ### POPULATE THE DETECTION MESSAGE HERE
                
                # Detect Shoes
                if self.modeInfo == 1:
                    self.shoes_frame            += 1

                    if self.shoes_frame         >= 100:
                        self.shoes_frame        = 100
                        self.shoeflag           = True
                        self.workdoneFlag       = True
                    else:
                        self.shoeflag           = False

                elif self.modeInfo == 2:
                    self.shoes_frame            += 1

                    if self.shoes_frame >= 30:
                        self.shoes_frame        = 30
                        self.frame_continue     = 0
                
            else: 
                if self.modeInfo == 1:
                    self.frame_continue         += 1
                    if self.frame_continue      >= 30:
                        self.frame_continue     = 30
                        self.shoes_frame        = 0
                
                elif self.modeInfo == 2:
                    self.shoes_frame            = 0
                    self.frame_continue         += 1
                    if self.frame_continue      >= 100:
                        self.frame_continue     = 100
                        self.shoeflag           = True
                        self.workdoneFlag       = True 
                    else:
                        self.shoeflag           = False

            if self.workdoneFlag:
                if not self.flag_send_msg:
                    self.shoePub.publish(self.shoeflag)
                    self.shoeflag = False
                    self.taskdone = False
                    self.shoes_frame = 0
                    self.frame_continue = 0
                    self.flag_send_msg = True
                self.workdoneFlag = False
                    


        background_color = (255, 255, 255)  # 흰색
        # 흰색 사각형 그리기
        cv2.rectangle(im0, (0, 0), (320, 150), background_color, -1)

        # 신발 유무 text로 표현
        if self.num_shoes == 0:
            self.shoe_detect = 'OFF'
            color = (0,0,255)
        else:
            self.shoe_detect = 'ON'
            color = (0,255,0)

        cv2.putText(im0, f"SHOES:  ", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(im0, f"{self.shoe_detect:>17}",(15, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(im0, f"SHOE FRAME:  {self.shoes_frame:>3}", (15, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(im0, f"NOT DETECTED:  {self.frame_continue:>1}", (15, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Stream results
        im0 = annotator.result()
        
        # Publish prediction
        self.pred_pub.publish(bounding_boxes)

        # Publish & visualize images
        if self.view_image:
            if platform.system() == 'Linux':
                    cv2.namedWindow(str("camera"), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str("camera"), im0.shape[1], im0.shape[0])

            cv2.imshow(str("camera"), im0)
            cv2.waitKey(1)  # 1 millisecond
        if self.publish_image:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(im0, "bgr8"))


    def mode_callback(self, data):

        self.modeInfo = data.data

        rospy.loginfo(f"MODE = {self.modeInfo}")

    def task_callback(self, data):

        # self.shoes_frame = 0
        
        # self.frame_continue = 0

        self.flag_send_msg = False
        
        self.taskdone = data.data

        rospy.loginfo(f"TASKDONE = {self.taskdone}")

    def preprocess(self, img):
        """
        Adapted from yolov5/utils/datasets.py LoadStreams class
        """
        img0 = img.copy()
        img = np.array([letterbox(img, self.img_size, stride=self.stride, auto=self.pt)[0]])
        # Convert
        img = img[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        img = np.ascontiguousarray(img)

        return img, img0 


if __name__ == "__main__":

    check_requirements(exclude=("tensorboard", "thop"))

    rospy.init_node("yolov5", anonymous=True)

    detector = Yolov5Detector()

    rospy.spin()
