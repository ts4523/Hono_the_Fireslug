import pygame
import button
import csv

pygame.init()
clock = pygame.time.Clock()
FPS = 60

# game window
WIDTH = 800
HEIGHT = 480
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

# game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = HEIGHT//ROWS
TILE_TYPES = 24
level = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0

# load images
mountain_img = pygame.transform.scale(pygame.image.load(
    "Assets/Images/bg_mountains_pix.png").convert_alpha(), (1200, HEIGHT))
pine1_img = pygame.transform.scale(pygame.image.load("Assets/Images/bg_pine3.png").convert_alpha(), (1200, HEIGHT - 100))
# store tiles in list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Assets/Images/Editor/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load(f"Assets/Images/Buttons/save_btn.png").convert_alpha()
load_img = pygame.image.load(f"Assets/Images/Buttons/load_btn.png").convert_alpha()

# colors
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
RED = (200, 25, 25)

# fonts
font = pygame.font.SysFont("Futura", 30)

# tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 10


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# draw background
def draw_bg():
    screen.fill(GREEN)
    width = mountain_img.get_width()
    for x in range(4):
        screen.blit(mountain_img, ((x*width)-scroll*.5, 0))
        screen.blit(pine1_img, ((x*width)-scroll, HEIGHT - pine1_img.get_height()))


# drawing world
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                if tile == 23:
                    pygame.transform.scale(img_list[tile], (2*TILE_SIZE, 2*TILE_SIZE))
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c*TILE_SIZE - scroll, 0), (c*TILE_SIZE - scroll, HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c*TILE_SIZE), (WIDTH, c*TILE_SIZE))


# create buttons
save_button = button.Button(WIDTH // 2, HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(WIDTH // 2, HEIGHT + LOWER_MARGIN - 90, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(WIDTH + (75 * button_col) + 75, (50 * button_row) + 75, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, HEIGHT + LOWER_MARGIN - 60)

    # save and load data
    if save_button.draw(screen):
        with open(f"Map/level{level}_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        scroll = 0
        with open(f"Map/level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    '''if save_button.draw(screen):
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_grid, pickle_out)
        pickle_out.close()
    if load_button.draw(screen):
        scroll = 0
        world_grid = []
        pickle_in = open(f'level{level}_data', 'rb')
        world_grid = pickle.load(pickle_in)'''

    # draw panel and buttons
    pygame.draw.rect(screen, GREEN, (WIDTH, 0, SIDE_MARGIN, HEIGHT))

    # choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    # highlight
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles
    pos = pygame.mouse.get_pos()
    '''if tile == 23:
        x = (pos[0] + scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE'''
    x = (pos[0] + scroll)//TILE_SIZE
    y = pos[1] // TILE_SIZE

    if 0 < pos[0] < WIDTH and 0 < pos[1] < HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()

