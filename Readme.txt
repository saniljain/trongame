This is the source code of my project..


Instructions
	Python version-2.7
	Necessary libraries
		Pygame version-1.9.2
		numpy version-1.6.2

	Press 'q' to quit the game

	TRONGAME.py is the main game
		1.In the arena, the left boundary is constructed slightly to the right of the game window's left wall
	voronoi_generator.py is the voronoi diagram generator given the positions of the two bots


	voronoi_generator
		1. The program hangs if try to take input from the console.. so if u want to change the coordinates, change them in the last few lines of source code

The basic aims of my project have been fulfilled, but there is still scope of all these improvements
1. I have kept the depth_max=1 for now as it is as good as depth_max=2 and faster
2. I am thinking of increasing the depth has the game progresses as the number of leafs will increase... but I still haven't found an ideal end game condition as almost always, the game ends with the bot going into space filling mode
3. The minimax is very slow.. so I am thinking of trying to incorporate some dynamic programming..storing some moves in advanced and displaying them while the next are thought of(I highly doubt it though)
4. Getting a even better heuristic, probably improved coefficient(now 1) through data mining..

I will send the documentation within a week and try to achieve these improvements if possible


