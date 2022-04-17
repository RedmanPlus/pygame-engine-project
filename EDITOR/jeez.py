import pygame
import numpy
import os

#TODO: Repair a saving function

def map_save(name, data):
	for layer in data:
		print(data)
	os.mkdir(name)
	inter = []
	for line in data[0]:
		for layer in data:
			inter.append(layer[data[0].index(line)])
	npcs = numpy.asarray(inter).reshape((len(data[0]), len(data), len(data[0][0])))
	res_list = []
	for i in reversed(range(len(npcs))):
		res_list.append(npcs[i].tolist())
	counter = 0
	print(res_list)
	for layer in res_list:
		write_str = str()
		for line in layer:
			str_line = [str(i) for i in line]
			write_str = write_str + ''.join(str_line) + '\n'
		with open(f'{name}/{counter}.txt', 'w') as f:
			f.write(write_str)
		counter += 1


pygame.init()

TILESIZE = 8
BG_COLOR = (250, 0, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

tile = pygame.image.load('tile.png').convert_alpha()

map_size = 15
height = 6
level = 0
coord_data = [[[0 for l in range(map_size)] for j in range(map_size)] for i in range(height)]

dim_map = map_size*TILESIZE

x_first, y_first = 0, 0
x_last, y_last = TILESIZE, TILESIZE

coords = []

while x_last != dim_map + TILESIZE:
	y_first, y_last = 0, TILESIZE
	while y_last != dim_map + TILESIZE:
		coords.append([(x_first, y_first), (x_last, y_first), (x_last, y_last), (x_first, y_last)])
		y_first, y_last = y_last, y_last + TILESIZE
	x_first, x_last = x_last, x_last + TILESIZE

iso_coords = []

iso_matrix = [[1, 1],[-0.5, 0.5]]

for coord in coords:
	first_tuple = (iso_matrix[0][0]*coord[0][0] + iso_matrix[0][1]*coord[0][1], iso_matrix[1][0]*coord[0][0] + iso_matrix[1][1]*coord[0][1] + HEIGHT//2)
	second_tuple = (iso_matrix[0][0]*coord[1][0] + iso_matrix[0][1]*coord[1][1], iso_matrix[1][0]*coord[1][0] + iso_matrix[1][1]*coord[1][1] + HEIGHT//2)
	third_tuple = (iso_matrix[0][0]*coord[2][0] + iso_matrix[0][1]*coord[2][1], iso_matrix[1][0]*coord[2][0] + iso_matrix[1][1]*coord[2][1] + HEIGHT//2)
	forth_tuple = (iso_matrix[0][0]*coord[3][0] + iso_matrix[0][1]*coord[3][1], iso_matrix[1][0]*coord[3][0] + iso_matrix[1][1]*coord[3][1] + HEIGHT//2)
	iso_coords.append([first_tuple, second_tuple, third_tuple, forth_tuple])

called_coords = []

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			if event.key == pygame.K_s:
				map_save('test', coord_data)
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN:
				level -= 1

	#TODO: implement an auto-filler for floor and walls

	screen.fill((0,0,0))
	mouse_pos = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	for coord in iso_coords:
		coord = [(coord[0][0], coord[0][1] - TILESIZE*level),
		(coord[1][0], coord[1][1] - TILESIZE*level),
		(coord[2][0], coord[2][1] - TILESIZE*level),
		(coord[3][0], coord[3][1] - TILESIZE*level)
		]
		pygame.draw.polygon(screen, BG_COLOR, coord, 1)
		if coord[3][0] - mouse_pos[0] <= TILESIZE and coord[3][0] - mouse_pos[0] > 0 and coord[3][1] - mouse_pos[1] <= TILESIZE and coord[3][1] - mouse_pos[1] > 0:
			called = (coord[0][0], coord[0][1] - 11)
			if mouse_press[0]:
				pygame.draw.circle(screen, BG_COLOR, coord[1], 4, 0)
				called_coords.append(called)
				index = iso_coords.index([(coord[0][0], coord[0][1] + TILESIZE*level),
					(coord[1][0], coord[1][1] + TILESIZE*level),
					(coord[2][0], coord[2][1] + TILESIZE*level),
					(coord[3][0], coord[3][1] + TILESIZE*level)
					])
				coord_data[level][index//map_size][index%map_size] = 1

	for coord in called_coords:
		screen.blit(tile, coord)
	

	pygame.display.update()
	clock.tick(60)