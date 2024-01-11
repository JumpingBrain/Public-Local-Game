import pygame
import sys
from pygame.locals import *
from math import floor
from _thread import *
try:
	import server #attempt to host the server
except:
	pass

from data import data
from network import Network
from map import Map

pygame.init()

from sounds import sfx

mon_info = pygame.display.Info()
data.mon_siz = [mon_info.current_w, mon_info.current_h]


class Main:
	def __init__(self):
		self.window = pygame.display.set_mode(data.winsize)
		self.display = pygame.Surface(data.dissize)

		self.clock = pygame.time.Clock()
		self.dt = 1
		self.ticks = 0
		self.timer = 0

		self.map = Map(self)

		self.camera = [0, 0]
		self.int_camera = self.camera.copy()

	def process(self, p1, p2):
		self.dt = self.clock.tick(data.ui_dat['fps_cap']) * .001 * data.dt_fps
		self.ticks += 1
		self.timer += 1 * self.dt

		self.camera[0] += (((p1.rect.centerx - self.camera[0]) - (data.dissize[0] / 2)) / 20) * self.dt
		self.camera[1] += (((p1.rect.centery - self.camera[1]) - (data.dissize[1] / 2)) / 20) * self.dt
		self.int_camera[0] = floor(self.camera[0])
		self.int_camera[1] = floor(self.camera[1])

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if p1.jump_cnt < 2:
						sfx.sounds['jump'].reset()
						sfx.sounds['jump'].play(
							self.dt, self.ticks, 2
							)
						p1.y_momentum = -4
						p1.jump_cnt += 1
						p1.movement = 'jumping'

		p1.update(self.dt, self.map.map_rects)

	def rendering(self, p1, p2):
		self.display.fill((135, 206, 245))
		self.map.render(p1.pos)

		p1.render(self.display, self.int_camera)

		p2.render(self.display, self.int_camera)

		p1.render_stats(self.display)

		self.window.blit(
				pygame.transform.scale(self.display, data.ui_dat['winsize']), (0, 0))
		pygame.display.flip()


	def run(self):
		n = Network()
		p1 = n.get_p()
		while 1:
			p2 = n.send(p1)

			self.process(p1, p2)

			self.rendering(p1, p2)




main = Main()
main.run()