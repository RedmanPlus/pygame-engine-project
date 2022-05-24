import os
import json
from itertools import chain
from PIL import Image
import numpy as np

def jsonify(func):
	def inner(*args, **kwargs):
		result = func(*args, **kwargs)
		with open(f'{result[1]}\\lvl.json', 'w') as f:
			json.dump(result[0], f)
	return inner

def constructor(func):
	def inner(*args, **kwargs):
		result = func(*args, *kwargs)
		os.mkdir(result[1])
		for elem in result[0]:
			coords = result[0][elem]['coords']
			tile = result[0][elem]['tiles']
			canvas = Image.new('RGBA', result[0][elem]['shape'], (255, 0, 0, 0))
			img = Image.open(tile, 'r')
			img = img.convert('RGBA')
			for coord in coords:
				canvas.paste(img, coord, img)

			canvas.save(f'{result[1]}\\{elem}.png')

			del result[0][elem]['coords']
			del result[0][elem]['pos'][2:]
		return result
	return inner

def iso_convert(func):
	def inner(*args, **kwargs):
		result = func(*args, **kwargs)
		scale_matrix = np.asarray([[8,0], [0, 8]])
		iso_matrix = np.asarray([[1, 1],[-0.5, 0.5]])
		for elem in result[0]:
			fin = []
			for coord in result[0][elem]['coords']:
				npcoord = np.asarray(coord[0:2])
				npcoord = scale_matrix.dot(npcoord)
				npcoord = iso_matrix.dot(npcoord)
				iso_coord = npcoord.tolist()
				iso_coord[1] = iso_coord[1] - coord[2]*8
				iso_coord[0] = int(iso_coord[0])
				iso_coord[1] = int(iso_coord[1])
				fin.append(iso_coord)
			min_of_mins = min([min(x) for x in fin])
			for ind, coord in enumerate(fin):
				fin[ind][1] -= min_of_mins

			max_x = max([x[0] for x in fin])
			max_y = max([y[1] for y in fin])

			result[0][elem]['coords'] = fin
			result[0][elem]['shape'] = [max_x+17, max_y+17]
			result[0][elem]['pos'] = fin[0]
		return result
	return inner

@jsonify
@constructor
@iso_convert
def object_splitter(coords, tiles, dirname):
	data_dict = {}
	for coord in coords:
		x_group = []
		y_group = []
		z_group = []
		x_counter = 0
		y_counter = 0
		z_counter = 0
		for other_coord in coords:
			if coord[0] == other_coord[0]:
				x_group.append(other_coord)
				x_counter += 1
			if coord[1] == other_coord[1]:
				y_group.append(other_coord)
				y_counter += 1
			if coord[2] == other_coord[2]:
				z_group.append(other_coord)
				z_counter += 1

		if x_counter >= y_counter and x_counter >= z_counter:

			data_dict[coords.index(coord)] = {
				'coords': x_group,
				'tiles': tiles
			}

			for one in x_group:
				if one in coords:
					coords.remove(one)

		elif y_counter >= x_counter and y_counter >= z_counter:

			res_y = []

			for elem in y_group:
				same = []
				for one in y_group:
					if elem[1] == one[1] and elem[2] == other[2]:
						same.append(other)
				same = sorted(same, reverse=True)
				for y in same:
					res_y.append(y)
					if y in y_group:
						y_group.remove(y)

			data_dict[coords.index(coord)] = {
				'coords': res_y,
				'tiles': tiles
			}
			for elem in res_y:
				if elem in coords:
					coords.remove(elem)

		elif z_counter >= x_counter and z_counter >= y_counter:
			res_z = []
			print(z_group)
			for elem in z_group:
			    same = []
			    for other in z_group:
			        if elem[0] == other[0]:
			            same.append(other)
			    print(same)
			    for remover in same:
			        check = (remover in z_group)
			        if check:
			            del z_group[z_group.index(remover)]

			    res_z = list(chain(same, res_z))

			data_dict[coords.index(coord)] = {
				'coords': res_z,
				'tiles': tiles,
			}
			for used in res_z:
				if used in coords:
					del coords[coords.index(used)]

	return data_dict, dirname

def testfunc(coords, tiles, dirname):
	os.mkdir(dirname)
	tile = tiles
	canvas = Image.new('RGBA', (200, 200), (255, 0, 0, 0))
	img = Image.open(tile, 'r')
	img = img.convert('RGBA')
	for coord in coords:
		canvas.paste(img, coord, img)

	canvas.save(f'{dirname}\\one.png')