import pygame
import sys
from _thread import *

from data import data
from menu.button import Button
from network import Network


class MenuMain:
	def __init__(self, Main):
		self.main = Main
		self.exit_main_menu = False
		self.clock = pygame.time.Clock()
		self.end_loading_thread = False

		self.play_button = Button([True, [data.dissize[0] - 200, data.dissize[1] - 25]], 'button_border1', 'PLAY', (220, 220, 220), 16, 'play') # render_pos, border_name, text, text_colour, text_size
		self.join_lan_button = Button([True, [data.dissize[0] + 7, data.dissize[1] - 25]], 'button_border1', 'JOIN LAN', (220, 220, 220), 16, 'join_lan')
		self.quit_button = Button([True, [data.dissize[0] + 200, data.dissize[1] - 25]], 'button_border1', 'EXIT', (220, 220, 220), 16, 'exit')

		self.button_functions = {
			'play' 		: self.play,
			'join_lan'  : self.join_lan,
			'exit' 		: self.exit
		}

		#menu background stuff
		self.bg_tree_size = 72
		bg_tree = data.stitch_unpacked_image('maps', 'tree', (72, 72))
		density = 6
		self.bg_trees = [[bg_tree, i * (data.dissize[0] / density-2)] for i in range(density)]

		#name changing stuff
		self.changing_name = False
		self.name = ''
		self.typing_font = 'mainfont8'

	#button function calls
	def play(self, empty_args):
		self.main.host_server = True
		self.exit_main_menu = True

	def join_lan(self, empty_args):
		start_new_thread(self.finding_servers_loading_ani, ())
		self.main.network = Network(False)
		self.end_loading_thread = True
		if self.main.network.found_server:
			self.main.join_ip = self.main.network.ip_found
			self.main.network = None
			self.exit_main_menu = True
		else:
			self.main.network = None

	def exit(self, empty_args):
		pygame.quit()
		sys.exit()


	def finding_servers_loading_ani(self):
		searching_text = data.fonts['mainfont12'].render('Searching', False, (255, 255, 255))
		dots = ''
		timer = 0
		text_size = data.fonts['mainfont12'].size('Searching')
		while 1:
			self.main.display.fill((0, 0, 0))
			dt = self.clock.tick(data.fps_cap) * .001 * data.dt_fps

			searching_text = data.fonts['mainfont12'].render('Searching' + dots, False, (255, 255, 255))
			self.main.display.blit(searching_text, ((data.dissize[0] / 2) - (text_size[0] / 2), (data.dissize[1] / 2) - (text_size[1] / 2)))

			self.main.window.blit(
				pygame.transform.scale(self.main.display, data.winsize), (0, 0)
				)
			pygame.display.flip()

			timer += 1 * dt
			if timer >= 25:
				timer = 0
				dots += '.'
				if len(dots) >= 4:
					dots = ''

			if self.end_loading_thread:
				self.end_loading_thread = False
				break


	def render_text(self, text, pos, colour):
		surf = data.fonts[self.typing_font].render(text, False, colour)
		self.main.display.blit(surf, pos)


	def run(self):
		tmp_darken_surf = pygame.Surface(data.dissize).convert_alpha()
		pygame.draw.rect(tmp_darken_surf, (0, 0, 0), (0, 0, data.dissize[0], data.dissize[1]))
		tmp_darken_surf.set_alpha(125)

		while 1:
			if self.exit_main_menu:
				break

			self.main.display.fill((135, 206, 245))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.changing_name = not self.changing_name
						if not self.changing_name:
							self.name = ''

				if self.changing_name:
					if event.type == pygame.TEXTINPUT:
						if len(self.name) < 24 and not (' ' in event.text):
							self.name += event.text
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_BACKSPACE:
							self.name = self.name[:-1]
						if event.key == pygame.K_RETURN:
							if len(self.name) > 3:
								data.modify_json('json/player_data/user_specified_info.json', 'gamer_tag', self.name)
								self.changing_name = False
								data.reload()

			#background rendering
			for (tree_image, x_pos) in self.bg_trees:
				self.main.display.blit(tree_image, (
					x_pos, data.dissize[1] - self.bg_tree_size
					))

			mpos = pygame.mouse.get_pos()
			d_mpos = [mpos[0] / data.ratio, mpos[1] / data.ratio]
			self.play_button.process(d_mpos, self, ())
			self.quit_button.process(d_mpos, self, ())
			self.join_lan_button.process(d_mpos, self, ())

			try:
				self.play_button.render(self.main.display)
				self.join_lan_button.render(self.main.display)
				self.quit_button.render(self.main.display)
			except:
				pass

			#changing name (typing)
			if self.changing_name:
				self.main.display.blit(tmp_darken_surf, (0, 0))
				box_size = data.fonts[self.typing_font].size(self.name)
				pygame.draw.rect(self.main.display, (0, 0, 0), ((data.dissize[0] / 2) - (box_size[0] / 2), (data.dissize[1] / 2) - 4, box_size[0] + 8, box_size[1] + 4))	
				pygame.draw.rect(self.main.display, (200, 200, 200), ((data.dissize[0] / 2) - (box_size[0] / 2), (data.dissize[1] / 2) - 4, box_size[0] + 8, box_size[1] + 4), 2)	
				self.render_text(self.name, [(data.dissize[0] / 2) + 4 - (box_size[0] / 2), (data.dissize[1] / 2) - 2], (220, 220, 220))

			self.main.window.blit(
				pygame.transform.scale(self.main.display, data.winsize), (0, 0)
				)

			pygame.display.flip()