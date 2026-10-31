# line_following

## comparison
ALl three attempts used the same settings except for the gain. On the practice (straight line), the gain of .08 was good for it to drive at .155 m/s. On the track with .08 gain, the gain was too weak. On the first hairpin, the line drifted too far to the right of the image with an error of around +.6 to +.78. Because of this large error, the controller slowed the robot down to about .07 m/s. On the track with gain of 2.0, the same hairpin was cleared with more ease where the error was now around +.03 and +.06. The robot turned harder at .13 rad/s and the line stayed centered in the mask. The error didn't swing back and forth between left and right so the higher gain did not cause oscillations.

## limits
One stop that occurred in my attempts was in my practice run. The robot stopped with LINE_LOST at 68.6 seconds. The magenta area in the mask dropped very fast as the robot reached the end of the line. The stop began with missing information and not with image processing or control. For a real delivery robot that operates around people, a lidar would be needed to detect people and obstacles.  
