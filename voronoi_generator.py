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
pygame.init()					#importing necessary libraries

#declaring necessary variables 

#COLORS
black=(0,0,0)  #declaring color variables as tuples
white=(255,255,255)
green=(0,255,0)
blue=(0,0,255)

#defining modes
screen_height=600
screen_width=600
dx=[0,1,-1,0]
dy=[-1,0,0,1]
bluesquares=0
greensquares=0
whitesquares=0
dfscounter=1
board=numpy.ndarray((screen_width/20,screen_height/20),dtype=object)
dfs=numpy.ndarray((screen_width/20,screen_height/20),dtype=object)
start = 0
one_over=1
two_over=2.
still=3
mode=0
up=0
down=3
left=2
right=1
true=1
components=[0]
comp=0
comp_count=1
score_max=99999
score_min=-99999
depth_max=5
#declaring global variables


class array:
	value=0
	comp=0
	color="none"
	art="no"
	art_special="no"
class art_points:
	dfsnum=-1
	low=-1
	pos_x=-1
	pos_y=-1
	children=0
	level=0
class minimax_node:
	level=0
	alpha=score_min
	beta=score_max
	value=-1
	move=0
class coordi:
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

def initialize_board():
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y]=array()

def initialize_dfs():
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			dfs[x][y]=art_points()

def voronoi_reset():
	global greensquares,bluesquares,whitesquares
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y].color="none"
	bluesquares=0
	whitesquares=0
	greensquares=0		

def voronoi_diagram(x1,y1,x2,y2):
	global bluesquares,greensquares,whitesquares
	square=rect(x1,y1,20,20)
	voronoi_reset()
	queue1=Queue()
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

	while (not queue1.empty() )or (not queue2.empty()):
		for i in range(0,count1):
			temp=queue1.get()
			count1-=1
			if board[temp.pos_x][temp.pos_y].color=="inter":
				board[temp.pos_x][temp.pos_y].color="blue"
				
				square.left=temp.pos_x*20
				square.top=temp.pos_y*20
				draw.rect(screen,blue,square)
				display.flip()
				bluesquares+=1
				for i in range(0,31):
					pygame.gfxdraw.hline(screen,0,600,i*20,white)
				for i in range (0,31):
					pygame.gfxdraw.vline(screen,i*20,0,600,white)
				display.flip()

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
							square.left=var.pos_x*20
							square.top=var.pos_y*20
							draw.rect(screen,white,square)
							pygame.display.flip()
							whitesquares+=1
							for i in range(0,31):
								pygame.gfxdraw.hline(screen,0,600,i*20,white)
							for i in range (0,31):
								pygame.gfxdraw.vline(screen,i*20,0,600,white)
							display.flip()

							
						elif board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="none":
								var=coordi()
								var.pos_x=temp.pos_x+dx[i]
								var.pos_y=temp.pos_y+dy[i]
								board[var.pos_x][var.pos_y].color="green"
								square.left=var.pos_x*20
								square.top=var.pos_y*20
								draw.rect(screen,green,square)
								pygame.display.flip()
								greensquares+=1
								queue2.put(var)
								count2+=1
								for i in range(0,31):
									pygame.gfxdraw.hline(screen,0,600,i*20,white)
								for i in range (0,31):
									pygame.gfxdraw.vline(screen,i*20,0,600,white)
								display.flip()

								
								
	#return voronoi_calculator(x1,y1,"blue")-voronoi_calculator(x2,y2,"green")

def voronoi_calculator(x,y,color):
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
					if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color==color:
						colorcount+=1
						var=coordi()
						var.pos_x=temp.pos_x+dx[i]
						var.pos_y=temp.pos_y+dy[i]
						queue.put(var)
					if board[temp.pos_x+dx[i]][temp.pos_y+dy[i]].color=="white":
						colorcount+=1
						whitecount+=1
						var=coordi()
						var.pos_x=temp.pos_x+dx[i]
						var.pos_y=temp.pos_y+dy[i]
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

def initialize_board():
	for x in range(0,screen_width/20):
		for y in range(0,screen_height/20):
			board[x][y]=array()

initialize_board()

# "The coordinates should be between 0 and 29"
x1=13  #enter any coordinates for coordinates of player1
y1=12

x2=23	#enter any coordinates for coordinates of player1
y2=14



voronoi_diagram(x1,y1,x2,y2)

