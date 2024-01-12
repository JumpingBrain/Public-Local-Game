import pygame
import os
import json

from pathlib import Path
path = Path(os.getcwd())
PARDIR = str(path.parent.absolute())

pygame.font.init()


class Data:
	def __init__(self):
		self.mon_size = None

		self.jsondir = PARDIR + '/json/'
		self.imagedir = PARDIR + '/images/'
		self.fontdir = PARDIR + '/fonts/'
		self.sounddir = PARDIR + '/sounds/'

		self.images = {}
		for foldername in os.listdir(self.imagedir):
			curr_dir = self.imagedir + foldername + '/'
			self.images[foldername] = {}
			for filename in os.listdir(curr_dir):
				unpack_size, dis = self.get_unpack_size(filename)
				self.images[foldername][filename[:-dis]] = self.unpack(
					pygame.image.load(curr_dir + filename), unpack_size)

		#all surfaces must be saved here
		#server cannot transfer surfaces
		#so all surfaces must be saved on
		#each client machine

		self.p_images = {}
		for key in self.images['player']:
			images = self.images['player'][key]
			self.p_images[f'{key} 1'] = [image for image in images] #right (1)
			self.p_images[f'{key} -1'] = [pygame.transform.flip(image, True, False) for image in images] #left (-1)
		self.running_ani_speed = .25
		self.idle_ani_speed = .25
		self.hitground_ani_speed = .2
		self.render_dis = 400

		#do the same with fonts as they're a surface
		#(read above comments if unsure what i mean)
		self.fonts = {}
		f_base = 6
		f_size = f_base
		for font_name in os.listdir(self.fontdir):
			for i in range(6):
				font = pygame.font.Font(self.fontdir + font_name, f_size)
				self.fonts[font_name[:-4] + str(f_size)] = font
				f_size += 2
			f_size = f_base

		#loading more player surfaces here rather than in player class (cus of server stuff yaknow)
		self.gamer_tag_str = self.retrieve_json('json/player_data/user_specified_info.json', 'gamer_tag')
		self.p_gamer_tag = self.fonts['mainfont8'].render(
			self.gamer_tag_str, False, (255, 255, 255))
		self.p_gamer_tag_size = self.fonts['mainfont8'].size(self.gamer_tag_str)


		self.ui_dat = json.load(open(self.jsondir + 'non_ingame_data.json'))
		self.winsize = self.ui_dat['winsize']
		self.dissize = self.ui_dat['dissize']
		self.ratio = self.winsize[0] / self.dissize[0]
		self.dt_fps = 60
		self.fps_cap = self.ui_dat['fps_cap']

		self.raw_map_data = {key[:-5]:json.load(open(self.jsondir + 'maps/' + key)) for key in os.listdir(self.jsondir + 'maps/')}

	def reload(self):
		self.jsondir = PARDIR + '/json/'
		self.imagedir = PARDIR + '/images/'
		self.fontdir = PARDIR + '/fonts/'
		self.sounddir = PARDIR + '/sounds/'

		self.images = {}
		for foldername in os.listdir(self.imagedir):
			curr_dir = self.imagedir + foldername + '/'
			self.images[foldername] = {}
			for filename in os.listdir(curr_dir):
				unpack_size, dis = self.get_unpack_size(filename)
				self.images[foldername][filename[:-dis]] = self.unpack(
					pygame.image.load(curr_dir + filename), unpack_size)

		#all surfaces must be saved here
		#server cannot transfer surfaces
		#so all surfaces must be saved on
		#each client machine

		self.p_images = {}
		for key in self.images['player']:
			images = self.images['player'][key]
			self.p_images[f'{key} 1'] = [image for image in images] #right (1)
			self.p_images[f'{key} -1'] = [pygame.transform.flip(image, True, False) for image in images] #left (-1)
		self.running_ani_speed = .25
		self.idle_ani_speed = .25
		self.hitground_ani_speed = .2
		self.render_dis = 400

		#do the same with fonts as they're a surface
		#(read above comments if unsure what i mean)
		self.fonts = {}
		f_base = 6
		f_size = f_base
		for font_name in os.listdir(self.fontdir):
			for i in range(6):
				font = pygame.font.Font(self.fontdir + font_name, f_size)
				self.fonts[font_name[:-4] + str(f_size)] = font
				f_size += 2
			f_size = f_base

		#loading more player surfaces here rather than in player class (cus of server stuff yaknow)
		self.gamer_tag_str = self.retrieve_json('json/player_data/user_specified_info.json', 'gamer_tag')
		self.p_gamer_tag = self.fonts['mainfont8'].render(
			self.gamer_tag_str, False, (255, 255, 255))
		self.p_gamer_tag_size = self.fonts['mainfont8'].size(self.gamer_tag_str)


		self.ui_dat = json.load(open(self.jsondir + 'non_ingame_data.json'))
		self.winsize = self.ui_dat['winsize']
		self.dissize = self.ui_dat['dissize']
		self.ratio = self.winsize[0] / self.dissize[0]
		self.dt_fps = 60
		self.fps_cap = self.ui_dat['fps_cap']

		self.raw_map_data = {key[:-5]:json.load(open(self.jsondir + 'maps/' + key)) for key in os.listdir(self.jsondir + 'maps/')}

	def retrieve_json(self, json_dir, key):
		json_dir = PARDIR + '/' + json_dir
		data = json.load(open(json_dir))
		return data[key]

	def modify_json(self, json_dir, key, new_data):
		json_dir = PARDIR + '/' + json_dir
		data = json.load(open(json_dir))
		data[key] = new_data
		with open(json_dir, 'w') as file:
			file.write(json.dumps(data))
			file.close()

	def stitch_unpacked_image(self, pre_id, image_name, image_size):
		x, y, n = 0, 0, 0
		stitched_image = pygame.Surface(image_size).convert()
		stitched_image.set_colorkey((0, 0, 0, 0))
		for image in self.images[pre_id][image_name]:
			stitched_image.blit(image, (x, y))
			x += image.get_width()
			if x >= image_size[0]:
				x = 0
				y += image.get_height()


		return stitched_image

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