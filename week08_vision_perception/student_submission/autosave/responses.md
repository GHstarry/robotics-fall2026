# Lab 7 saved answers

## mission_1.diagnosis
I compared normal_1 and dim_1 from my saved runs. In both of these runs, the box covers the mug area. The mask as well as the contour in dim_1 shrank. However it was still the largest eligible contour so the box stayed the same. One setting that explains how a region was missed is because setting the lowest brighness eligible to 25 made is to that the darkest part of the mug + dimmed made it so that this dark area becomes ineligible.

## mission_1.limitations
One parameter that I changed was setting lowest saturation to 145 from 70. This changed the number of eligible pixels. This is because fewer pixels now pass that threshold. This means that the wood (which is pretty bright in color) merge less onto the mug. A limitation that remains for  a different cup (such as a different color) might fall outside the range for hue which is set to 0 to 35. 

## mission_2.choice
I recommend using the learned detector with a .25 acceptance threshold for further testing. On normal, dim, and occluded, it gave 4 correct and no false boxes while the classical detector produced no correct boxes. The learned detector is much slower but at the speed of about 13 ms per, it is still fast enough for testing and since accuracy matters more here. For normal_1, the foreground mask had an IoU of .57 and a Dice score of .73mk. A detailed foreground mask by itself cannot identify the mug as it does not separate regions so the mask could cover a different object/ merge them with the mug. One import limit with this small test is that a single changing result can severely damage a condition's precision. 

## mission_2.comparison
Normal | Classical: 0 correct, 2 false, 2 missed | Learned: 2 correct, 0 false, 0 missed
Dim | Classical: 0 correct, 2 false, 2 missed | Learned: 2 correct, 0 false, 0 missed
Occluded | Classical: 0 correct, 2 false, 2 missed | Learned: 0 correct, 0 false, 0 missed

## pillar_search.diagnosis
In attempt 20261031T073530-df66efc5, the robot successfully centered on the blue pillar. For the first 14.2 seconds, the camera did not see blue so the mask was empty and kept turning left at .35 rad/s. at 14.3, blue was detected and the centroid gave an error of -1 meaning that it was all the way to the left. To negate the error, the robot continued to turn left to center on the middle of the image. In attempt 20261031T080127-b95873d2, I raised the gain to 2.75 and the tolerance to .15. The higher gain made the robot turn faster so centering was faster but there was much more overshoot where it would land past the center.  

## pillar_search.evidence
In attempt 20261031T080127-b95873d2, all four colors were centered and the run ended in COMPLETE after 18.3 seconds. The state timeline and camera evidence shows the same pattern for every color. It goes into SEARCH where it turns until the color appears, then CENTER to turn towards it more. Then CONFIRM where it centers it. Lastly, it HOLD the position for .7 seconds. Then NEXT searches for the next sequence's color (and repeats). A cnetered color and a stable hold does not prove that the robot found the right object because the controller only looks for pixels of a certain color. Any other object that is of the same color would also pass as the controller never checks the shape. It also does not say anything about distance as the single camera only tells what is left and right.

## line_following.comparison
ALl three attempts used the same settings except for the gain. On the practice (straight line), the gain of .08 was good for it to drive at .155 m/s. On the track with .08 gain, the gain was too weak. On the first hairpin, the line drifted too far to the right of the image with an error of around +.6 to +.78. Because of this large error, the controller slowed the robot down to about .07 m/s. On the track with gain of 2.0, the same hairpin was cleared with more ease where the error was now around +.03 and +.06. The robot turned harder at .13 rad/s and the line stayed centered in the mask. The error didn't swing back and forth between left and right so the higher gain did not cause oscillations.

## line_following.limits
One stop that occurred in my attempts was in my practice run. The robot stopped with LINE_LOST at 68.6 seconds. The magenta area in the mask dropped very fast as the robot reached the end of the line. The stop began with missing information and not with image processing or control. For a real delivery robot that operates around people, a lidar would be needed to detect people and obstacles.  

## final.synthesis
The three missions taught me that turning visual evidence into reliable robot behavior has a lot more processes that are running in the back. It showed me that seeing something in an image is not the same as knowing where it is and that knowing where it is does not guarantee that the robot can act on it the way we want it to. In In mission 2, a color mask was what gave the robot a steering signal. With gain at 1.2, it centered at blue in 1.4 seconds without passing the center. At gain 2.75, it was able to center on all four colors in 18.3 seconds but slightly overshot  past the center. In mission 3, the control choice changed how the robot maneuvered on the track. By upping the gain to 2 on the track, the error dipped to just .03 and .06 and at the same time, lowered the time to finish to 122.3 seconds from 187.9 seconds when the gain was at .08.

## final.course_reflection
1. This activity made me more interest in the computer vision side of robots. By seeing how a camera image is processed by the robot and then turned into a command was interesting especially when it can be seen in the robot's behavior.
3. I see a lot of value in connecting robots that can see in our society. However one consideration I have with this is that a robot that perceives a colored region can still be wrong about the actual location of the object. As such, if this robot was to move among people, these mistakes could very well hurt someone.
4. One thing that stood out to me in this activity was how much the gain mattered on the track following task. By changing the gain from 0.08 to 2 allowed it to stay on line better as well as finishing over a minute faster.
