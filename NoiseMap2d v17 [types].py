#03.11.2021
#working random map generator, using bilinear interpolation.  a base map and 3 octaves are
#combined (via simple weighted summation) to give a nice, detailed map.  Different map modes
#allow for a few different modes of generation [island, doubleIsland, caldera, default], and
#can be combined for even more map modes.  Attempts at creating a river have resulted in
#mixed results due to dissonance between the base and the 3 octaves.  


#3.19.21 issues
"""
While I  can increase the DPI to get extremely high resolution results, I cannot
Figure out how to export this highres image.  Using the "save" button on the
graph screen always creates an image of lower resolution (about 700x700 max)
Using print screen key has the same results.  There might be a direct save
method that will allow me to export the graph in full resolution. 
"""

import random as r
import math as math
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

import matplotlib as mpl #for changing colorbar

from matplotlib.colors import BoundaryNorm  #for more 2d plotting
from matplotlib.ticker import MaxNLocator
def getMapMin(matrix): #gets lowest value of 2d matrix
    h = len(matrix)
    w = len(matrix[0]) #get map dimensions
    lowP = 100 #lowpoint
    for i in range(0,h-1):
        if min(matrix[i]) < lowP:
            lowP = min(matrix[i])
    return lowP #return the lower value in the whole matrix
    
def drawRiver(matrix): #draws rivers on the map
    #issues as of 3.10.2021:
        #Can't get river to pass through mountains
        #can't get river to curve along cosine
        #likely issue: do to different dimensions, octaves interpret river line
        #differently,  its why y=x works but y= cos(x) + x doesn't
        #lets initialize none-random flat rmap, then draw river on it. 
    
    #pick random point, random angle
    #draw straight line to end of the map by reducing height
    #next step is to make river curve, try cosine
    h = len(matrix)
    w = len(matrix[0]) #get map dimensions
    #pick a random points
    springH = r.randint(0,h-1) #coordinates of where to start the river
    springW = r.randint(0,w-1)
    #pick random angle
    #angle = r.randint(0,359)
    slope = r.randint(0,5)
    # y = mx+b
    #riverH = getMapMin(matrix) #works, remove to test 0
    riverH = 0 #no change from above
    #matrix[springW][springH] = riverH#this works
    #matrix[springW][springH] = ri#this works
    curH = springH
    curW = springW #current
    #while curH < h-1 and curH > 0: #this is never ending
     #   while curW < w-1 and curW > 0:
    #cheating, adding my own starint point
    curH = 0
    curW = 0
    print("here!" + str(springW) + ", " + str(springH))
    while curH < h and curW < w:
            matrix[curW][curH] = riverH 
            #temp just draw line y = x
            #curH = math.floor(curW*1.0)
            #curH += 1
            #cosine attempt
            #curH = math.floor(math.cos(curW) + curW) #choppy results
            #curH = math.floor(curW**1.2)
            curH += math.floor(math.cos(curW)+1) 
            # y = cos(x) + x
            #curH += math.floor(math.cos(curW)) + curW
            curW += 1
            print("river ran! at: " + str(curW) + ", " + str(curH)) #tp
            
        
    return matrix
def drawIsland(matrix): #creates  low elevation nodes on map border
    h = len(matrix)-1
    w = len(matrix[0])-1 #get map dimensions
    #for i in range(0,w):   #doesn't get top of map
     #   for j in range(0,h):
      #      if i == 0 or i == w or j == 0 or j == h: #if we're at endge coord
       #         matrix[i][j] = 0
    for i in range(0,w):
        matrix[0][i] = 0
        matrix[w][i] = 0
        matrix[i][0] = 0
        matrix[i][w] = 0
        
    return matrix
def drawDoubleIsland(matrix): #draws 2 random islands
    h = len(matrix)-1
    w = len(matrix[0])-1 #get map dimensions
    
        
    #for i in range(0,w):   #doesn't get top of map
     #   for j in range(0,h):
      #      if i == 0 or i == w or j == 0 or j == h: #if we're at endge coord
       #         matrix[i][j] = 0
    for i in range(0,w):
        matrix[0][i] = 0
        matrix[w][i] = 0
        matrix[i][0] = 0
        matrix[i][w] = 0

    #axis = r.random()  #runs different each time
    #axis = seed
    w2 = math.floor(w/2) #horizontal midpoint #issue: different for octaves!
    
    #if axis > .5:
    for i in range(0,w):
        matrix[w2][i] = 0
    #if axis <.5:
        #for i in range(0,w):   #enable for 4 islands
         #   matrix[i][w2] = 0
        
        
    return matrix
def drawCaldera(matrix): #too often square
    h = len(matrix)-1
    w = len(matrix[0])-1 #get map dimensions
    #get center of map, lower all points in radius around it
    w2 = math.floor(w/2) #get center point
    h2 = math.floor(h/2) #h and 2 are equal, at least for this version
    radius = math.floor(h/4)
    pi = math.pi
    c = 2*pi*radius
    for i in range(0,w):
        for j in range(0,h):
            #if i < w2 + radius and i > w2 - radius and j < h2+radius and j > h2 - radius:
            dist = math.sqrt((i-w2)**2 + (j-h2)**2) #if point within circle of caldera
            if dist <= radius:
                matrix[i][j] = 0
    return matrix
def sigmoid(x):
  return 1 / (1 + math.exp(-x))
def drawFlatMap(matrix): #creats a flat map (for testing new map features)
    h = len(matrix)
    w = len(matrix[0]) #get map dimensions
    for i in range(0,h):  
        for j in range(0,w):
             matrix[i][j] = 0
    #print('drawFlatMap() ran')
    return matrix
    
def noiseMap(freq, width, hight, style): #I know, spelling, not of concern right now
    ######Global Controllers
    h = freq #height of random matrix
    w = freq #width of random matrix
    mapH = hight#dimensions of the interpolated final height map, iMap
    mapW = width
    backupH = h #height changed to 0 at some point.  check later if still needed
    ######Step 1: 2D Matrix of random values
    rMap = [] #map of random values.  not final map, no interpolation

    #flatMap = False
        
    for i in range(0,h):  #creates a 2d list of random values (0 to 1)
        row = []
        for j in range(0,w):
            row.append(r.random())
        rMap.append(row)
    if style == 'flatMap': 
        rMap = drawFlatMap(rMap)
    if style == 'island':
        rMap = drawIsland(rMap)
    if style == 'doubleIsland':   
        rMap = drawDoubleIsland(rMap)
    if style == 'caldera':   
        rMap = drawCaldera(rMap)
    
    
    #extra step for cylindrical maps
    #make first and last column identical
    for i in range(0,h): #for each height level, aka, each ROW
        #set last element equal to the first
        #rMap[i][h-1]=rMap[i][0] #vertical, not horizontal
        rMap[h-1][i]=rMap[0][i] #works!
    #Extra Step for Rivers
    if style == 'river':
        rMap = drawRiver(rMap)
    ######Step 2: Bilinear Interpolation
    iMap = [] #interpolated map
    for i in range(0,mapH):
        row = []
        for j in range(0,mapW):
            #convert i,j to rMap coordinates
            y = i/mapH * (h-1) #the row of P
            x = j/mapW * (w-1) #the column of P
            x1 = int(x)
            y2 = int(y)
            x2 = x1+1
            y1 = y2+1
            Q12 = rMap[x1][y2]
            Q22 = rMap[x2][y2]
            Q11 = rMap[x1][y1]
            Q21 = rMap[x2][y1]
            #print("x:" + str(x)+ ", y:" + str(y) + ", x1 " + str(x1) + ", y2 "+str(y2) )
            
            #calculate the interpolated value
            newValue = ((y2-y)/(y2-y1)*((x2-x)/(x2-x1)*Q11 + (x-x1)/(x2-x1)*Q21)+(y-y1)/(y2-y1)*((x2-x)/(x2-x1)*Q12+(x-x1)/(x2-x1)*Q22)) 
            row.append(newValue) #append value to row
        iMap.append(row) #building iMap row by row
    #print(str(mapW) + ", " + str(mapH) + str(len(iMap)) + ", " + str(len(iMap[1])))
    return iMap

##Controllers
r.seed(3)
mapW = 300 #careful with values above 1000, takes lots of time
mapH = 300
freq = 2  #"zooms out" on map, more detail per area
smooth = 1.5 #values below 1 raise floors, above one makes lower elevations flat
style = 'caldera' #valid options: island, caldera, doubleIsland, flatMap
baseMap = noiseMap(freq,mapW,mapH, style) #works
octA = noiseMap(freq*2,mapW,mapH, style)  #works
octB = noiseMap(freq*4,mapW,mapH, style)  #works
octC = noiseMap(freq*8,mapW,mapH, style)
baseMap2 = []
for i in range(0,len(octA)):
    row = []
    for j in range(0,len(octA[0])):
        val = baseMap[i][j] + octA[i][j]*0.5 + octB[i][j]*.25 + octC[i][j]*.125 #- .6875
        #val = octC[i][j] #+ baseMap[i][j] + octA[i][j]*0.5 + octB[i][j]*.25 +  #rivers
        #val = pow(val,smooth)
        val = sigmoid(pow(val,smooth)) #puts Z values on 0-1 scale
        row.append(val)
    baseMap2.append(row)
#Addition Height Map Processing
#Testing new draw river function
#baseMap2 = drawRiver(baseMap2) #should draw river on random map



######New Plot: Surface Area 3d
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# Make data.
#X = np.arange(0, mapW, 1)
#Y = np.arange(0, mapH, 1)
#X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
#Z = np.array(baseMap2) #convert Z to array

# Plot the surface.
#customColors = mpl.colors.ListedColormap(['blue', 'green', 'yellow', 'white'])
#bounds = [.9, .95, 1, 1.05, 1.2]
#norm = mpl.colors.BoundaryNorm(bounds, customColors.N)
#surf = ax.plot_surface(X, Y, Z, cmap=cm.terrain,     #cmap changes colors, cm.terrain
 #                      linewidth=0, antialiased=False)
# Customize the z axis.
#ax.set_zlim(0, 1.5)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')
# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

#plt.show()
        
######Old Plot Stuff (2d color map)

#To raise/lower "sea level", need a custom color bar to raise/lower the black parts
#of the graph.

plt.rcParams['figure.dpi'] = 200 #WORKS! Actually changes resolution.
np.random.seed(19680801)
Z = baseMap2
X = np.arange(0, mapW, 1)  
Y = np.arange(0, mapH, 1)  
fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box') # gives square output
ax.pcolormesh(X, Y, Z, shading = 'nearest', cmap=cm.gray)
plt.savefig('savedMap2',dpi = 400) #this works! resolution still too low though
plt.show()
#plt.figure(dpi=200)
#Graphs Terrain colored 2d map
fig, ax = plt.subplots()
ax.pcolormesh(X, Y, Z, shading = 'nearest', cmap=cm.terrain)
#plt.figure(dpi=200) #trying to increase plot resolution#######DPI
#plt.savefig('heightMap.png', dpi = 300) #saves blank image


plt.show()
#plt.savefig('heightMap.png', dpi = 300)
#Graphs 3D map, Terrain Coloring
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.arange(0, mapW, 1)
Y = np.arange(0, mapH, 1)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
Z = np.array(baseMap2) #convert Z to array

# Plot the surface.
customColors = mpl.colors.ListedColormap(['blue', 'green', 'yellow', 'white'])
bounds = [.9, .95, 1, 1.05, 1.2]
norm = mpl.colors.BoundaryNorm(bounds, customColors.N)
surf = ax.plot_surface(X, Y, Z, cmap=cm.terrain,     #cmap changes colors, cm.terrain
                       linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_zlim(0, 1.5)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')
# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.8, aspect=5)
plt.show()


