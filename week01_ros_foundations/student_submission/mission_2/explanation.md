# Mission 2

## Measurement Explanation

For the trial where I was able to set my own parameters, the estimated traveled path and the start-to-end distance differ slightly as the curve caused by the turning speed made the start-to-end distance shorter as the fastest way to get from point a to b is a straight line. The slight turn made it so that the estimated traveled path of .762m caused the robot to only displace itself by .759m. 

## Motion Comparison

For the first curved trial, my prediction was wrong because the duration was not long enough for the robot to make a full circle. Two values that prove this are duration and start-to-end distance. The duration given was 4 seconds while the start-to-end distance is .5m. This means that the curve the robot made did not ultimately close at its origin point as there is still a distance of .5m from the starting point.

## Prediction Locks

{'straight': '2026-09-11T23:15:06.886657+00:00', 'rotation': '2026-09-11T23:42:02.221086+00:00', 'curve': '2026-09-11T23:43:58.763356+00:00', 'curve_modified': '2026-09-11T23:47:49.684777+00:00'}

## Predictions

{'straight': 'I predict the robot will finish with a displacement of .45 meters  ahead of its original starting point.', 'rotation': 'I predict its position will not change while its direction will change to face behind where it was originally facing. ', 'curve': 'I predict a path shape of a circle because a forward speed of .15 m/s is pretty slow and a right turn of -.4 radians/ second over a duration of 4 seconds could allow the robot to make a full but small circle.', 'curve_modified': 'This curve should be wider as well as turns the other way because the turning speed is positive (turns left) with a much faster forward speed and lower turning speed.'}

## Safety Explanation

The command guard checks the proposed command given to the robot and alters or rejects the command if they are not safe. The final zero command stops all movement when a trial ends so that no sudden unexpected movements are executed after the trial. The stale-command timeout is needed if the robot is no longer receiving communication from a node that could be vital in keeping the robot in a functioning state. 

## Modified Settings

{'linear_x': 0.22, 'angular_z': 0.1, 'duration': 4.0}
