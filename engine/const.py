'''
Created on 8 sept. 2013

@author: efarhan
'''
import sys

#constant for physics and gameplay
gravity = -20
move = 2
jump = 10 #8.5
jump_step = 5
framerate = 60
animation_step = 12
invulnerability = 60
if sys.platform == 'darwin':
	jump_step = 4
	framerate = 30
	animation_step = 3
	invulnerability = 30

startup = "gameplay"
def log(text):
	sys.stdout.write(str(text)+"\n")