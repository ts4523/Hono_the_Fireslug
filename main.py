import pygame
import time
import button
# import sprite
# import random
import market

# fonts
pygame.font.init()
TITLE = pygame.font.SysFont("timesnewroman", 30)
H1 = pygame.font.SysFont("timesnewroman", 20)
H2 = pygame.font.SysFont("timesnewroman", 15)
NORM = pygame.font.SysFont("timesnewroman", 12)
SUB = pygame.font.SysFont("timesnewroman", 10)

# constants
WIDTH, HEIGHT = 1000, 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
CURSOR_WIDTH = 30
CURSOR_HEIGHT = 40
CURSOR_VEL = 5
GOLD_X = WIDTH - 200
GOLD_Y = HEIGHT - 50

# create screens
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# create main screen caption and background image
pygame.display.set_caption("DND Simulator")
BG = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/bg_beach.jpg"), (WIDTH, HEIGHT))

# create images
CURSOR = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/cursor.png"), (30, 40))
POINTER = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/pointer.png"), (20, 30))
coin_img = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/coin.png"), (30, 30))

# create button images
start_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/start_btn.png").convert_alpha()
resume_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/resume_btn.png").convert_alpha()
options_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/options_btn.png").convert_alpha()
quit_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/quit_btn.png").convert_alpha()
settings_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/settings_btn.png").convert_alpha()
controls_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/controls_btn.png").convert_alpha()
back_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/back_btn.png").convert_alpha()
exit_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/exit_btn.png").convert_alpha()
home_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/home_btn.png").convert_alpha()
menu_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/menu_btn.png").convert_alpha()
market_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/market_btn.png").convert_alpha()

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


def draw(run, player, elapsed_time, cursor):
    if start_button.draw(screen):
        print('start')
    if exit_button.draw(screen):
        run = False
    if market_button.draw(screen):
        print('market')

    pygame.draw.circle(screen, 'gold', (GOLD_X, GOLD_Y), 8, 0)

    time_text = NORM.render(f"Time: {round(elapsed_time)}s", 1, "white")
    screen.blit(time_text, (10, 10))
    gold_txt = NORM.render('Gold: ', 1, 'gold')
    screen.blit(gold_txt, (GOLD_X + 10, GOLD_Y - 8))

    pygame.display.update()

    return run


def draw_txt(txt, font, color, x, y):
    img = font.render(f"{txt}", 1, color)
    screen.blit(img, (x, y))


def main():
    # local variables
    run = True
    game_mode = "home"
    menu_state = "main"

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    # button = pygame.Rect((WIDTH/2 - BUTTON_W/2), (HEIGHT/2 - BUTTON_H/2), BUTTON_W, BUTTON_H)
    cursor = pygame.Rect(400, 300, CURSOR_WIDTH, CURSOR_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        screen.fill('grey')

        # check if game_mode is home
        if game_mode == "home":
            # check menu state
            if menu_state == "main":
                if start_button.draw(screen):
                    game_mode = "play"
                if options_button.draw(screen):
                    menu_state = "options"
                if exit_button.draw(screen):
                    run = False
            elif menu_state == "options":
                if settings_button.draw(screen):
                    print("Settings")
                if controls_button.draw(screen):
                    print("Controls")
                if back_button.draw(screen):
                    menu_state = "main"

        # check if game_mode is paused
        if game_mode == "paused":
            # check menu state
            if menu_state == "main":
                if resume_button.draw(screen):
                    game_mode = "play"
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    run = False
            elif menu_state == "options":
                if settings_button.draw(screen):
                    print("Settings")
                if controls_button.draw(screen):
                    print("Controls")
                if back_button.draw(screen):
                    menu_state = "main"

        # game_mode is play
        elif game_mode == "play":
            # check if market has been selected
            if market_button.draw(screen):
                market.market()
                print('market')
            if home_button.draw(screen):
                game_mode = "home"
            if menu_button.draw(screen):
                game_mode = "paused"
            # draw_txt("Press SPACE to pause.", TITLE, "white", 450, 100)
            pygame.draw.circle(screen, 'gold', (GOLD_X, GOLD_Y), 8, 0)

            # time_text = NORM.render(f"Time: {round(elapsed_time)}s", 1, "white")
            # screen.blit(time_text, (10, 10))
            # gold_txt = NORM.render('Gold: ', 1, 'gold')
            # screen.blit(gold_txt, (GOLD_X + 10, GOLD_Y - 8))

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_mode = "paused"
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        # Arrow keys control red Player
        if keys[pygame.K_LEFT] and player.x != 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x != (WIDTH - PLAYER_WIDTH):
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y != 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y != (HEIGHT - PLAYER_HEIGHT):
            player.y += PLAYER_VEL

        # A, S, W, D keys control black Cursor
        if keys[pygame.K_a] and cursor.x != 0:
            cursor.x -= CURSOR_VEL
        if keys[pygame.K_d] and cursor.x != (WIDTH - CURSOR_WIDTH):
            cursor.x += CURSOR_VEL
        if keys[pygame.K_w] and cursor.y != 0:
            cursor.y -= CURSOR_VEL
        if keys[pygame.K_s] and cursor.y != (HEIGHT - CURSOR_HEIGHT):
            cursor.y += CURSOR_VEL

        pygame.display.update()
        # run = draw(run, player, elapsed_time, cursor)

    pygame.quit()


if __name__ == "__main__":
    main()
