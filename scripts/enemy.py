import pygame


class Enemy:
	def __init__(self):
		self.pos = [80, 50]

	def move(self, dt):
		#self.pos[0] += .1 * dt
		pass

	def render(self, surf, int_camera):
		pygame.draw.rect(surf, (0, 0, 0), (self.pos[0] - int_camera[0], self.pos[1] - int_camera[1], 20, 20))