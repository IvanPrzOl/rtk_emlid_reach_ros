cmake_minimum_required(VERSION 2.8.3)
project(rtk_emlid_reach)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_message_files(
  FILES
  rtklibLLH.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES beginner_tutorials
  CATKIN_DEPENDS roscpp rospy std_msgs message_generation
#  DEPENDS system_lib
)


