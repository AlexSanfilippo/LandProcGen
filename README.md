# LandProcGen
While teaching myself python during the Spring of 2021, I undertook this attempt at making one of my favorite types of program: a procedural terrain generator.  

Updated 20 Feb, 2022
Since I first starting programming I wanted to recreate the procedural terrain generation I had seen in so many of the games I played in my youth, such as Age of Empires and Minecraft.  I figured that while teaching myself python, this project would allow me to hone my python programming skills on something I enjoy.  

HOW TO RUN: 
  I programming the map generator in Idle, but it should run on any python IDE (Jypter Notebook, etc.) so long as it supports numpy and matplotlib.  There is only one python script (I would like to revisit this and organize it better when I have time for these personal projects) so simpy hitting "run" should produce 3 projections of the same map: A 2d black and white elevation map, a 2d "colored" elevation map, and a 3d map.  Lines 217 to 222 (inclusive) contain variable that effect how the map is generated.  
CHANGING THE MAP GENERATION 
   First, changing the seed value on line 217 will produce a new random map.  The program uses Bilinear interpolation, which relies on a random number generator to create noise on which the map is based.  On lines 218 and 219, the dimensions of the map can be changed.  Note that very large values will take a while to run, and matplotlib can only produce graphs up to a certain maximum resolution.  Line 220 will add more detail to the map by adding more nodes between which height values are interpolated.  The "smooth" variable on line 221 will raise the lowest points on the map, if a flatter map is desired.  Last, line 222 can take 4 different strings as values: caldera, island, doubleIsland, and flatMap.  Each will set the initial nodes (rather than have them be set randomly) to create certain map "styles", such as an island surrounded by the sea.  
