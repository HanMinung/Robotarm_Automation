#include "ros/ros.h"					// ROS 기본 헤더 파일
#include "my_tutorial/tutorial_msg.h"	// 메시지 파일의 헤더. 빌드 후 자동 생성됨.

int main(int argc, char **argv){
  // 노드 초기화
  ros::init(argc, argv, "talker");     // 노드 이름: talker
  ros::NodeHandle nh;                  // ROS 시스템과 통신을 위한 노드 핸들
  
  // Publisher 초기화 및 변수 선언 (노드 핸들을 이용하여 publisher 초기화)
  // my_tutorial 패키지에 정의된 tutorial_msg 타입의 '/chatter' 토픽 생성 (queue 사이즈 = 100개)
  // 만약, 표준 메시지를 사용한다면 (예) <std_msgs::String>
  ros::Publisher pub_chatter = nh.advertise<my_tutorial::tutorial_msg>("/chatter", 100); 
  
  // 변수 초기화  
  ros::Rate loop_rate(10);			// 주기를 10Hz로 설정
  my_tutorial::tutorial_msg msg;	// 메시지 변수 선언
  
  int count = 0;

  while (ros::ok()){			// 종료 전까지 반복 수행
    msg.stamp = ros::Time::now();	// 메시지 변수 내 stamp에 현 시간 입력
    msg.data  = count;				// 메시지 변수 내 data에 count 입력

    // 터미널에 출력
    ROS_INFO("send time(sec) = %d", msg.stamp.sec);
    ROS_INFO("send msg = %d", msg.data);

    // publisher 변수를 통해 msg를 publish 함
    pub_chatter.publish(msg);

    loop_rate.sleep();		// 사전에 정의된 주기만큼 일시정지(sleep)

    ++count;
  }

  return 0;
}