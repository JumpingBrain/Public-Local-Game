import pygame


class SavedIcon:
	def __init__(self, dissize, images):
		self.images = images
		self.frame = 0
		self.ani_speed = .15
		self.dissize = dissize
		self.timer = 0

	def render(self, surf, darkened_bg, dt, dt_fps):
		image = self.images[int(self.frame)]
		surf.blit(darkened_bg, (0, self.dissize[1] - image.get_height() - 4))
		surf.blit(image, (2, self.dissize[1] - image.get_height() - 2))

		self.frame += self.ani_speed * dt

		if self.frame >= len(self.images):
			self.timer += 1 * dt
			if self.timer >= dt_fps / 1.8:
				self.timer = 0
				return True
			self.frame -= self.ani_speed * dt

		return False

	def reset(self):
		self.frame = 0