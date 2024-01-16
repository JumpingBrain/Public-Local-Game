import pygame

from data import data

pygame.font.init()


class Button:
	def __init__(self, render_pos, border_name, text, text_colour, text_size, name):
		self.name = name

		self.text_size = text_size
		font = pygame.font.Font(data.fontdir + 'mainfont.otf', self.text_size)
		self.button_text = font.render(text, False, text_colour)
		self.move = False

		self.render_pos = render_pos
		if render_pos[0] == True:
			f_size = font.size(text)
			self.pos = [(render_pos[1][0] / 2) - (f_size[0] / 2), 
						(render_pos[1][1] / 2) - (f_size[1] / 2)]
		elif render_pos[0] == 'move_in':
			self.pos = [
						render_pos[1][0], render_pos[1][1], 
						render_pos[1][2], render_pos[1][3]] #these values are just where the x and y positions are moving to
			self.move = True
			self.move_speed = 2
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

		self.upsize = 1.25
		self.hovered_button_surf = pygame.Surface((self.hitbox_area[0] * self.upsize, self.hitbox_area[1] * self.upsize))
		tmp_size = self.border_img.get_size()
		self.hovered_button_surf.blit(pygame.transform.scale(self.border_img, (tmp_size[0] * self.upsize, tmp_size[1] * self.upsize)), (0, 0))
		self.hovered_button_surf.set_colorkey((0, 0, 0, 0))
		tmp_size = self.button_text.get_size()
		self.hovered_button_surf.blit(pygame.transform.scale(self.button_text, (tmp_size[0] * self.upsize, tmp_size[1] * self.upsize)), ((self.padding / 2) * self.upsize, (self.padding / 2) * self.upsize))

		self.hovered = False

		self.clicked = False

	def reset(self):
		if self.render_pos[0] == 'move_in':
			self.pos = [
						self.render_pos[1][0], self.render_pos[1][1], 
						self.render_pos[1][2], self.render_pos[1][3]] #these values are just where the x and y positions are moving to
			self.move = True
			self.move_speed = 2

	def render(self, surf, dt=None, go_back=None):
		if self.move:
			x_finished = False
			y_finished = False
			if not go_back:
				if abs(self.pos[0] - self.pos[2]) > self.move_speed * 2:
					self.pos[0] += ((self.pos[2] - self.pos[0]) - ((self.pos[2] - self.pos[0]) * .85)) * self.move_speed * dt
				if abs(self.pos[1] - self.pos[3]) > self.move_speed * 2:
					self.pos[1] += ((self.pos[3] - self.pos[1]) - ((self.pos[3] - self.pos[1]) * .85)) * self.move_speed * dt
			else:
				if not x_finished:
					self.pos[0] += (((self.pos[2] - self.render_pos[1][0]) - ((self.pos[2] - self.render_pos[1][0]) * .85)) * (self.move_speed * .5)) * -1 * dt
				if not y_finished:
					self.pos[1] += (((self.pos[3] - self.render_pos[1][1]) - ((self.pos[3] - self.render_pos[1][1]) * .85)) * (self.move_speed * .5)) * -1 * dt
				if abs(self.pos[0] - self.render_pos[1][0]) < self.move_speed:
					x_finished = True
				if abs(self.pos[1] - self.render_pos[1][1]) < self.move_speed:
					y_finished = True
				if x_finished and y_finished:
					return 'back_in'
		if self.clicked:
			change = (1 - self.downsize) / 2
			surf.blit(self.clicked_button_surf, (self.pos[0] - (self.padding / 2) + (self.hitbox_area[0] * change), self.pos[1] - (self.padding / 2) + (self.hitbox_area[1] * change)))
		elif self.hovered:
			change = (1 - self.upsize) / 2
			surf.blit(self.hovered_button_surf, (self.pos[0] - (self.padding / 2) + (self.hitbox_area[0] * change), self.pos[1] - (self.padding / 2) + (self.hitbox_area[1] * change)))
		else:
			surf.blit(self.button_surf, (self.pos[0] - (self.padding / 2), self.pos[1] - (self.padding / 2)))

	def process(self, mpos, classs, args):
		mposx_diff = mpos[0] - self.pos[0]
		mposy_diff = mpos[1] - self.pos[1]

		if self.pos[0] <= self.pos[0] + mposx_diff and self.pos[0] + self.hitbox_area[0] > self.pos[0] + mposx_diff and self.pos[1] < self.pos[1] + mposy_diff and self.pos[1] + self.hitbox_area[1] > self.pos[1] + mposy_diff:
			self.hovered = True
			if pygame.mouse.get_pressed()[0]:
				self.clicked = True
			else:
				if self.clicked:
					classs.button_functions[self.name](args)
				self.clicked = False
		else:
			self.hovered = False
			self.clicked = False

		#if pygame.mouse.get_pressed()[0]:
		#	if self.pos[0] <= self.pos[0] + mposx_diff and self.pos[0] + self.hitbox_area[0] > self.pos[0] + mposx_diff and self.pos[1] < self.pos[1] + mposy_diff and self.pos[1] + self.hitbox_area[1] > self.pos[1] + mposy_diff:
		#		self.clicked = True
		#	else:
		#		self.clicked = False
		#		#classs.button_functions[self.name](args)
		#else:
		#	if self.clicked:
		#		classs.button_functions[self.name](args)
		#	self.clicked = False