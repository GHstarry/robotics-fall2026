# Week 6: SLAM and Mapping

- email: stanley.zheng44@login.cuny.edu
- name: Stanley Zheng

## final.course_reflection

1. This activity made me rethink me interest in robotics. I recently saw these robots called "Microduck" on stage with Jensen Huang and after going through this activity, it has made me appreciate these tiny robots much more. 
2. Although it was quite a chore to make robots do exactly what you want it to perform, I think being able to work through it is rewarding. Overall, I would still consider doing something similar in the future.
4. One thing that stood out to me in this activity was unreliable/ finicky the robot was overall. Even though controlling the robot was easy, there were many limitation that prevented me from going where I wanted to go and map out what I thought was there.

## final.synthesis

The robot only knows what its LiDAR scans and where it believes it was when each scan happens. Map 1 and map 2 both do not describe the whole house. My perimeter route that took 8 mins covered the center hallway and east side while my east route that took 10 mins mapped out one room as well as the center hallway. Everything else is unknown but not empty. The robot is also unable to determine what each obstacle is (whether it's a wall or furniture). Motion-estimate error shaped both maps. In mission 1, the west area contains copies of the same walls at different angles and when I came back to the long center walls near the start, a speckled line appeared that was not parallel to the original wall. That suggests there was drift that was effecting the mapping and rather than correcting it, it was added on top of it. Because of this, I can't claim that a loop closure happened. In mission 2, I made sure to stop before every turn and also took care to rotate slowly. The speckle fraction did go down  but one rotated duplicate wall still appeared. Mapping time was exchanged for quality. In mission 1, it gained 4.14 m^2 of known area per minute versus 2.65 for mission 2. With that said, the majority of map 1's "known" area is unreliable. For a later task, I would trust mission 2's map more (for a task that goes to the east of the house) because it seems more coherent although still having imperfections. For a task that goes go the west, we would have to make do with the messier map from mission 1.

## mission_1.drift_and_revisit

The place that I had revisited was the long wall next to the origin. It was solid and legible on the first run however on revisit, the walls seemed to be shifted with what seems like a straight speckled line that is no longer parallel to the original wall. This looks like drift when new scans were added on top of previous mapped scans. 

## mission_1.limitations

One area that remained unknown was the east side of the house as I was only able to "explore" west side of the house before it became too messy and had to stop. In the screenshot, that would be the top-right side of the "box" looking shape that I had mapped. My method of going through the perimeter (kinda like DFS) only made it to the north-central and west rooms and never got back to the center (entry point) to explore the east side. This is why our LiDAR never had a line of sight in that area.  

## mission_1.route.original_prediction

The route that I plan to take is to move along the outer walls and go through each entry that I reach. I predict that weak areas include corners and alignment may become worse as drift may build up.

## mission_1.route.prediction_draft

The route that I plan to take is to move along the outer walls and go through each entry that I reach. I predict that weak areas include corners and alignment may become worse as drift may build up.

## mission_2.comparison

Mission 1 took 8 mins while mission 2 took 10 mins. Map 1 gave more coverage for the time (33.1 m^2 compared to 26.6 m^2) which is 4.14 m^2/min vs 2.65 m^2/min as well as a 23.7 percent known fraction against 22.3 percent respectfully. My prediction was not completely correct as it did not cover more of the house. However, it was correct on that by being more careful (coming to a complete stop before turning as well as turning slow) gave a clearer map. 

## mission_2.map_choice

I would trust mission 2's map more for a task especially in the east side of the house. It completely mapped out a room in the east and the long central wall is a clean parallel line with no dupes. With that being said, mission 2 is still no where near perfect as near the doorway into the south room, ,there is a duplicated wall that can be seen to be extending outside the house's wall. This is probably due to drift while turning in a narrow corner. It is also missing the entire west side of the house. A limitation that these images and numbers have is that these walls and mapped out cells are not necessarily in the correct place. The known fraction can thus be a deceitful measurement as someone who is looking at map 1 could know less since it is so messy compared to map 2 even though map 1's known area (33.12 m^2) is larger than map 2's (26.52 m^2).

## mission_2.strategy.original_prediction

My second route will go east first. I predict that this map will cover more of the house because the first map never reached the east rooms and it should also be clearer because I will stop before rotating rather which may decrease drift. I think that turning too fast in a corner was when the scans became messy and disorganized.

## mission_2.strategy.prediction_draft

My second route will go east first. I predict that this map will cover more of the house because the first map never reached the east rooms and it should also be clearer because I will stop before rotating rather which may decrease drift. I think that turning too fast in a corner was when the scans became messy and disorganized. 
