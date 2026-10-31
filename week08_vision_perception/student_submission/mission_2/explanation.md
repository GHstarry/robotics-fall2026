# mission_2

## choice
I recommend using the learned detector with a .25 acceptance threshold for further testing. On normal, dim, and occluded, it gave 4 correct and no false boxes while the classical detector produced no correct boxes. The learned detector is much slower but at the speed of about 13 ms per, it is still fast enough for testing and since accuracy matters more here. For normal_1, the foreground mask had an IoU of .57 and a Dice score of .73mk. A detailed foreground mask by itself cannot identify the mug as it does not separate regions so the mask could cover a different object/ merge them with the mug. One import limit with this small test is that a single changing result can severely damage a condition's precision. 

## comparison
Normal | Classical: 0 correct, 2 false, 2 missed | Learned: 2 correct, 0 false, 0 missed
Dim | Classical: 0 correct, 2 false, 2 missed | Learned: 2 correct, 0 false, 0 missed
Occluded | Classical: 0 correct, 2 false, 2 missed | Learned: 0 correct, 0 false, 0 missed
