import pygame
from data import data
from menu.button import Button

class PausedScreen:
	def __init__(self, Main):
		self.main = Main

		self.resume_button = Button(['move_in', [-50, 50,  50, 50]], 'button_border1', 'Resume', (220, 220, 220), 10, 'resume') #render_pos, border_name, text, text_colour, text_size, name
		self.fullscreen_button = Button(['move_in', [-50, 75,  50, 75]], 'button_border1', 'Fullscreen', (220, 220, 220), 10, 'fullscreen')
		self.windowed_button = Button(['move_in', [-50, 75,  50, 75]], 'button_border1', 'Windowed', (220, 220, 220), 10, 'windowed')
		self.quit_button = Button(['move_in', [-50, 100,  50, 100]], 'button_border1', 'Quit', (220, 220, 220), 10, 'quit')

		self.button_functions = {
			'resume'	: self.resume,
			'fullscreen': self.fullscreen,
			'windowed'  : self.windowed,
			'quit'		: self.exit_out
		}

		self.darkened_bg = pygame.Surface(data.dissize).convert_alpha()
		self.darkened_bg.fill((0, 0, 0))
		self.darkened_bg.set_alpha(100)

	def resume(self, empty_args):
		self.main.paused_game = False

	def fullscreen(self, empty_args):
		data.in_fullscreen = True
		data.ratio = [data.mon_size[0] / data.dissize[0], data.mon_size[1] / data.dissize[1]]
		self.main.window = pygame.display.set_mode(data.mon_size, pygame.FULLSCREEN)

	def windowed(self, empty_args):
		data.in_fullscreen = False
		data.winsize = data.get_safe_windowsize()
		self.main.window = pygame.display.set_mode(data.winsize, pygame.RESIZABLE)

	def exit_out(self, empty_args):
		self.main.exit_game = True


	def reset(self):
		self.resume_button.reset()
		self.fullscreen_button.reset()
		self.quit_button.reset()

	def render(self):
		self.main.display.blit(self.darkened_bg, (0, 0))

		self.resume_button.process(data.d_mpos, self, ())
		if not data.in_fullscreen:
			self.fullscreen_button.process(data.d_mpos, self, ())
		else:
			self.windowed_button.process(data.d_mpos, self, ())
		self.quit_button.process(data.d_mpos, self, ())
		moved_in = self.resume_button.render(self.main.display, self.main.dt, self.main.move_pause_buttons_back)
		if not data.in_fullscreen:
			moved_in = self.fullscreen_button.render(self.main.display, self.main.dt, self.main.move_pause_buttons_back)
		else:
			moved_in = self.windowed_button.render(self.main.display, self.main.dt, self.main.move_pause_buttons_back)
		moved_in = self.quit_button.render(self.main.display, self.main.dt, self.main.move_pause_buttons_back)
		if moved_in == 'back_in':
			self.reset()
			self.main.move_pause_buttons_back = False
