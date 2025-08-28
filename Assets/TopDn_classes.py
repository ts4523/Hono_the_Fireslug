import pygame
import math
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# constants
WIDTH = 1200
HEIGHT = 600
WHITE = (255, 255, 255)

# create screen and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player")

# load background image
BG = pygame.image.load("/personal_projects/Hono_the_Fireslug/Assets/Images/bg_winter_forest.jpg").convert()
bg_width = BG.get_width()

# game variables
tiles = math.ceil(WIDTH / bg_width) + 1
scroll = 0
move_l = False
move_r = False
move_up = False
move_dn = False
attack = False
interact = False


def draw_bg(scroll):
    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(BG, (i * bg_width + scroll, 0))

        # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    pygame.draw.line(screen, WHITE, (0, 530), (WIDTH, 530))
    return scroll


class Goblin(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load animations
        animation_types = ["Walk", "Idle"]
        directions = ["North", "South", "East"]
        for animation in animation_types:
            temp_dir_list = []
            for direction in directions:
                # reset temp_list
                temp_list = []
                num_of_frames = len(os.listdir(f'goblin/{animation}/{direction}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'goblin/{animation}/{direction}/{i}.png')
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                    temp_list.append(img)
                temp_dir_list.append(temp_list)
            self.animation_list.append(temp_dir_list)

        self.image = self.animation_list[self.action][self.direction][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, move_left, move_right, move_up, move_down):
        # reset variables
        dx = 0
        dy = 0

        # move player
        if move_right:
            dx = self.speed
            self.action = 0
            if move_up:
                dy = -self.speed
                self.direction = 0
            elif move_down:
                dy = self.speed
                self.direction = 1
            else:
                self.direction = 2
            self.flip = False
        elif move_left:
            dx = -self.speed
            self.action = 0
            if move_up:
                dy = -self.speed
                self.direction = 0
                self.flip = False
            elif move_down:
                dy = self.speed
                self.direction = 1
                self.flip = False
            else:
                self.direction = 2
                self.flip = True
        elif move_up:
            dy = -self.speed
            self.action = 0
            self.flip = False
            self.direction = 0
        elif move_down:
            dy = self.speed
            self.action = 0
            self.flip = False
            self.direction = 1
        else:
            self.action = 1
            self.flip = False
            self.direction = 0

        # update player
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 200
        self.image = self.animation_list[self.action][self.direction][self.frame_index]
        # check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action][self.direction]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


'''
# create player
player = Goblin('goblin', WIDTH/2, 400, 1, 2)


run = True
while run:
    clock.tick(FPS)

    screen.fill("darkgrey")

    player.update_animation()
    player.draw()

    # update player actions
    if player.alive:
        if move_l or move_r or move_up or move_dn:
            player.update_action(0)  # walk
        elif attack:
            player.update_action(2)  # attack
        elif interact:
            player.update_action(3)  # general interact
        else:
            player.update_action(1)  # idle
        player.move(move_l, move_r, move_up, move_dn)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_l = True
            if event.key == pygame.K_RIGHT:
                move_r = True
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_dn = True
            if event.key == pygame.K_a:
                attack = True
            if event.key == pygame.K_d:
                interact = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_l = False
            if event.key == pygame.K_RIGHT:
                move_r = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_dn = False

    pygame.display.update()
'''
