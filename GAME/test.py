import pygame
from sys import exit
from scr.level import Level
from scr.player import Player
from scr.render import Render

def main():
	pygame.init()

	WIDTH, HEIGHT = 500, 500
	BG_COLOR = (0, 0, 0)

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Test')
	clock = pygame.time.Clock()

	level = Level(screen, WIDTH, HEIGHT, 'lvl/new1', 'spr/Tile.png')
	player = Player(screen, 'spr/player.png')
	level.map_unpack()

	render = Render(screen, level, player)

	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()

		#player.base_coord_move()
		render.render()

		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()