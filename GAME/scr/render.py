import pygame

class Render:

	def __init__(self, screen, level, player):
		self.screen = screen
		self.level = level
		self.player = player

	def render(self):
		drawn_coords = []
		for coord in self.level.map_coords_main:
			self.screen.blit(self.level.tile, 
				(int((self.level.width - 50)/2 + coord[0]*8 - coord[1]*8), 
				int((self.level.height-50)/2 + coord[0]*4 + coord[1]*4 - coord[2]*8))
				)
			drawn_coords.append(coord)
			if coord == tuple(self.player.player_coords):
				break

		self.player.player_rect.x = (self.level.width-50)/2 + 8 * self.player.player_coords[0] - 8 * self.player.player_coords[1]
		self.player.player_rect.y = (self.level.height-50)/2 + 4 * self.player.player_coords[0] + 4 * self.player.player_coords[1] - 8 * self.player.player_coords[2] - 36
		self.screen.blit(self.player.player, self.player.player_rect)
			
		for coord in self.level.map_coords_main:
			if coord in drawn_coords:
				continue
			else:
				self.screen.blit(self.level.tile, 
					(int((self.level.width - 50)/2 + coord[0]*8 - coord[1]*8), 
					int((self.level.height-50)/2 + coord[0]*4 + coord[1]*4 - coord[2]*8))
					)
