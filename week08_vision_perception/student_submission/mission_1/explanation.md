# mission_1

## diagnosis
I compared normal_1 and dim_1 from my saved runs. In both of these runs, the box covers the mug area. The mask as well as the contour in dim_1 shrank. However it was still the largest eligible contour so the box stayed the same. One setting that explains how a region was missed is because setting the lowest brighness eligible to 25 made is to that the darkest part of the mug + dimmed made it so that this dark area becomes ineligible.

## limitations
One parameter that I changed was setting lowest saturation to 145 from 70. This changed the number of eligible pixels. This is because fewer pixels now pass that threshold. This means that the wood (which is pretty bright in color) merge less onto the mug. A limitation that remains for  a different cup (such as a different color) might fall outside the range for hue which is set to 0 to 35. 
