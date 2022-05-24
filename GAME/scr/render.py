import pygame
import numpy

class Render:

	def __init__(self, screen, level, player):
		self.screen = screen
		self.level = level
		self.player = player
		self.render_coords = []

	def render(self):
		for key, value in self.level.item_data.items():
			self.screen.blit(value, tuple(self.level.map_data[key]['pos']))
