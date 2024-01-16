import pygame
import sys
from pygame.locals import *
from math import floor
from _thread import *

from data import data
from network import Network
from map import Map
from menu.menu_main import MenuMain
from paused_screen import PausedScreen

pygame.init()

from sounds import sfx

mon_info = pygame.display.Info()
data.mon_siz = [mon_info.current_w, mon_info.current_h]


class Main:
	def __init__(self):
		self.window = pygame.display.set_mode(data.winsize, RESIZABLE)
		self.display = pygame.Surface(data.dissize)

		#run menu
		self.network = None
		self.host_server = False
		self.join_ip = None
		self.mainmenu = MenuMain(self)
		self.mainmenu.run()

		if self.host_server:
			try: import server #attempt to host the server
			except: pass
			self.network = Network(True)
		else:
			self.network = Network(True, server=self.join_ip)

		self.paused_screen = PausedScreen(self)
		self.paused_game = False
		self.move_pause_buttons_back = False

		self.exit_game = False

		#send player gamer tag to server
		#self.network.str_send(data.gamer_tag_str)

		self.clock = pygame.time.Clock()
		self.dt = 1
		self.ticks = 0
		self.timer = 0

		self.map = Map(self)

		self.camera = [0, 0]
		self.int_camera = self.camera.copy()

		self.ignore_input = False

		self.resized = False

		#these must be initiated here as the pygame.display must be initialised first
		#these are simply just for the transparent background behind the autosave icon
		saved_icon_base_image = data.images['ui']['saved_icon'][0]
		self.darkened_bg = pygame.Surface((saved_icon_base_image.get_width() + 4, saved_icon_base_image.get_height() + 4)).convert_alpha()
		self.darkened_bg.fill((0, 0, 0))
		self.darkened_bg.set_alpha(75)

	def process(self, p1, p2, p3):
		self.dt = self.clock.tick(data.fps_cap) * .001 * data.dt_fps
		self.ticks += 1
		self.timer += 1 * self.dt

		self.camera[0] += (((p1.rect.centerx - self.camera[0]) - (data.dissize[0] / 2)) / 20) * self.dt
		self.camera[1] += (((p1.rect.centery - self.camera[1]) - (data.dissize[1] / 2)) / 20) * self.dt
		self.int_camera[0] = floor(self.camera[0])

		self.int_camera[1] = floor(self.camera[1])

		mouse_pressed = pygame.mouse.get_pressed()[0]
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if not self.ignore_input:
						if p1.jump_cnt < 2:
							sfx.sounds['jump'].reset()
							sfx.sounds['jump'].play(
								self.dt, self.ticks, 2
								)
							p1.y_momentum = -4
							p1.jump_cnt += 1
							p1.movement = 'jumping'
				elif event.key == K_ESCAPE:
					self.paused_game = not self.paused_game
			if event.type == WINDOWRESIZED:
				self.resized = True
				#the buffer is just so that the player returns back to where he was
				#because when you resize the screen, his physics keep running
				#for some reason idk man haha
				p1.buf_pos = p1.pos
				#the window just got resized so change window into better ratio for viewing
				new_size = self.window.get_size()
				new_width = new_size[0] - (new_size[0] % 16)
				new_height = 9 * (new_width / 16)
				if new_size[0] == data.mon_size[0]:
					self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
					data.in_fullscreen = True
				else:
					self.window = pygame.display.set_mode((new_width, new_height), RESIZABLE)
				data.winsize = (new_width, new_height)
				data.ratio = [new_width / data.dissize[0], new_height / data.dissize[1]]
				self.resized = False


		if self.timer >= data.dt_fps:
			self.timer = 0
			#print(self.ticks)
			print('FPS:', self.ticks)
			self.ticks = 0

	def rendering(self, p1, p2, p3):
		self.display.fill((135, 206, 245))
		self.map.render(p1.pos)

		p1.update(self.dt, self.map.map_rects, self.ignore_input, self)

		p1.render(self.display, self.int_camera)

		try: 
			p2.render(self.display, self.int_camera)
			p3.render(self.display, self.int_camera)
		except: pass

		p1.render_stats(self.display)

		if self.paused_game:
			self.ignore_input = True
			self.paused_screen.render()
		else:
			if self.ignore_input:
				self.move_pause_buttons_back = True
			self.ignore_input = False
			if self.move_pause_buttons_back:
				self.paused_screen.render()
				#print('moving')


		#the autosave icon is done here to insure that it renders above everything
		data.save_timer += 1 * self.dt
		if data.save_timer >= data.dt_fps * (data.save_freq * 60): #2 minutes in seconds
			#data.save_timer = 0
			data.save_current_player_data(p1)
			end = data.saved_icon.render(self.display, self.darkened_bg, self.dt, data.dt_fps)
			print('saving...')
			if end:
				data.save_timer = data.save_timer - data.dt_fps * (data.save_freq * 60)
				data.saved_icon.reset()


	def run(self):
		p1 = self.network.get_p()
		p1.gamer_tag = data.gamer_tag_str
		while 1:
			if not self.exit_game:
				players = self.network.send(p1)
				p2, p3 = players[0], players[1]

				self.process(p1, p2, p3)

				self.rendering(p1, p2, p3)

				self.window.blit(
						pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
				pygame.display.flip()
			else:
				self.display.fill((0, 0, 0))
				self.dt = self.clock.tick(data.fps_cap) * .001 * data.dt_fps

				data.save_current_player_data(p1)
				end = data.saved_icon.render(self.display, self.darkened_bg, self.dt, data.dt_fps)

				self.window.blit(
						pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
				pygame.display.flip()

				if end:
					break




main = Main()
main.run()