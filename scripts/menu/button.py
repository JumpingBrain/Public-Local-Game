import pygame

from data import data

pygame.font.init()


class Button:
	def __init__(self, render_pos, border_name, text, text_colour, text_size, name):
		self.name = name

		self.text_size = text_size
		font = pygame.font.Font(data.fontdir + 'mainfont.otf', self.text_size)
		self.button_text = font.render(text, False, text_colour)

		if render_pos[0] == True:
			f_size = font.size(text)
			self.pos = [(render_pos[1][0] / 2) - (f_size[0] / 2), 
						(render_pos[1][1] / 2) - (f_size[1] / 2)]
		else:
			self.pos = render_pos

		text_surf_size = font.size(text)
		self.padding = 6
		self.border_img = pygame.transform.scale(data.images['menu'][border_name][0], (text_surf_size[0] + self.padding, text_surf_size[1] + self.padding))
		self.hitbox_area = self.border_img.get_size()

		self.button_surf = pygame.Surface(self.hitbox_area)
		self.button_surf.blit(self.border_img, (0, 0))
		self.button_surf.blit(self.button_text, (self.padding / 2, self.padding / 2))
		self.button_surf.set_colorkey((0, 0, 0, 0))

		self.downsize = .75
		self.clicked_button_surf = pygame.Surface((self.hitbox_area[0] * self.downsize, self.hitbox_area[1] * self.downsize))
		tmp_size = self.border_img.get_size()
		self.clicked_button_surf.blit(pygame.transform.scale(self.border_img, (tmp_size[0] * self.downsize, tmp_size[1] * self.downsize)), (0, 0))
		self.clicked_button_surf.set_colorkey((0, 0, 0, 0))
		tmp_size = self.button_text.get_size()
		self.clicked_button_surf.blit(pygame.transform.scale(self.button_text, (tmp_size[0] * self.downsize, tmp_size[1] * self.downsize)), ((self.padding / 2) * self.downsize, (self.padding / 2) * self.downsize))

		self.clicked = False

	def render(self, surf):
		if not self.clicked:
			surf.blit(self.button_surf, (self.pos[0] - (self.padding / 2), self.pos[1] - (self.padding / 2)))
		else:
			change = (1 - self.downsize) / 2
			surf.blit(self.clicked_button_surf, (self.pos[0] - (self.padding / 2) + (self.hitbox_area[0] * change), self.pos[1] - (self.padding / 2) + (self.hitbox_area[1] * change)))

	def process(self, mpos, classs, args):
		mposx_diff = mpos[0] - self.pos[0]
		mposy_diff = mpos[1] - self.pos[1]

		if pygame.mouse.get_pressed()[0]:
			if self.pos[0] <= self.pos[0] + mposx_diff and self.pos[0] + self.hitbox_area[0] > self.pos[0] + mposx_diff and self.pos[1] < self.pos[1] + mposy_diff and self.pos[1] + self.hitbox_area[1] > self.pos[1] + mposy_diff:
				self.clicked = True
			else:
				self.clicked = False
				#classs.button_functions[self.name](args)
		else:
			if self.clicked:
				classs.button_functions[self.name](args)
			self.clicked = False