#include "ros/ros.h"
#include "my_tutorial/tutorial_msg.h" 

// Publisher가 생성한 topic을 Subscribing 하면서 callback 함수 실행
void chatterCallback(const my_tutorial::tutorial_msg::ConstPtr& msg){ // 토픽 정보를 msg 포인터 파라미터로 읽어드림.
  // 터미널 출력
  ROS_INFO("recieve time(sec) = %d", msg->stamp.sec);
  ROS_INFO("recieve msg = %d", msg->data);
}

int main(int argc, char **argv){
  // 노드 초기화
  ros::init(argc, argv, "listener");	// 노드 이름: listener
  ros::NodeHandle nh;					// ROS 시스템과 통신을 위한 노드 핸들
    
  // Subscriber 초기화 및 변수 선언, callback 함수 지정
  ros::Subscriber sub = nh.subscribe("/chatter", 100, chatterCallback);	// 토픽 이름: '/chatter', queue size = 100

  // 무한 루프 / 노드가 callback 이외의 어떤 일도 하지 않는다면 spin()함수 사용.
  ros::spin();

  return 0;
}