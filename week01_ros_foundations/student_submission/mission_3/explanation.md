# Mission 3

## Data To Command

The first function 'front_distance' finds the distance of the closest obstacle in front of it from the LiDAR. It does so by putting the values from the LiDAR into a list, finds the angle using the angle_increment of each value and angle_min. Using the angle, we determine whether the value is in front of the robot and is a valid value. Out of the distances we have left, we get the closest one to our robot.

 Then the second function 'decide_velocity' and it stops the robot if there is no given distance or if the distance to travel is shorter than equal to the determined distance from an object in front of it. Otherwise, if neither of those are flagged, we tell the robot to move.

## Missing Data Safety

The robot stops when there is not valid front measurement because it means we don't know if the path in front of it is clear. It could be a that our LiDAR sensor bugged out or something else unexpected happened. But to treat the path as clear and have the robot to continue forward is risky.

## System Layers

The decision functions and the supplied ROS node, as well as the command guard work together to help move the robot. First, the LiDAR values are passed through the functions and fed into the command guards. The command guard checks to make sure the values are safe to pass through and the ROS node receives the value from the command guard to move the actual part.
