import pygame
from pygame import mixer
import os
import random
import csv
import button

pygame.init()
mixer.init()

clock = pygame.time.Clock()
FPS = 60

# constants
TILE_SIZE = 25
ROWS = 15
HEIGHT = ROWS * TILE_SIZE
WIDTH = HEIGHT * 2
COLS = WIDTH//TILE_SIZE
GRAVITY = 0.75
TILE_TYPES = 24
game_mode = "home"
menu_state = "main"
start_intro = False
pause_intro = False
can_click = True

# game variables
move_l = False
move_r = False
spit_fire = False
throw_fireball = False
fireball_thrown = False
freeze = False
selector = 0
regions = {0: "TU", 1: "GL", 2: "IC", 3: "SF"}
region = 0
alpha = 0
num = 0

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

# create screen and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hono the Fireslug")

# load images
# background images
mountain_img = pygame.transform.scale(pygame.image.load(
    "Assets/Images/bg_mountains_pix.png").convert_alpha(), (1200, HEIGHT))
pine1_img = pygame.transform.scale(pygame.image.load(
    "Assets/Images/bg_pine3.png").convert_alpha(), (1200, HEIGHT))

# world tiles
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Assets/Images/Editor/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# button images
start_img = pygame.image.load("Assets/Images/Buttons/start_btn.png").convert_alpha()
resume_img = pygame.image.load("Assets/Images/Buttons/resume_btn.png").convert_alpha()
options_img = pygame.image.load("Assets/Images/Buttons/options_btn.png").convert_alpha()
quit_img = pygame.image.load("Assets/Images/Buttons/quit_btn.png").convert_alpha()
settings_img = pygame.image.load("Assets/Images/Buttons/settings_btn.png").convert_alpha()
controls_img = pygame.image.load("Assets/Images/Buttons/controls_btn.png").convert_alpha()
back_img = pygame.image.load("Assets/Images/Buttons/back_btn.png").convert_alpha()
exit_img = pygame.image.load("Assets/Images/Buttons/exit_btn.png").convert_alpha()
home_img = pygame.image.load("Assets/Images/Buttons/home_btn.png").convert_alpha()
menu_img = pygame.image.load("Assets/Images/Buttons/menu_btn.png").convert_alpha()
market_img = pygame.image.load("Assets/Images/Buttons/market_btn.png").convert_alpha()

# items and projectiles
firespit_img = pygame.image.load("Assets/Images/Icons/fireball_pix.png").convert_alpha()
fireball_img = pygame.image.load("Assets/Images/Icons/fireball_pix.png").convert_alpha()
grain_img = pygame.image.load("Assets/Images/Icons/grain_pix.png").convert_alpha()
pebble_img = pygame.image.load("Assets/Images/Icons/pebble_pix.png").convert_alpha()
meat_img = pygame.image.load("Assets/Images/Icons/meat_pix.png").convert_alpha()
item_boxes = {"Grain": grain_img,
              "Pebble": pebble_img,
              "Meat": meat_img}

# load music and SFX
pygame.mixer.music.load("Assets/Audio/nature_theme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound("Assets/Audio/jump.mp3")
jump_fx.set_volume(0.1)
spit_fx = pygame.mixer.Sound("Assets/Audio/spit.mp3")
spit_fx.set_volume(0.1)
explosion_fx = pygame.mixer.Sound("Assets/Audio/explosion.mp3")
explosion_fx.set_volume(0.1)

# define font
font = pygame.font.SysFont("Futura", 30)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill((0, 255, 0))
    width = mountain_img.get_width()
    for x in range(4):
        screen.blit(mountain_img, (0, 0))
        screen.blit(pine1_img, (0, 500 - pine1_img.get_height()))


def reset_level():
    ice_slug_group.empty()
    toad_group.empty()
    firespit_group.empty()
    fireball_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    hazard_group.empty()
    exit_group.empty()

    # empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, char_name, x, y, scale, speed, ammo, fireballs):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.char_name = char_name
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.spit_cool = 0
        self.fireballs = fireballs
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.shiver = 0
        self.cool = False
        self.warm = False
        self.warmth = 0
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # load animations
        # load Hono animations
        if self.char_type == "player":
            animation_types = ["Idle", "Run", "Death", "Jump", "Crawl"]
            warmth_types = ["Warm", "Cool", "Cold"]
            for animation in animation_types:
                # reset temp_list1
                temp_list1 = []
                for temperature in warmth_types:
                    # reset temp_list2
                    temp_list2 = []
                    num_of_frames = len(os.listdir(f'Assets/Characters/{char_name}/{animation}/{temperature}'))
                    for i in range(num_of_frames):
                        img = pygame.image.load(f'Assets/Characters/{char_name}/{animation}/{temperature}/{i}.png')
                        img = pygame.transform.scale(img,
                                                     (int(img.get_width() * scale), (int(img.get_height() * scale))))
                        temp_list2.append(img)
                    temp_list1.append(temp_list2)
                self.animation_list.append(temp_list1)
            self.image = self.animation_list[self.action][self.warmth][self.frame_index]

        # load other enemy animations
        elif self.char_type == "enemy":
            animation_types = ["Idle", "Run", "Death"]
            for animation in animation_types:
                # reset temp_list1
                temp_list1 = []
                num_of_frames = len(os.listdir(f'Assets/Characters/{char_name}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'Assets/Characters/{char_name}/{animation}/{i}.png')
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                    temp_list1.append(img)
                self.animation_list.append(temp_list1)
            self.image = self.animation_list[self.action][self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.spit_cool > 0:
            self.spit_cool -= 1

    def move(self, move_left, move_right, num, alpha):
        # reset variables
        scene_change = False
        dx = 0
        dy = 0

        # move player
        if move_left:
            dx = -self.speed
            self.action = 1  # "Run" animation
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.action = 1  # "Run" animation
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -12
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision
        for tile in world.obastacle_list:
            # collision in x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # ai turn around
                if self.char_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0
            # collision in y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width + 1, self.height + 1):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # collision with hazard
        if pygame.sprite.spritecollide(self, hazard_group, False):
            self.health = 0

        # collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # fall off the map
        if self.rect.bottom > HEIGHT:
            self.health = 0

        # update player
        self.rect.x += dx
        self.rect.y += dy

        # change scene
        if self.char_type == "player":
            if self.rect.right >= WIDTH:
                num += 1
                scene_change = True
            elif self.rect.left <= 0 < num:
                num -= 1
                scene_change = True
            elif self.rect.top <= 0:
                alpha += 1
                scene_change = True
            elif self.rect.bottom >= HEIGHT and alpha > 0:
                alpha -= 1
                scene_change = True

        return scene_change, num, alpha

    def spit(self):
        if self.spit_cool == 0 and self.ammo > 0:
            self.spit_cool = 20
            firespit = Firespit(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery,
                                self.direction)
            firespit_group.add(firespit)
            # reduce ammo
            self.ammo -= 1
            spit_fx.play()

    def ai(self):
        if self.alive and player.alive:
            if self.char_name == "ice_slug":
                if not self.idling and random.randint(1, 200) == 1:
                    self.update_action(0)  # idle
                    self.idling = True
                    self.idling_counter = 20
            elif self.char_name == "mammoth_toad":
                if not self.idling and random.randint(1, 200) == 1:
                    self.update_action(0)  # idle
                    self.idling = True
                    self.idling_counter = 120
            # check proximity of player
            if self.vision.colliderect(player.rect):
                # stop and face player
                self.update_action(0)
                # shoot at player
                self.spit()
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.update_action(1)  # "Run" animation
                    self.move(ai_moving_left, ai_moving_right, num, alpha)
                    self.move_counter += 1
                    # update vision
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE * 2:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False

    def update_animation(self):
        ANIMATION_COOLDOWN = 200 - self.shiver * 50
        if self.char_type == "player":
            self.image = self.animation_list[self.action][self.warmth][self.frame_index]
            # check if enough time has passed
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action][self.warmth]):
                if self.action == 2:  # run Death animation once
                    self.frame_index = len(self.animation_list[self.action][self.warmth]) - 1
                else:
                    self.frame_index = 0

            # check player temperature
            if self.cool:
                self.shiver += 1
                self.warmth += 1
                self.cool = False
            elif self.warm:
                self.shiver -= 1
                self.warmth -= 1
                self.warm = False
            elif freeze:
                self.frame_index = 0

        elif self.char_type == "enemy":
            self.image = self.animation_list[self.action][self.frame_index]
            # check if enough time has passed
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different from the old action
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Toad(pygame.sprite.Sprite):
    def __init__(self, char_type, char_name, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.char_name = char_name
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.attack = False
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 60)
        self.idling = False
        self.idling_counter = 0

        # load animations
        animation_types = ["Idle", "Run", "Death"]
        for animation in animation_types:
            # reset temp_list1
            temp_list1 = []
            num_of_frames = len(os.listdir(f'Assets/Characters/{char_name}/{animation}')) - 1
            for i in range(num_of_frames):
                img = pygame.image.load(f'Assets/Characters/{char_name}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                temp_list1.append(img)
            self.animation_list.append(temp_list1)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()

    def move(self, move_left, move_right):
        # reset variables
        dx = 0
        dy = 0

        # move toad
        if move_left:
            dx = -self.speed
            self.action = 1  # "Run" animation
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.action = 1  # "Run" animation
            self.flip = False
            self.direction = 1

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision
        for tile in world.obastacle_list:
            # collision in x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.direction *= -1
                self.move_counter = 0
            # collision in y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update toad
        self.rect.x += dx
        self.rect.y += dy

    def ai(self):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)  # idle
                self.idling = True
                self.idling_counter = 60
            # check proximity of player
            if self.vision.colliderect(player.rect):
                # stop and face player
                self.update_action(0)
                # shoot at player
                self.attack = True
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.update_action(1)  # "Run" animation
                    self.move(ai_moving_left, ai_moving_right)
                    self.move_counter += 1
                    # update vision
                    self.vision.center = (self.rect.centerx + (self.width // 2) * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE * 10:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False

    def update_animation(self):
        ANIMATION_COOLDOWN = 250
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different from the old action
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class HeadFlame(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # load animations
        num_of_frames = len(os.listdir('Assets/Characters/Hono/Flame')) - 1
        for i in range(num_of_frames):
            img = pygame.image.load(f'Assets/Characters/Hono/Flame/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
            self.animation_list.append(img)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_animation(self):
        ANIMATION_COOLDOWN = 150
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def follow(self, leader):
        dx = 0
        dy = 0
        if leader.rect.centerx + (0.25 * leader.rect.width * leader.direction) != self.rect.centerx:
            dx = leader.rect.centerx + (0.25 * leader.rect.width * leader.direction) - self.rect.centerx
        if leader.rect.y != self.rect.y + self.rect.height:
            dy = leader.rect.y - self.rect.y + self.rect.height

        # update flame position
        self.rect.centerx += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, (self.rect.centerx, self.rect.y - self.rect.height))


class World:
    def __init__(self):
        self.obastacle_list = []
        self.level_length = 0

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through data
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 0:  # player
                        player = Character('player', 'Hono', x * TILE_SIZE, y * TILE_SIZE, 1, 5, 20, 5)
                        health_bar = Healthbar(10, 10, player.health, player.health)
                        headflame = HeadFlame(player.rect.x, player.rect.y - 0.5 * player.rect.size[1], 1)
                    elif tile == 1:  # ice slug
                        ice_slug = Character('enemy', 'ice_slug', x * TILE_SIZE, (y * TILE_SIZE), 1, 3, 20, 0)
                        ice_slug_group.add(ice_slug)
                    elif tile == 2:  # mammoth toad
                        toad = Character('enemy', 'mammoth_toad', x * TILE_SIZE, (y * TILE_SIZE), 2, 2, 0, 0)
                        toad_group.add(toad)
                    elif tile == 3:  # meat
                        meat_box = ItemBox("Meat", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(meat_box)
                    elif tile == 4:  # pebble
                        pebble_box = ItemBox("Pebble", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(pebble_box)
                    elif tile == 5:  # grain
                        grain_box = ItemBox("Grain", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(grain_box)
                    elif tile == 6:  # exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 7:  # hazard
                        hazard = Hazard(img, x * TILE_SIZE, y * TILE_SIZE)
                        hazard_group.add(hazard)
                    elif 8 <= tile <= 23:  # ground
                        self.obastacle_list.append(tile_data)
                    elif tile == 25:  # decoration
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)

        return player, health_bar

    def draw(self):
        for tile in self.obastacle_list:
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height))


class Hazard(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.vel_y = 0
        self.in_air = False
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # check if player collision
        if pygame.sprite.collide_rect(self, player):
            # check box type
            if self.item_type == "Grain":
                player.health += 20
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Pebble":
                player.fireballs += 1
            elif self.item_type == "Meat":
                player.ammo += 3
            # delete box
            self.kill()


class Healthbar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update health
        self.health = health
        # calculate ratio
        ratio = self.health / self.max_health

        pygame.draw.rect(screen, "black", (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, "red", (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, "green", (self.x, self.y, 150 * ratio, 20))


class Firespit(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = firespit_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move firespit
        self.rect.x += (self.direction * self.speed)
        # check if off the screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
        # check collision with level
        if tile in world.obastacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, firespit_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for ice_slug in ice_slug_group:
            if pygame.sprite.spritecollide(ice_slug, firespit_group, False):
                if ice_slug.alive:
                    ice_slug.health -= 100
                    self.kill()
        for toad in toad_group:
            if pygame.sprite.spritecollide(toad, firespit_group, False):
                if toad.alive:
                    toad.health -= 50
                    self.kill()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = fireball_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # check collision with level
        for tile in world.obastacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            # collision in y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update fireball position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            # do damage to nearby characters
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for ice_slug in ice_slug_group:
                if abs(self.rect.centerx - ice_slug.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - ice_slug.rect.centery) < TILE_SIZE * 2:
                    ice_slug.health -= 50
            for toad in toad_group:
                if abs(self.rect.centerx - toad.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - toad.rect.centery) < TILE_SIZE * 2:
                    toad.health -= 25


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0, 3):
            img = pygame.image.load(f'Assets/Characters/Hono/Explosion/expo{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # zoom out fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, WIDTH // 2, HEIGHT))
            pygame.draw.rect(screen, self.color, (WIDTH // 2 + self.fade_counter, 0, WIDTH, HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, WIDTH, HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, HEIGHT // 2 + self.fade_counter, WIDTH, HEIGHT))

        if self.direction == 2:  # vertical fade down
            pygame.draw.rect(screen, self.color, (0, 0, WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= WIDTH:
            fade_complete = True

        return fade_complete


# screen fades
intro_fade = ScreenFade(1, BLACK, 6)
death_fade = ScreenFade(2, PINK, 4)
pause_menu = ScreenFade(2, WHITE, 20)

# create buttons
start_button = button.Button(WIDTH // 2, 105, start_img, 2)
resume_button = button.Button(WIDTH // 2, 100, resume_img, 2)
options_button = button.Button(WIDTH // 2, 190, options_img, 2)
quit_button = button.Button(WIDTH // 2, 280, quit_img, 2)
settings_button = button.Button(WIDTH // 2, 200, settings_img, 2)
controls_button = button.Button(WIDTH // 2, 290, controls_img, 2)
back_button = button.Button(WIDTH // 2, 380, back_img, 2)
home_button = button.Button(147, 10, home_img, 1)
menu_button = button.Button(50, 10, menu_img, 1)
exit_button = button.Button(WIDTH // 2, 275, exit_img, 2)
market_button = button.Button(WIDTH // 2, 200, market_img, 2)

# create sprite groups
ice_slug_group = pygame.sprite.Group()
toad_group = pygame.sprite.Group()
firespit_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
hazard_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load level data
with open(f"Map/{regions[region]}/{regions[region]}_map_{alpha}-{num}.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for y, row in enumerate(reader):
        for x, tile in enumerate(row):
            world_data[y][x] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)

# main loop
run = True
while run:
    clock.tick(FPS)

    # Menu Functions
    # check if the mouse has already clicked
    if not pygame.mouse.get_pressed(3)[0]:
        can_click = True
    if can_click:
        # check if game_mode is home
        if game_mode == "home":
            screen.fill(WHITE)
            # check menu state
            if menu_state == "main":
                if start_button.draw(screen):
                    game_mode = "play"
                    start_intro = True
                    can_click = False
                elif options_button.draw(screen):
                    menu_state = "options"
                    can_click = False
                elif exit_button.draw(screen):
                    run = False
                    can_click = False
            elif menu_state == "options":
                if settings_button.draw(screen):
                    print("Settings")
                    can_click = False
                elif controls_button.draw(screen):
                    print("Controls")
                    can_click = False
                elif back_button.draw(screen):
                    menu_state = "main"
                    can_click = False

        if pause_intro:
            if pause_menu.fade():
                pause_intro = False
                pause_menu.fade_counter = 0

        # check if game_mode is paused
        elif game_mode == "paused":
            screen.fill("lightgray")
            # check menu state
            if menu_state == "main":
                if resume_button.draw(screen):
                    game_mode = "play"
                    can_click = False
                if options_button.draw(screen):
                    menu_state = "options"
                    can_click = False
                if quit_button.draw(screen):
                    game_mode = "home"
                    can_click = False
            elif menu_state == "options":
                if settings_button.draw(screen):
                    print("Settings")
                    can_click = False
                if controls_button.draw(screen):
                    print("Controls")
                    can_click = False
                if back_button.draw(screen):
                    menu_state = "main"
                    can_click = False

    # play the game
    if game_mode == "play":
        draw_bg()
        # draw world map
        world.draw()
        # show player health
        health_bar.draw(player.health)
        # show ammo
        draw_text("AMMO:  ", font, "white", 10, 35)
        for x in range(player.ammo):
            screen.blit(pebble_img, (90 + x * 12, 40))
        # show fireballs
        draw_text("FIREBALLS:  ", font, "white", 10, 60)
        for x in range(player.fireballs):
            screen.blit(fireball_img, (130 + x * 15, 60))

        # update and draw characters
        for ice_slug in ice_slug_group:
            ice_slug.ai()
            ice_slug.update()
            ice_slug.draw()
        for toad in toad_group:
            toad.ai()
            toad.update()
            toad.draw()

        player.update()
        player.draw()

        # update groups
        firespit_group.update()
        fireball_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        hazard_group.update()
        exit_group.update()

        # draw groups
        firespit_group.draw(screen)
        fireball_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        hazard_group.draw(screen)
        exit_group.draw(screen)

        # show intro fade
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            # spit fire
            if spit_fire:
                player.spit()
            # throw fireball
            elif throw_fireball and not fireball_thrown and player.fireballs > 0:
                fireball = Fireball(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                    player.rect.top, player.direction)
                fireball_group.add(fireball)
                player.fireballs -= 1
                fireball_thrown = True

            if player.in_air:
                player.update_action(3)  # jump
            elif move_l or move_r:
                player.update_action(1)  # run
            elif freeze:
                player.update_action(2)  # death
            else:
                player.update_action(0)  # idle

            scene_change, num, alpha = player.move(move_l, move_r, num, alpha)

            if scene_change:
                with open(f"Map/{regions[region]}/{regions[region]}_map_{alpha}-{num}.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                player, health_bar = world.process_data(world_data)

        else:
            if death_fade.fade():
                if resume_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    world_data = reset_level()
                    # load level data
                    with open(f"Map/{regions[region]}/{regions[region]}_map_{alpha}-{num}.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player, health_bar = world.process_data(world_data)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # move left
                move_l = True
            if event.key == pygame.K_RIGHT:  # move right
                move_r = True
            if event.key == pygame.K_UP and player.alive:  # jump
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:  # exit game
                run = False
            if event.key == pygame.K_c:
                player.cool = True
            if event.key == pygame.K_h:
                player.warm = True
            if event.key == pygame.K_x:
                freeze = True
            if event.key == pygame.K_SPACE:  # spit fire
                spit_fire = True
            if event.key == pygame.K_q:  # throw fireball
                throw_fireball = True
            if event.key == pygame.K_p:  # pause game
                game_mode = "paused"
                pause_intro = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:  # stop moving left
                move_l = False
            if event.key == pygame.K_RIGHT:  # stop moving right
                move_r = False
            if event.key == pygame.K_SPACE:  # stop spitting fire
                spit_fire = False
            if event.key == pygame.K_q:  # reset fireball charge
                throw_fireball = False
                fireball_thrown = False

    pygame.display.update()

pygame.quit()
