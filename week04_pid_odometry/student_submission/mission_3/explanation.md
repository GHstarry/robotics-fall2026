# mission_3 Submission

- Name: Stanley Zheng
- Section: 1

## Explanations

### technical_analysis

I predicted that higher speed and too little Kd would increase error and decrease the pedestrian clearance. The next route point becomes a heading command when first, the target point is chosen, then it calculates how to get to the heading. An inaccurate wheel radius can make a well-tuned controller follow the the wrong path as the odometry uses the radius to measure distance traveled. The difference in each measurement adds up and ultimately could make even a well-tuned controller to fall short/ follow the wrong path.

### human_centered_analysis

The most consequential failure for a pedestrian is when a robot hits a pedestrian. This could happen if the robot does not recognize that the target is blocked by a pedestrian. A good clearance I believe would be around .5 meters and a speed of .2 m/s or slower.A person who is responsible for verifying that decision before deployment is the engineer who designs it.