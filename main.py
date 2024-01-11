import pygame
import sys
from pygame.locals import *
from math import floor

from data import data
from network import Network
from map import Map



class Main:
	def __init__(self):
		self.window = pygame.display.set_mode(data.ui_dat['winsize'])
		self.display = pygame.Surface(data.ui_dat['dissize'])

		self.clock = pygame.time.Clock()
		self.dt = 1


		self.map = Map(self)

		self.camera = [0, 0]
		self.int_camera = self.camera.copy()


	def run(self):
		n = Network()
		p1 = n.get_p()
		while 1:
			self.display.fill((135, 206, 245))
			self.map.render(p1.pos)
			self.dt = self.clock.tick(data.ui_dat['fps_cap']) * .001 * 60
			print(self.dt)

			p2 = n.send(p1)

			self.camera[0] += (((p1.rect.centerx - self.camera[0]) - (data.ui_dat['dissize'][0] / 2)) / 20) * self.dt
			self.camera[1] += (((p1.rect.centery - self.camera[1]) - (data.ui_dat['dissize'][1] / 2)) / 20) * self.dt
			self.int_camera[0] = floor(self.camera[0])
			self.int_camera[1] = floor(self.camera[1])

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_SPACE:
						if p1.jump_cnt < 2:
							p1.y_momentum = -4
							p1.jump_cnt += 1
							p1.movement = 'jumping'

			p1.update(self.dt, self.map.map_rects)
			p1.render(self.display, self.int_camera)

			#p2.update(self.dt)
			p2.render(self.display, self.int_camera)


			self.window.blit(
				pygame.transform.scale(self.display, data.ui_dat['winsize']), (0, 0))
			pygame.display.flip()


main = Main()
main.run()