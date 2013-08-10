#importing and initializing necessary libraries
import sys,os,logging   #need some modifications in minimax and voronoi, for avoiding draws assume player has already made his move
import pygame
import numpy
import random
from numpy import *
import Queue
from Queue import *
from pygame.locals import *
from pygame import gfxdraw
pygame.init()			#importing necessary libraries

#declaring necessary variables 

#COLORS-declaring color variables as tuples
black=(0,0,0)  
white=(255,255,255)
green=(0,255,0)
blue=(0,0,255)

#defining necessary global variables
#screen dimensions
screen_height=600
screen_width=600
#movement array
dx=[0,1,-1,0]
dy=[-1,0,0,1]
#square count
bluesquares=0
greensquares=0
whitesquares=0
dfscounter=1
#arena represented by a square array of objects
board=numpy.ndarray((screen_width/20,screen_height/20),dtype=object)
dfs=numpy.ndarray((screen_width/20,screen_height/20),dtype=object)
#various modes of game
start = 0
one_over=0
two_over=0
still=3
mode=0
#direction -- kept opposite directions such that their sum is 3
up=0
down=3
left=2
right=1
true=1
#various standard variables for different algorithms
components=[0]
comp=0
comp_count=1
#references for minimax algorithm
score_max=99999
score_min=-99999
depth_max=1




class array: #array object for representing the arena elements
	value=0
	comp=0
	color="none"
	art="no"
	art_visited="no"
class art_points:  #art_points object for calculating articulation points
	dfsnum=-1
	low=-1
	pos_x=-1
	pos_y=-1
	children=0
	level=0
class minimax_node: #object for minimax with alpha beta pruning
	level=0
	alpha=score_min
	beta=score_max
	value=-1
	move=0
class coordi: #object used for voronoi diagram construction
	pos_x=200
	pos_y=200


#graphic objects
screen = pygame.display.set_mode((screen_width,screen_height))  #SEE IF FULLSCREEN NECESSARY
clock=pygame.time.Clock()
keypressed=pygame.key.get_pressed()
music=pygame.mixer.music
mouse=pygame.mouse
sprite=pygame.sprite
rect=pygame.Rect
draw=pygame.draw
display=pygame.display
image=pygame.image
font=pygame.font.Font(None,30)

#initializing the board
def initialize_board():  
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y]=array()

#initializing the dfs array before starting calculating articulation points
def initialize_dfs():
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			dfs[x][y]=art_points()

#resetting color code of the board elements
def voronoi_reset():
	global greensquares,bluesquares,whitesquares
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y].color="none"
			bluesquares=0
			whitesquares=0
			greensquares=0
#blue glider object
class blueglider:           
	glider_color=blue
	glider_id=1
	art_check=0  #an aid for huggwall function
	#images for different directions of movement
	glider_up=image.load("blueup.png").convert_alpha()
	glider_down=image.load("bluedown.png").convert_alpha()
	glider_right=image.load("blueright.png").convert_alpha()
	glider_left=image.load("blueleft.png").convert_alpha()
	glider_up=pygame.transform.scale(glider_up,(20,20))
	glider_down=pygame.transform.scale(glider_down,(20,20))
	glider_right=pygame.transform.scale(glider_right,(20,20))
	glider_left=pygame.transform.scale(glider_left,(20,20))
	comp=0
	pos_x=(screen_width/4)+10
	pos_y=screen_height/2
	def __init__(self):     #initiliazing the glider
		screen.blit(self.glider_right,(self.pos_x,self.pos_y))
		display.flip()
		board[self.pos_x/20][self.pos_y/20].value=1
		self.pos_x=(screen_width/4)+10
		self.pos_y=screen_height/2
	
#green glider object
class greenglider:  #same for green glider
	glider_color=green
	glider_id=2
	#images for different directions of movement
	glider_up=image.load("greenup.png").convert_alpha()
	glider_down=image.load("greendown.png").convert_alpha()
	glider_right=image.load("greenright.png").convert_alpha()
	glider_left=image.load("greenleft.png").convert_alpha()
	glider_up=pygame.transform.scale(glider_up,(20,20))
	glider_down=pygame.transform.scale(glider_down,(20,20))
	glider_right=pygame.transform.scale(glider_right,(20,20))
	glider_left=pygame.transform.scale(glider_left,(20,20))
	comp=0
	pos_x=(3*screen_width)/4+10
	pos_y=screen_height/2
	def __init__(self):
		screen.blit(self.glider_left,(self.pos_x,self.pos_y))
		display.flip()
		board[self.pos_x/20][self.pos_y/20].value=1
		self.pos_x=((3*screen_width)/4)+10
		self.pos_y=screen_height/2
	#getting move of glider
	def tronmove(self):
		return which_move()

class initialize:   #initializes and loads the arena
	def __init__(self):
		music.load("music.mp3")
		music.play(-1)
		display.set_caption("Tron the legacy")




def gameplay(object1,object2,move1,move2):
	
	(x,y)=(object2.pos_x,object2.pos_y)  # in get coordi, return x and y in multiples of 20
	#updating the components and articulation points
	if board[object1.pos_x/20][object1.pos_y/20].art=="no":
		
		object1.art_check=0
		components[board[object1.pos_x/20][object1.pos_y/20].comp] -= 1
	
	else:
		
		
		object1.art_check=1   #checking if bot has entered an articulation point
		calc_components()
		
	if board[x/20][y/20].art=="no":
		
		components[board[x/20][y/20].comp] -= 1
		calc_artpoints()
		
	else:
		
		calc_components()
		calc_artpoints()
		
	#deciding game move
	
	if object1.comp==object2.comp:
		
		return minimax_move(object1,object2)
	else:
		
		return huggwall(object1,move1)
			

	
#resetting the articulation point nodes
def artpoint_reset():
	for i in range(0,screen_width/20):
		for j in range(0,screen_height/20):
			board[i][j].art="no"
			board[i][j].art_visited="no"

def component_reset(): 							#function for resetting the component element of every square
	for i in range(0,screen_width/20):
		for j in range(0,screen_height/20):
			board[i][j].comp=0

def calc_components(): 							 #for finding the connected components in the arena
	global comp,comp_count
	comp=0
	
	component_reset() 							 #resetting the components before calculation
	for i in range(0,comp_count):					#resetting number of nodes under each component
		components[i]=0
	for j in range(0,screen_height/20):
		for i in range(0,screen_width/20):
			if board[i][j].value==1:    #ignore wall
				continue
			else:
				if i-1>=0 and j-1>=0:  
					if board[i-1][j-1].value==0:
						if board[i][j-1].value==0:
							board[i][j].comp=board[i][j-1].comp
							components[board[i][j].comp] +=1
						elif board[i-1][j].value==0:
							board[i][j].comp=board[i-1][j].comp
							components[board[i][j].comp] +=1
						else:
							comp+=1
							if comp==comp_count:
								components.append(0)
								comp_count+=1
							board[i][j].comp=comp
							components[comp]+=1
					else:
						if board[i][j-1].value==0:
							if board[i-1][j].value==0:
								if board[i][j-1].comp==board[i-1][j].comp:
									board[i][j].comp==board[i][j-1].comp
									components[board[i][j].comp]+=1
								else:
									if board[i][j-1].comp<board[i-1][j].comp:
										board[i][j].comp=board[i][j-1].comp
										components[board[i][j].comp]+=1
										replace(board[i][j-1].comp,board[i-1][j].comp)
										
									else:
										board[i][j].comp=board[i-1][j].comp
										components[board[i][j].comp]+=1
										replace(board[i-1][j].comp,board[i][j-1].comp)
										
							else:
								board[i][j].comp=board[i][j-1].comp
								components[board[i][j].comp]+=1
						elif board[i-1][j].value==0:
							board[i][j].comp=board[i-1][j].comp
							components[board[i][j].comp] +=1
						else:
							comp+=1
							if comp==comp_count:
								components.append(0)
								comp_count+=1
							board[i][j].comp=comp
							components[comp]+=1
							
				elif i-1<0 or j-1<0:
					if i-1<0 and j-1<0:
						board[i][j].comp=comp
						
					elif i-1<0:
						if board[i][j-1].value==0:
							board[i][j].comp==board[i][j-1].comp
							components[board[i][j].comp]+=1
						else:
							comp+=1
							if comp==comp_count:
								components.append(0)
								comp_count+=1
							board[i][j].comp=comp
							components[comp]+=1
					else :
						if board[i-1][j].value==0:
							board[i][j].comp==board[i-1][j].comp
							components[board[i][j].comp]+=1
						else:
							comp+=1
							if comp==comp_count:
								components.append(0)
								comp_count+=1
							board[i][j].comp=comp
							components[comp]+=1

#replace function's purpose is to reallocate comp if a node connects two previously disconnected components
def replace(comp1,comp2):
	global comp_count,comp
	while comp2<comp_count:
		for j in range(0,screen_height/20):
			for i in range(0,screen_width/20):
				if board[i][j].comp==comp2 and board[i][j].value==0:
					board[i][j].comp=comp1
					components[comp1]+=1
		components[comp2]=0
		comp1=comp2
		comp2=comp2+1
	comp_count-=1
	comp-=1
		

def get_coordi(object,move2):
	if(move2==up):
		return (object.pos_x,object.pos_y-20)
	elif(move2==down):
		return (object.pos_x,object.pos_y+20)
	elif(move2==left):
		return (object.pos_x-20,object.pos_y)
	else:
		return (object.pos_x+20,object.pos_y)
#function for calculating the articulation points in the given arena
def calc_artpoints():
	
	initialize_dfs()
	artpoint_reset()
	global dfscounter
	dfscounter=1
	
	for j in range(0,screen_height/20):
		for i in range(0,screen_width/20):
			if board[i][j].value==0:
					if dfs[i][j].dfsnum==-1:
						
						dfs_graph(i,j)

			
	

#depth first search algorithm for finding the articulation points in a connected component
def dfs_graph(x,y):
	global dfscounter
	dfs[x][y].dfsnum=dfscounter
	dfscounter+=1
	dfs[x][y].low=dfs[x][y].dfsnum
	for i in range(0,4):
		if (x+dx[i]>=0 and x+dx[i]<screen_width/20) and (y+dy[i]>=0 and y+dy[i]<screen_height/20):
			if board[x+dx[i]][y+dy[i]].value==0:
				if dfs[x+dx[i]][y+dy[i]].dfsnum==-1:
					dfs[x][y].children+=1
					dfs[x+dx[i]][y+dy[i]].level=dfs[x][y].level+1
					dfs_graph(x+dx[i],y+dy[i])
					dfs[x][y].low=min(dfs[x][y].low,dfs[x+dx[i]][y+dy[i]].low)
					if dfs[x][y].dfsnum==1:
						if dfs[x][y].children>=2:
							board[x][y].art="yes"
							
							
							
					elif dfs[x+dx[i]][y+dy[i]].low>=dfs[x][y].dfsnum:
						board[x][y].art="yes"
						
						
						
				elif dfs[x+dx[i]][y+dy[i]].level<dfs[x][y].level-1:
					dfs[x][y].low=min(dfs[x][y].low,dfs[x+dx[i]][y+dy[i]].dfsnum)
	
#function to draw the voronoi diagram for the two players
def voronoi_diagram(x1,y1,x2,y2):
	global bluesquares,greensquares,whitesquares
	#resetting the color attribute of each square to none
	voronoi_reset()
	queue1=Queue() #2 queues for inserting nodes(coordinates of the neighbouring non-wall square) to be evaluated
	queue2=Queue()
	bluesquares=0
	greensquares=0
	whitesquares=0
	coordi1=coordi()
	coordi2=coordi()
	coordi1.pos_x=x1
	coordi1.pos_y=y1
	coordi2.pos_x=x2
	coordi2.pos_y=y2
	queue1.put(coordi1)
	queue2.put(coordi2)
	count1=1
	count2=1
	board[x1][y1].value=1
	board[x2][y2].value=1

	while (not queue1.empty() )or (not queue2.empty()):  #until all squares are evaluated
		for i in range(0,count1):
			temp=queue1.get()
			count1-=1
			if board[temp.pos_x][temp.pos_y].color=="inter":
				board[temp.pos_x][temp.pos_y].color="blue"
				bluesquares+=1
			if board[temp.pos_x][temp.pos_y].color =="none" or board[temp.pos_x][temp.pos_y].color =="blue":
				for i in range(0,4):
					if temp.pos_x+dx[i]>=0 and temp.pos_x+dx[i]<screen_width/20 and temp.pos_y+dy[i]>=0 and temp.pos_y+dy[i]<screen_height/20:
						if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].value==0:
							if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="none":
								var=coordi()
								var.pos_x=temp.pos_x+dx[i]
								var.pos_y=temp.pos_y+dy[i]
								board[var.pos_x][var.pos_y].color="inter"
								queue1.put(var)
								count1+=1

						
		for i in range(0,count2):
			temp=queue2.get()
			count2-=1
			for i in range(0,4):
				if temp.pos_x+dx[i]>=0 and temp.pos_x+dx[i]<screen_width/20 and temp.pos_y+dy[i]>=0 and temp.pos_y+dy[i]<screen_height/20:
					if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].value==0:
						if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="inter":
							var=coordi()
							var.pos_x=temp.pos_x+dx[i]
							var.pos_y=temp.pos_y+dy[i]
							
							board[var.pos_x][var.pos_y].color="white"
							queue2.put(var)
							count2+=1
							whitesquares+=1
							 
						elif board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="none":
								var=coordi()
								var.pos_x=temp.pos_x+dx[i]
								var.pos_y=temp.pos_y+dy[i]
								board[var.pos_x][var.pos_y].color="green"
								greensquares+=1
								queue2.put(var)
								count2+=1
								
	#relative advantage of bot over player.. the heuristic for minimax
	return voronoi_calculator(x1,y1,"blue")-voronoi_calculator(x2,y2,"green")

def minimax_move(object1,object2): 
	x1=object1.pos_x/20
	y1=object1.pos_y/20
	x2=object2.pos_x/20
	y2=object2.pos_y/20
	node=minimax_node()
	
	comp=board[x1][y1].comp
	
	node= predict_move(node,x1,y1,x2,y2,comp,comp,0)
	calc_components()
	calc_artpoints()
	
	return node.move

def predict_move(node1,x1,y1,x2,y2,comp1,comp2,level):
	global depth_max,score_min,score_max
	node=minimax_node()
	node.alpha=node1.alpha
	node.beta=node1.beta

	if(level<depth_max):
		if level%2==0:  #max node
			
			for i in range(0,4):
				
				if node.alpha<=node.beta:	
					node_temp=minimax_node()
					if x1+dx[i]<0 or x1+dx[i]>=screen_width/20 or y1+dy[i]<0 or y1+dy[i]>=screen_height/20:
						node.value=max(score_min,node.value)
						
					elif board[x1+dx[i]][y1+dy[i]].value==1:
						node.value=max(node.value,score_min)
						
					else:
						x1=x1+dx[i]
						y1=y1+dy[i]
						board[x1][y1].value=1 	#making a wall for the corresponding move
						node_temp=predict_move(node,x1,y1,x2,y2,comp1,comp2,level+1)
						board[x1][y1].value=0	#reverting the changes
														
												

						if level==0:
							if node.alpha<=node_temp.value: #determining best move at the first level
								node.move=i
								node.alpha=node_temp.value
						node.alpha=max(node.alpha,node_temp.value)
						x1=x1-dx[i]
						y1=y1-dy[i]
						

						
				else:
					break
				
			node.value=node.alpha
			return node
		if level%2==1 :   #min node
			for i in range(0,4):
				

				if node.alpha<=node.beta:	
					node_temp=minimax_node()
					
					if x2+dx[i]<0 or x2+dx[i]>=screen_width/20 or y2+dy[i]<0 or y2+dy[i]>=screen_height/20:
						node.value=min(score_max,node.value)
						
					elif board[x2+dx[i]][y2+dy[i]].value==1:
						node.value=min(node.value,score_max)
						
					else:
						x2=x2+dx[i]
						y2=y2+dy[i]
						
						board[x2][y2].value=1
						node_temp=predict_move(node,x1,y1,x2,y2,comp1,comp2,level+1)
						board[x2][y2].value=0
																			
						
							

						x2=x2-dx[i]
						y2=y2-dy[i]
						
						node.beta=min(node_temp.value,node.beta)
						

				else:
					break
				
				node.value=node.beta
			return node
	if level==depth_max:
		calc_components()
		calc_artpoints()
		if board[x1][y1].comp==board[x2][y2].comp:
			node.value=voronoi_diagram(x1,y1,x2,y2)
		else:
			node.value=voronoi_diagram(x1,y1,x2,y2)*100 #multiplication by 100 emphasizes that nothing can be changed after going into disconnected components
		return node

def voronoi_calculator(x,y,color):  #analyses the voronoi area of each player to get effective available area under its control
	queue=Queue()
	coordi1=coordi()
	coordi1.pos_x=x
	coordi1.pos_y=y
	queue.put(coordi1)
	colorcount=0
	whitecount=0
	
	while not queue.empty():
		temp=queue.get()
		
		
		for i in range(0,4):
			if temp.pos_x+dx[i]>=0 and temp.pos_x+dx[i]<screen_width/20 and temp.pos_y+dy[i]>=0 and temp.pos_y+dy[i]<screen_height/20:
				if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].value==0 and board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].art=="no":
					if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].art_visited=="no":	
						if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color==color:
							colorcount+=1
							var=coordi()
							var.pos_x=temp.pos_x+dx[i]
							var.pos_y=temp.pos_y+dy[i]
							board[var.pos_x][var.pos_y].art_visited="yes"
							queue.put(var)
							
						if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="white":
							colorcount+=1
							whitecount+=1
							var=coordi()
							var.pos_x=temp.pos_x+dx[i]
							var.pos_y=temp.pos_y+dy[i]
							board[var.pos_x][var.pos_y].art_visited="yes"
							queue.put(var)
							
	
	if whitecount>0:
		if color=="blue":
			return bluesquares
		else:
			return greensquares
	else:
		if color=="blue":
			
			return max(colorcount,bluesquares-colorcount)
		else:
			
			return max(colorcount,greensquares-colorcount)

#function for effective filling space
def huggwall(object,pre_move):
	x=object.pos_x/20
	y=object.pos_y/20
	max=-1
	if object.art_check==1: #if we have to forcefully enter an articulation point, then go into the largest space
		move=0
		max=-1
		for i in range(0,4):
			if x+dx[i]>=0 and x+dx[i]<screen_width/20 and y+dy[i]>=0 and y+dy[i]<screen_height/20:
				if board[x+dx[i]][y+dy[i]].value==0:
					if max<components[board[x+dx[i]][y+dy[i]].comp]:
						max=components[board[x+dx[i]][y+dy[i]].comp]
						move=i
		object.art_check=0
		return move
		
	art_max=-1
	if pre_move!=up:
		move=up
		art_move=up
	else:
		move=down
		art_move=down
	#up
	if pre_move!=3-up and y-1>=0:
		if board[x][y-1].value==0:
			count=0
			count=count_neighbours(x,y-1)
			if max<count and board[x][y-1].art=="no":
				max=count
				move=up
			else:
				if art_max<components[board[x][y-1].comp]:
					art_max=components[board[x][y-1].comp]
					art_move=up
		#down
	if pre_move!=3-down and y+1<screen_height/20:
		if board[x][y+1].value==0 :
			count=0
			count=count_neighbours(x,y+1)
			if max<count and board[x][y+1].art=="no":
				max=count
				move=down
			else:
				if art_max<components[board[x][y+1].comp]:
					art_max=components[board[x][y+1].comp]
					art_move=down
		#left
	if pre_move!=3-left and x-1>=0:
		if board[x-1][y].value==0:
			count=0
			count=count_neighbours(x-1,y)
			if max<count and board[x-1][y].art=="no":
				max=count
				move=left
			else:
				if art_max<components[board[x-1][y].comp]:
					art_max=components[board[x-1][y].comp]
					art_move=left
		#right
	if pre_move!=3-right and x+1<screen_width/20:
		if board[x+1][y].value==0:	
			count=0
			count=count_neighbours(x+1,y)
			if max<count and board[x+1][y].art=="no":
				max=count
				move=right
			else:
				if art_max<components[board[x+1][y].comp]:
					art_max=components[board[x+1][y].comp]
					art_move=right
	if max>-1:
		return move
	else:
		return art_move
#returns no of neighbouring walls for a square
def count_neighbours(x,y):
	count=0
	if x-1>=0 and y-1>=0 and x+1<screen_width/20 and y+1<screen_height/20:
		count=board[x-1][y-1].value+board[x-1][y].value+board[x-1][y+1].value+board[x][y-1].value
		count=count+board[x][y+1].value+board[x+1][y].value+board[x+1][y-1].value+board[x+1][y+1].value
	elif x-1<0 and y-1<0:
		count=board[x+1][y].value+board[x+1][y+1].value+board[x][y+1].value+5
	elif x+1>=screen_width/20 and y+1>=screen_height/20:
		count = board[x-1][y].value+board[x-1][y-1].value+board[x][y-1].value+5
	elif x+1>=screen_width/20 and y-1<0:
		count = board[x][y+1].value+board[x-1][y].value+board[x-1][y+1].value+5
	elif y+1>=screen_height/20 and x-1<0:
		count = board[x][y-1].value+board[x+1][y].value+board[x+1][y-1].value+5
	elif x-1<0:
		count = board[x+1][y].value+board[x][y-1].value+board[x][y+1].value+board[x+1][y-1].value+board[x+1][y+1].value+3
	elif x+1>=screen_width/20:
		count = board[x-1][y].value+board[x][y-1].value+board[x][y+1].value+board[x-1][y-1].value+board[x-1][y+1].value+3
	elif y-1<0:
		count = board[x+1][y].value+board[x-1][y].value+board[x][y+1].value+board[x+1][y+1].value+board[x-1][y+1].value+3
	elif y+1>=screen_height/20:
		count=board[x+1][y].value+board[x-1][y].value+board[x][y-1].value+board[x+1][y-1].value+board[x-1][y-1].value+3
	return count
	




#initialize the board elements
def initialize_board():
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y]=array()
#get the move for the human player
def which_move():   #gets the move of the player
	clock.tick(15)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==KEYDOWN:
			if event.key==K_LEFT:
				return left
			elif event.key==K_RIGHT:
				return right
			elif event.key==K_UP:
				return up
			elif event.key==K_DOWN:
				return down
			elif event.key==K_q:
				sys.exit()
		else:
			return -1
#contains all the functions for display effect
class moves:    #various functions to show case moves and correct invalid moves
	def correct_move(self,pre_move,move): #make sure move is valid
		if(move==-1 or move==None):
			return pre_move
		if(pre_move==move):
			return move
		if(pre_move==left or pre_move==right) and (move==up or move==down):
			return move
		if(pre_move==up or pre_move==down) and (move==right or move==left):
			return move
		if(pre_move==up and move==down) or (pre_move==down and move==up):
			return pre_move
		if(pre_move==left and move==right) or (pre_move==right and move==left):
			return pre_move

	def show_move(self,object,move): #display the move on screen, respectively, up down,or left-right
		if(move==up):
			self.moveup(object)
		elif(move==down):
			self.movedown(object)
		elif(move==left):
			self.moveleft(object)
		elif(move==right):
			self.moveright(object)

	def moveup(self,object):
		temp=rect(object.pos_x,object.pos_y,20,20)
		x1=object.pos_x
		y1=object.pos_y+18
		rect_hor=rect(x1,y1,2,20)
		rect_ver=rect(x1,y1,20,2)
		for i in range(1,11):
			clock.tick(300)
			draw.rect(screen,black,temp)
			object.pos_y-=2
			screen.blit(object.glider_up,(object.pos_x,object.pos_y))
			display.flip()
			draw.rect(screen,object.glider_color,rect_ver)
			display.flip()
			rect_ver.top-=2
			temp.top-=2

	def movedown(self,object):
		temp=rect(object.pos_x,object.pos_y,20,20)
		x1=object.pos_x
		y1=object.pos_y
		rect_hor=rect(x1,y1,2,20)
		rect_ver=rect(x1,y1,20,2)
		for i in range(1,11):
			clock.tick(300)
			draw.rect(screen,black,temp)
			object.pos_y+=2
			screen.blit(object.glider_down,(object.pos_x,object.pos_y))
			display.flip()
			draw.rect(screen,object.glider_color,rect_ver)
			display.flip()
			rect_ver.top+=2
			temp.top+=2

	def moveright(self,object):
		temp=rect(object.pos_x,object.pos_y,20,20)
		x1=object.pos_x
		y1=object.pos_y
		rect_hor=rect(x1,y1,2,20)
		rect_ver=rect(x1,y1,20,2)
		for i in range(1,11):
			clock.tick(300)
			draw.rect(screen,black,temp)
			object.pos_x+=2
			screen.blit(object.glider_right,(object.pos_x,object.pos_y))
			display.flip()
			draw.rect(screen,object.glider_color,rect_hor)
			display.flip()
			rect_hor.left+=2
			temp.left+=2

	def moveleft(self,object):
		temp=rect(object.pos_x,object.pos_y,20,20)
		x1=object.pos_x+18
		y1=object.pos_y
		rect_hor=rect(x1,y1,2,20)
		rect_ver=rect(x1,y1,20,2)
		for i in range(1,11):
			clock.tick(300)
			draw.rect(screen,black,temp)
			object.pos_x-=2
			screen.blit(object.glider_left,(object.pos_x,object.pos_y))
			display.flip()
			draw.rect(screen,object.glider_color,rect_hor)
			display.flip()
			rect_hor.left-=2
			temp.left-=2


		

def checkcollision(object,move):   #check whether a bot has crashed into a wall
	if(move==up):
		if object.pos_y-20<0:
			return true
		elif board[object.pos_x/20][object.pos_y/20-1].value==1:
			return true
		else:
			return not true
	if(move==down):
		if object.pos_y+20>=screen_height:
			return true
		elif board[object.pos_x/20][object.pos_y/20+1].value==1:
			return true
		else:
			return not true
	if(move==left):
		if object.pos_x-20<0:
			return true
		elif board[object.pos_x/20-1][object.pos_y/20].value==1:
			return true
		else:
			return not true
	if(move==right):
		if object.pos_x+20>=screen_width:
			return true
		elif board[object.pos_x/20+1][object.pos_y/20].value==1:
			return true
		else:
			return not true

	
def update_board(object): #update the board and object upon movement
	board[object.pos_x/20][object.pos_y/20].value=1
	object.comp=board[object.pos_x/20][object.pos_y/20].comp
	
	


def notification(message):  #for displaying notifications 
	size=font.size(message)
	font_surface=font.render(message,False,white)
	fontx=(screen_width-size[0])/2
	fonty=(screen_height-size[1])/2
	screen.blit(font_surface,(fontx,fonty))
	display.flip()

def board_reset():  #resetting the arena, on screen and on array
	for i in range(0,screen_width/20):
		for j in range(0,screen_height/20):
			board[i][j]=array()












a=initialize()  #initializing the arena
initialize_board()
blueglider=blueglider()
greenglider=greenglider()
move=moves()  #object for moves class to get moves of player
move1=right
move2=left
pre_move1=move1  #storing previous moves--necessary to avoid wrong moves
pre_move2=move2
sys.setrecursionlimit(20000)  #recursion depth limit exceeded just in case
calc_components()  
calc_artpoints()
for i in range(0,31):
	pygame.gfxdraw.hline(screen,0,600,i*20,white)
for i in range (0,31):
	pygame.gfxdraw.vline(screen,i*20,0,600,white)
display.flip()

while 1:
	if(mode==still):   #resetting the arena and variables
		comp_count=1
		comp=0
		one_over=0
		two_over=0
		background=rect(0,0,screen_width,screen_height)
		draw.rect(screen,black,background)
		for i in range(0,31):
			pygame.gfxdraw.hline(screen,0,600,i*20,white)
		for i in range (0,31):
			pygame.gfxdraw.vline(screen,i*20,0,600,white)
		display.flip()

		pygame.display.flip()
		blueglider.__init__()
		greenglider.__init__()

		initialize_board()
		blueglider.comp=0
		greenglider.comp=0
		move1=right
		move2=left
		pre_move1=move1
		pre_move2=move2
		calc_components()
		calc_artpoints()
		notification("PRESS SPACE TO START")
		display.flip()
		pygame.time.delay(1000)
		for event in pygame.event.get():  #using event attribute of pygame to get pressed key
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:   #start game is Space is pressed
					mode=start
					draw.rect(screen,black,background)
					pygame.display.flip()
					blueglider.__init__()
					greenglider.__init__()
					display.flip()


				elif event.key == K_q:  #quit game if q is pressed
					pygame.quit()
					sys.exit()
	elif one_over and (not two_over):  #check if player wins"
		notification("YOU WIN")
		pygame.time.delay(1000)
		mode=still
	
	elif two_over and not one_over:  #check if bot wins
		notification("COMPUTER KICKED YOUR ASS")
		pygame.time.delay(1000)
		mode=still

	elif one_over and two_over:  #check if draw
		notification("DRAW")
		pygame.time.delay(1000)
		mode=still

	elif(mode==start):   #game in progress
		clock.tick(600)  	#setting the frame rate
		

		
		#getting move of the bot
		move1=gameplay(blueglider,greenglider,move1,move2)
		move1=move.correct_move(pre_move1,move1)
		if not checkcollision(blueglider,move1):
			move.show_move(blueglider,move1)
			#(blueglider.pos_x,blueglider.pos_y)=update_coordinates(move1,blueglider.pos_x,blueglider.pos_y)
			pre_move1=move1
			pygame.display.flip()
			update_board(blueglider)
		else:
			one_over=1
		for i in range(0,31):
			pygame.gfxdraw.hline(screen,0,600,i*20,white)
		for i in range (0,31):
			pygame.gfxdraw.vline(screen,i*20,0,600,white)
		display.flip()
	


		move2=greenglider.tronmove()
		move2=move.correct_move(pre_move2,move2)
		if not checkcollision(greenglider,move2):
			move.show_move(greenglider,move2)
			#(greenglider.pos_x,greenglider.pos_y)=update_coordinates(move2,greenglider.pos_x,greenglider.pos_y)
			pre_move2=move2
			pygame.display.flip()
			update_board(greenglider)
				
		else:
			two_over=1
		for i in range(0,31):
			pygame.gfxdraw.hline(screen,0,600,i*20,white)
		for i in range (0,31):
			pygame.gfxdraw.vline(screen,i*20,0,600,white)
		display.flip()

	