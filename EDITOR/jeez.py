import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
import numpy
from converter import object_splitter

def map_save(name, data):
	res_list = []
	for z, level in enumerate(data):
		for x, row in enumerate(level):
			for y, rur in enumerate(row):
				if rur:
					res_list.append((x, y, z))

	print(res_list)

	object_splitter(res_list, 'tile.png', 'new')

def single_pos(coord, c_list):
	if len(c_list) == 1:
		return c_list
	else:
		c_list.append(coord)
		return c_list

pygame.init()

TILESIZE = 8
BG_COLOR = (250, 0, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption('Test')
clock = pygame.time.Clock()

wall = False
floor = False

def ch_wall():
	global wall
	if wall:
		wall = False
	else:
		wall = True

def ch_floor():
	global floor
	if floor:
		floor = False
	else:
		floor = True

btn_floor = Button(
    screen, 50, 50, 100, 20, text='Пол',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    hoverColour=(200, 50, 50),
    pressedColour=(0, 255, 0), radius=2,
    onClick=ch_floor
)
btn_wall = Button(
    screen, 50, 80, 100, 20, text='Стена',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=2,
    onClick=ch_wall
)

tile = pygame.image.load('tile.png').convert_alpha()

map_size = 10
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
iso_np = numpy.asarray(iso_matrix)

for coord in coords:
	first_tuple = (iso_matrix[0][0]*coord[0][0] + iso_matrix[0][1]*coord[0][1], iso_matrix[1][0]*coord[0][0] + iso_matrix[1][1]*coord[0][1] + HEIGHT//2)
	second_tuple = (iso_matrix[0][0]*coord[1][0] + iso_matrix[0][1]*coord[1][1], iso_matrix[1][0]*coord[1][0] + iso_matrix[1][1]*coord[1][1] + HEIGHT//2)
	third_tuple = (iso_matrix[0][0]*coord[2][0] + iso_matrix[0][1]*coord[2][1], iso_matrix[1][0]*coord[2][0] + iso_matrix[1][1]*coord[2][1] + HEIGHT//2)
	forth_tuple = (iso_matrix[0][0]*coord[3][0] + iso_matrix[0][1]*coord[3][1], iso_matrix[1][0]*coord[3][0] + iso_matrix[1][1]*coord[3][1] + HEIGHT//2)
	iso_coords.append([first_tuple, second_tuple, third_tuple, forth_tuple])

called_coords = []

press_coord = []

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
			if event.key == pygame.K_w:
				ch_wall()
			if event.key == pygame.K_f:
				ch_floor()
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN:
				level -= 1

	screen.fill((0,0,0))
	mouse_pos = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	btn_floor.draw()
	btn_wall.draw()
	#TODO: implement an auto-filler for walls

	if floor:
		if mouse_press[0]:
			single_pos(mouse_pos, press_coord)

			top_left = press_coord[0]
			top_right = (mouse_pos[0], press_coord[0][1])
			bottom_right = mouse_pos
			bottom_left = (press_coord[0][0], mouse_pos[1])
			
			pygame.draw.polygon(screen, (0, 200, 100), (top_left, top_right, bottom_right, bottom_left), 2)

			for coord in iso_coords:
				coord = [(coord[0][0], coord[0][1] - TILESIZE*level),
				(coord[1][0], coord[1][1] - TILESIZE*level),
				(coord[2][0], coord[2][1] - TILESIZE*level),
				(coord[3][0], coord[3][1] - TILESIZE*level)
				]
				pygame.draw.polygon(screen, BG_COLOR, coord, 1)
				if coord[0][1] > top_right[1] and coord[0][1] < bottom_left[1]:
					if coord[0][0] > top_left[0] and coord[0][0] < bottom_right[0]:
						called = (coord[0][0], coord[0][1] - 11)
						if called not in called_coords:
							called_coords.append(called)
						index = iso_coords.index([(coord[0][0], coord[0][1] + TILESIZE*level),
							(coord[1][0], coord[1][1] + TILESIZE*level),
							(coord[2][0], coord[2][1] + TILESIZE*level),
							(coord[3][0], coord[3][1] + TILESIZE*level)
							])
						coord_data[level][index//map_size][index%map_size] = 1


		if not mouse_press[0]:
			press_coord = []
	else:
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
					if called not in called_coords:
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