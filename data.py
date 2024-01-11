import pygame
import os
import json


class Data:
	def __init__(self):
		self.imagedir = 'images/'
		self.jsondir = 'json/'

		self.images = {}
		for foldername in os.listdir(self.imagedir):
			curr_dir = self.imagedir + foldername + '/'
			self.images[foldername] = {}
			for filename in os.listdir(curr_dir):
				unpack_size, dis = self.get_unpack_size(filename)
				self.images[foldername][filename[:-dis]] = self.unpack(
					pygame.image.load(curr_dir + filename), unpack_size)

		self.p_images = {}
		for key in self.images['player']:
			images = self.images['player'][key]
			self.p_images[f'{key} 1'] = [image for image in images] #right (1)
			self.p_images[f'{key} -1'] = [pygame.transform.flip(image, True, False) for image in images] #left (-1)

		self.running_ani_speed = .25
		self.idle_ani_speed = .25
		self.hitground_ani_speed = .2

		self.ui_dat = json.load(open('non_ingame_data.json'))

		self.raw_map_data = {key[:-5]:json.load(open(self.jsondir + 'maps/' + key)) for key in os.listdir(self.jsondir + 'maps/')}
		self.render_dis = 400

	def get_unpack_size(self, image_name):
			dis = 0
			extracted = ''
			extract = False
			for id, char in enumerate(image_name):
				if char == '.': break
				if extract: extracted += char
				if char == '!': 
					extract = True
					dis = len(image_name) - id
			size = ["", ""]
			id = 0
			for char in extracted:
				if char == 'x': id += 1
				else: size[id] += char
			size = [int(i) for i in size]

			return size, dis


	def unpack(self, tilemap, tilesize):
		width, height = tilesize[0], tilesize[1]
		x, y = 0, 0
		surf_x, surf_y = 0, 0
		images = []

		for _ in range(int(tilemap.get_width() / width) * int(tilemap.get_height() / height)):
			images.append((pygame.Surface((width, height))))
			curr_surf = images[len(images)-1]
			for surf_y in range(height):
				for surf_x in range(width):
					pygame.draw.rect(curr_surf, tilemap.get_at((x + surf_x, y + surf_y)), (surf_x, surf_y, 1, 1))
			images[len(images)-1].set_colorkey((0, 0, 0, 0))

			x += width
			if x >= tilemap.get_width():
				x = 0
				y += height

		return images

data = Data()