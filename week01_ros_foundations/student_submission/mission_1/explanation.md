# Mission 1

## Command Path Explanation

A proposed command travels on /student_cmd_vel and which is published to /course_cmd_vel_guard (AKA the guard). The guard checks/ alters the command to make sure it is 'safe' and publishes the command to /cmd_vel.


## Graph Explanation

A ROS 2 graph shows nodes and each of their subscriptions/ publishers. For example, a ROS 2 showed a node 'course_cmd_vel_guard' with topic type 'geometry_msg/msg/Twist'. It had 0 publishers and 2 subscriptions.

## Guided Checks

{'bridge_info': True, 'command_topics': True, 'guard_info': True, 'node_list': True, 'scan_info': True, 'scan_message': True}

## Scan Observation

I found .inf in the ranges field, which represents infinity.

## Tools Explanation

Gazebo is responsible for simulating the virtual world for the robot while RViz is responsible for displaying information about our robot as it has subscriptions to ROS' topics.

