# mission_2 Submission

- Name: Stanley Zheng
- Section: 1

## Explanations

### prediction

The estimated forward distance will be larger than the actual distance while the sideways distance will be shorter than.

### calibration_analysis

I predicted that the forward distance would be overestimated and that the sideways distance would be underestimated. This is proven when I set the foward pod's in/tick higher and strafe pod's in/tick lower. Each pod scale changed how much inches each forward pod tick is worth so raising this made every forward and backwards movement longer and same is for the strafe pod but for sideways movements. The sideways pod is necessary because a holonomic robot can move sideways without turning. The sideways pods enable that movement. Some drift can still remain after calibration because it never checks and updates the actual distance with the real world.