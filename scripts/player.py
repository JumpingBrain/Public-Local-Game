import pygame
import sys

from data import data

class Player:
	def __init__(self, pos, id_tag):
		self.id_tag = id_tag
		self.rect = pygame.FRect(pos[0], pos[1], 7, 11)

		self.falling_speed = .2
		self.y_momentum = 0
		self.x_momentum = 0
		self.dir = 1
		self.mov_dir = 0
		self.curr_image_frame = 0
		self.mov_speed = 1.5
		self.movement = 'idle'
		self.hitground = False
		self.jump_cnt = 0

		#stats
		#HEALTH
		self.health = 100
		self.health_bar_length = 75
		self.regen_speed = .2
		#SHIELD
		self.shield = 100
		self.shield_bar_length = 25
		#LEVELING
		xp_data = data.retrieve_json('json/player_data/in_game_player_info.json', 'xp_data')
		self.level = xp_data[0]
		self.xp = xp_data[1]
		self.xp_bar_length = 14

		self.rect_buf = []
		self.buf_pos = None

		# load in the enemy
		if self.id_tag == '1':
			from enemy import Enemy # if you're hosting the server, import the enemy class
			self.enemy = Enemy()
		else:
			self.enemy = None

		#actions (like a fighting move) that the player can do
		self.dash = False
		self.dash_cnt = 0
		self.dash_time_length = .1
		self.dash_finished = False #this is for the slowing down portion
		self.dash_cooldown = False
		self.dash_cooldown_timer = 0
		self.dash_cooldown_length = .75

	@property
	def pos(self):
		return [self.rect.x, self.rect.y]

	def xp_needed(self):
		if self.level < 10:
			return (self.level + 1) * 4
		elif self.level > 9 and self.level < 20:
			return (self.level + 1) * 2
		elif self.level > 19 and self.level < 30:
			return (self.level + 1) * 1.5
		else:
			return (self.level + 1) * 1.75

	def render_stats(self, display):
		#HEALTH
		width = self.health_bar_length * (self.health / 100)
		x_pos = data.dissize[0] - width
		padding = 2
		pygame.draw.rect(display, (196, 68, 74), (x_pos - padding, padding, width, 7))
		display.blit(data.images['ui']['healthbar_border'][0], (x_pos - padding - 1, padding - 1))

		#SHIEDL
		width = self.shield_bar_length * (self.shield / 100)
		x_pos = data.dissize[0] - width
		padding = 9 + 3
		pygame.draw.rect(display, (97, 186, 255), (x_pos - 2, padding, width, 4))
		display.blit(data.images['ui']['shieldbar_border'][0], (x_pos - 2 - 1, padding - 1))

		#LEVEL
		display.blit(data.images['ui']['level_border'][0], (2, 2))
		font = data.fonts['mainfont' + '16']
		level_surf = font.render(str(int(self.level)), False, (255, 255, 235))
		if self.level > 10: display.blit(level_surf, (3, 3))
		else: display.blit(level_surf, (3 + 4, 3))
		#####################-XP
		xp_needed = self.xp_needed()
		width = self.xp_bar_length * (self.xp / xp_needed)
		x_pos = 4
		padding = 2
		pygame.draw.rect(display, (118, 255, 112), (x_pos, 22, width, 4))
		display.blit(data.images['ui']['xpbar_border'][0], (x_pos - 1, 22 - 1))
		########-resetting xp and leveling up is done here
		if self.xp >= xp_needed:
			self.level += 1 
			self.xp = 0

		#gamer tag stuff
		self.gamer_tag = data.gamer_tag_str

	def render(self, display, int_camera):
		#render gamer tag
		gamer_tag_surf = data.fonts['mainfont8'].render(self.gamer_tag, False, (255, 255, 255))
		display.blit(gamer_tag_surf, (self.rect.centerx - (data.p_gamer_tag_size[0] / 2) - int_camera[0], self.rect.y - data.p_gamer_tag_size[1] - 2 - int_camera[1]))
		#render actual player
		if self.curr_image_frame >= len(data.p_images[f'{self.movement + self.id_tag} {self.dir}']):
			self.curr_image_frame = 0
			self.hitground = False
		display.blit(data.p_images[f'{self.movement + self.id_tag} {self.dir}'][int(self.curr_image_frame)], (self.rect.x - int_camera[0], self.rect.y - int_camera[1]))

	def collisions(self, rect_list):
		hits = []
		for d in rect_list:
			rect = d[0]
			if rect.colliderect(self.rect):
				hits.append(d)
		return hits

	def reset_ani(self, new_ani):
		if new_ani != self.movement:
			self.curr_image_frame = 0

	def do_dash(self, dt):
		if self.dash:
			dash_speed = 8 * self.dir * dt
			self.x_momentum += dash_speed
			self.dash_cnt += 1 * dt
			if self.dash_cnt >= data.dt_fps * self.dash_time_length:
				self.dash = False
				self.dash_cnt = 0
				self.dash_finished = True
				self.dash_cooldown = True

		if self.dash_cooldown:
			self.dash_cooldown_timer += 1 * dt
			if self.dash_cooldown_timer >= data.dt_fps * self.dash_cooldown_length:
				self.dash_cooldown_timer = 0
				self.dash_cooldown = False

	def actions(self, key_presses, dt):
		if key_presses['rmb']:
			if not self.dash_cooldown:
				self.dash = True
		self.do_dash(dt)

	def update(self, dt, map_rects, ignore_input):
		#return player to where he was before the window was being resized
		if self.buf_pos != None:
			self.rect.x = self.buf_pos[0]
			self.rect.y = self.buf_pos[1]
		self.xp += 0.1 * dt
		keys = pygame.key.get_pressed()

		self.mov_dir = keys[pygame.K_d] - keys[pygame.K_a]
		if self.mov_dir != 0:
			if self.buf_pos != None:
				self.buf_pos = None
		if ignore_input:
			self.mov_dir = 0
		if self.mov_dir != 0:
			self.dir = self.mov_dir
			if not self.hitground:
				self.reset_ani('running')
			self.movement = 'running'
		else:
			if not self.hitground:
				self.reset_ani('idle')
			self.movement = 'idle'

		if self.jump_cnt > 0:
			self.movement = 'jumping'

		if self.hitground:
			self.movement = 'hitground'


		#do animation counting
		if self.movement == 'running':
			self.curr_image_frame += data.running_ani_speed * dt
		elif self.movement == 'idle':
			self.curr_image_frame += data.idle_ani_speed * dt
		elif self.movement == 'hitground':
			#print(self.curr_image_frame)
			if self.mov_dir == 0: self.curr_image_frame += data.hitground_ani_speed * dt
			else: self.curr_image_frame += data.hitground_ani_speed * 2 * dt

		if self.mov_dir == 1:
			dir = 'right'
		elif self.mov_dir == -1:
			dir = 'left'

		if self.mov_dir != 0:
			if not self.dash:
				if dir == 'right':
					if not self.x_momentum >= self.mov_speed:
						self.x_momentum += self.mov_dir * (self.mov_speed * .75) * dt
						if not self.dash:
							self.dash_finished = False
				else:
					if not self.x_momentum <= -self.mov_speed:
						self.x_momentum += self.mov_dir * (self.mov_speed * .75) * dt
						if not self.dash:
							self.dash_finished = False
		if self.x_momentum != 0:
			if not self.dash_finished:
				deceleration = .75
			else:
				deceleration = .5
			diff = (self.x_momentum * -1) * deceleration
			self.x_momentum += diff * dt
			if abs(self.x_momentum) < .2 and self.mov_dir == 0:
				self.x_momentum = 0
				self.dash_finished = False

		self.rect.x += self.x_momentum * dt
		hits = self.collisions(map_rects)
		#this is for the occasion when the user resizes the window
		#use_buf = False
		#if len(hits) > 0:
		#	self.rect_buf = hits
		#else:
		#	use_buf = True
		#if use_buf:
		#	hits = self.rect_buf
		for d in hits:
			rect = d[0]
			if self.x_momentum > 0:
				self.rect.right = rect.left
				self.x_momentum = 0
			elif self.x_momentum < 0:
				self.rect.left = rect.right
				self.x_momentum = 0

		self.y_momentum += self.falling_speed * dt
		if self.y_momentum >= 6:
			self.y_momentum = 6

		self.rect.y += self.y_momentum * dt
		hits = self.collisions(map_rects)
		#this is for the occasion when the user resizes the window
		#use_buf = False
		#if len(hits) > 0:
		#	self.rect_buf = hits
		#else:
		#	use_buf = True
		#if use_buf:
		#	hits = self.rect_buf
		#print(iters)
		for d in hits:
			rect = d[0]
			if self.y_momentum > 0:
				if self.y_momentum > 1:
					self.reset_ani('hitground')
					self.hitground = True
				self.rect.bottom = rect.top
				self.y_momentum = 0
				self.jump_cnt = 0
			elif self.y_momentum < 0:
				self.rect.top = rect.bottom
				self.y_momentum = 0

	def run_enemy(self, surf, dt, int_camera, p1):
		if self.id_tag == '1':
			self.enemy.move(dt)
		p1.enemy.render(surf, int_camera)