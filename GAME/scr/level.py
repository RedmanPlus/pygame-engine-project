import glob
import pygame

class Level:
	
	def __init__(self, screen=None, width=500, height=500, lvl_path='', spr_path=''):
		self.screen = screen
		self.width = width
		self.height = height
		self.lvl_path = lvl_path
		self.tile = pygame.image.load(spr_path).convert_alpha()
		self.map_data = []
		self.map_coords_main = []

	def map_unpack(self):
		file_list = glob.glob(self.lvl_path)

		for file in file_list:
			with open(file, 'r') as f:
				data = [[int(c) for c in row] for row in f.read().split('\n')]
				self.map_data.append(data)

	def get_coords(self):
		for y, level in enumerate(self.map_data):
			for z, row in enumerate(level):
				for x, rur in enumerate(row):
					if rur:
						self.map_coords_main.append((x, y, z))