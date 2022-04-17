import pygame

class Player:

	def __init__(self, screen, spr_path):
		self.screen = screen
		self.player = pygame.image.load(spr_path)
		self.keys = pygame.key.get_pressed()
		self.player_coords = [0, 0, 0]
		self.player_rect = self.player.get_rect(midbottom = (0,0))

	def base_coord_move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.player_coords[0] -= 1 
		elif keys[pygame.K_RIGHT]:
			self.player_coords[0] += 1
		elif keys[pygame.K_UP]:
			self.player_coords[1] -= 1
		elif keys[pygame.K_DOWN]:
			self.player_coords[1] += 1