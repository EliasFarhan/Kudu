import pygame
from engine.scene import Scene

class Pygame(Scene):
	def init(self):
		self.img_manager.load('data/pygame_logo.png')
		self.ttw = 30*3
	def loop(self, screen):
		self.ttw -= 1
		if self.ttw > 0:
			self.img_manager.show('data/pygame_logo.png', screen, (0,0))
		else:
			import engine.level_manager as level_manager
			level_manager.switch("main_menu")