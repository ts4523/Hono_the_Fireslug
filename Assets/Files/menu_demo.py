import pygame
import button_demo

pygame.init()

# create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Demo")

# define variables
game_paused = False

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colors
COL = (255, 255, 255)

# create button image
resume_img = pygame.image.load("/personal_projects/Hono_the_Fireslug/Assets/Images/meat.png").convert_alpha()

# create button instances
resume_button = button_demo.Button(200, 98, 390, 158, resume_img)


def draw_txt(txt, font, color, x, y):
    img = font.render(txt, 1, color)
    screen.blit(img, (x, y))


run = True
while run:

    screen.fill((52, 78, 91))

    # check if game is paused
    if game_paused:
        if resume_button.draw(screen):
            game_paused = False
        pass
    else:
        draw_txt("Press SPACE to pause.", font, COL, 160, 250)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
                print("Pause")
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
