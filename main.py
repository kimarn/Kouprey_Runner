from pyclbr import Class

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('Assets/pics/kouprey/kouprey1.png').convert_alpha()
		player_walk_2 = pygame.image.load('Assets/pics/kouprey/kouprey2.png').convert_alpha()
		player_walk_3 = pygame.image.load('Assets/pics/kouprey/kouprey3.png').convert_alpha()

		player_walk_1,player_walk_2,player_walk_3 = pygame.transform.rotozoom(player_walk_1,0,2.5),pygame.transform.rotozoom(player_walk_2,0,2.5),pygame.transform.rotozoom(player_walk_3,0,2.5)

		self.player_walk = [player_walk_1,player_walk_2,player_walk_3]
		self.player_index = 0
		self.player_jump = pygame.image.load('Assets/pics/kouprey/kouprey1.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,500))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('Assets/sounds/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
			self.gravity = -25
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 500:
			self.rect.bottom = 500

	def animation_state(self):
		if self.rect.bottom < 500: 
			self.image = self.player_walk[0]
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,obstacle_type):
		super().__init__()
		
		if obstacle_type == 'bird':
			bird_1 = pygame.image.load('Assets/pics/bird/bird1.png').convert_alpha()
			bird_2 = pygame.image.load('Assets/pics/bird/bird2.png').convert_alpha()
			bird_3 = pygame.image.load('Assets/pics/bird/bird3.png').convert_alpha()

			bird_1,bird_2,bird_3 = pygame.transform.rotozoom(bird_1,0,2.3),pygame.transform.rotozoom(bird_2,0,2.3),pygame.transform.rotozoom(bird_3,0,2.3)

			self.frames = [bird_1,bird_2,bird_3]
			y_pos = 380
		else:
			chicken_1 = pygame.image.load('Assets/pics/chicken/chicken1.png').convert_alpha()
			chicken_2 = pygame.image.load('Assets/pics/chicken/chicken2.png').convert_alpha()
			chicken_3 = pygame.image.load('Assets/pics/chicken/chicken3.png').convert_alpha()

			chicken_1,chicken_2,chicken_3 = pygame.transform.rotozoom(chicken_1,0,2),pygame.transform.rotozoom(chicken_2,0,2),pygame.transform.rotozoom(chicken_3,0,2)

			self.frames = [chicken_1,chicken_2,chicken_3]
			y_pos  = 500

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(1300,1500),y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 10
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(topleft = (1000,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False, pygame.sprite.collide_mask):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption('Kouprey Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Assets/sounds/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

angkor_surface = pygame.image.load('Assets/pics/angkor.png').convert()
angkor_surface = pygame.transform.smoothscale_by(angkor_surface,(1.1))

ground_surface = pygame.image.load('Assets/pics/ground.png').convert()
ground_surface = pygame.transform.smoothscale_by(ground_surface,(1.5))

# Intro screen
class Player_stand(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_stand_1 = pygame.image.load('Assets/pics/kouprey/kouprey1.png').convert_alpha()
		player_stand_2 = pygame.image.load('Assets/pics/kouprey/kouprey2.png').convert_alpha()
		player_stand_3 = pygame.image.load('Assets/pics/kouprey/kouprey3.png').convert_alpha()

		player_stand_1,player_stand_2,player_stand_3 = pygame.transform.rotozoom(player_stand_1,0,2.5),pygame.transform.rotozoom(player_stand_2,0,2.5),pygame.transform.rotozoom(player_stand_3,0,2.5)

		self.frames = [player_stand_1,player_stand_2,player_stand_3]
		self.player_index = 0

		self.image = self.frames[self.player_index]
		self.rect = self.image.get_rect(center = (600,300))

	def animation_state(self):
		self.player_index += 0.1
		if self.player_index >= len(self.frames):
			self.player_index = 0
		self.image = self.frames[int(self.player_index)]

	def update(self):
		self.animation_state()

intro_player = pygame.sprite.GroupSingle()
intro_player.add(Player_stand())

game_name = test_font.render('Kouprey Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (600,100))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (600,500))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,100)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['bird','chicken','chicken','chicken'])))
				pygame.time.set_timer(obstacle_timer, randint(800,1400))
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(angkor_surface,(-50,-50))
		screen.blit(ground_surface,(0,500))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		intro_player.draw(screen)
		intro_player.update()

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (600,500))
		screen.blit(game_name,game_name_rect)

		play_again = test_font.render("Press Space to play again",False,(111,196,169))
		play_again_rect = play_again.get_rect(center = (600,550))


		if score == 0: 
			screen.blit(game_message,game_message_rect)
		else: 
			screen.blit(score_message,score_message_rect)
			screen.blit(play_again,play_again_rect)

	pygame.display.update()
	clock.tick(60)