import glob
import json
import pygame
import numpy as np

class Level:

	def __init__(self, screen=None, width=500, height=500, lvl_path='', spr_path=''):
		self.screen = screen
		self.width = width
		self.height = height
		self.lvl_path = lvl_path
		self.tile = pygame.image.load(spr_path).convert_alpha()
		self.map_data = {}
		self.item_data = {}

	def map_unpack(self):

		with open(f'{self.lvl_path}/lvl.json', 'r') as f:
			self.map_data = json.load(f)

		for key in self.map_data:
			self.item_data[key] = pygame.image.load(f'{self.lvl_path}/{key}.png').convert_alpha()