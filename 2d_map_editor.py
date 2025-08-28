import pygame
import button
import csv

pygame.init()
clock = pygame.time.Clock()
FPS = 60

# game window
TILE_SIZE = 25
ROWS = 12
HEIGHT = ROWS * TILE_SIZE
WIDTH = HEIGHT * 2
COLS = WIDTH//TILE_SIZE
LOWER_MARGIN = 100
SIDE_MARGIN = 300


def screen_dim():
    pass


screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

# game variables
TILE_TYPES = 24
mode = 1
scroll_x = 0
scroll_y = 0
scroll_speed = 1
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
do_scroll_map = False
current_tile = 0
selector = 0
regions = {0: "TU", 1: "GL", 2: "IC", 3: "SF"}
region = 0
alpha = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
sub = 0
num_x = 0
num_y = 0
timer = 0
save = False
test_hit = False


# load images
mountain_img = pygame.transform.scale(pygame.image.load(
    "Assets/Images/bg_mountains_pix.png").convert_alpha(), (1200, HEIGHT))
pine1_img = pygame.transform.scale(pygame.image.load(
    "Assets/Images/bg_pine3.png").convert_alpha(), (1200, HEIGHT - 100))
# store tiles in list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Assets/Images/Editor/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load(f"Assets/Images/Buttons/save_btn.png").convert_alpha()
load_img = pygame.image.load(f"Assets/Images/Buttons/load_btn.png").convert_alpha()
col_r_img = pygame.image.load(f"Assets/Images/Buttons/col_r_btn.png").convert_alpha()
col_l_img = pygame.image.load(f"Assets/Images/Buttons/col_l_btn.png").convert_alpha()
row_up_img = pygame.image.load(f"Assets/Images/Buttons/row_up_btn.png").convert_alpha()
row_dn_img = pygame.image.load(f"Assets/Images/Buttons/row_dn_btn.png").convert_alpha()
arrow_up_img = pygame.image.load(f"Assets/Images/Buttons/arrow_up.png").convert_alpha()
arrow_dn_img = pygame.image.load(f"Assets/Images/Buttons/arrow_dn.png").convert_alpha()
arrow_l_img = pygame.image.load(f"Assets/Images/Buttons/arrow_l.png").convert_alpha()
arrow_r_img = pygame.image.load(f"Assets/Images/Buttons/arrow_r.png").convert_alpha()

# colors
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
RED = (200, 25, 25)

# fonts
font = pygame.font.SysFont("Futura", 20)

# tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# create ground
for tile in range(0, COLS):
    world_data[ROWS - 1][tile] = 10


def fade_text(text, font, color, x, y, trigger, fade_time):
    img = font.render(text, True, color)
    if timer < fade_time:  # while the timer is beneath the time limit
        screen.blit(img, (x, y))
    else:
        trigger = False

    return trigger


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_text2(text, font, color, x, y, fade, time, trigger):
    img = font.render(text, True, color)
    if not fade:  # set text to static
        screen.blit(img, (x, y))
    elif fade and trigger:  # draw text for set amount of time when the trigger is hit
        if timer < time:  # while the timer is beneath the time limit
            screen.blit(img, (x, y))
        else:
            trigger = False

        return trigger


# draw background
def draw_bg():
    screen.fill("lightgray")
    # screen.blit(mountain_img, (0, 0))
    # screen.blit(pine1_img, (0, HEIGHT - pine1_img.get_height()))


# drawing world
def draw_world():
    # for each row in the world_grid list
    for y, row in enumerate(world_data):
        # for each tile in the row
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll_x, y * TILE_SIZE - scroll_y))


def update_world():
    # for each row in the world_grid list
    for y, row in enumerate(world_data):
        # for each tile in the row
        for x, tile in enumerate(row):
            tile = update_tile(x, y, tile)
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))


def draw_grid():
    # vertical lines
    for c in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (c*TILE_SIZE - scroll_x, 0), (c*TILE_SIZE - scroll_x, HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c*TILE_SIZE - scroll_y), (WIDTH, c*TILE_SIZE - scroll_y))


def check_above_tile(y, x):
    # if not on the top-most row and the tile above is air
    if y > 0:
        if world_data[y - 1][x] == -1:
            return True
    else:
        return False


def check_below_tile(y, x):
    # if not on the bottom-most row and the tile below is air
    if y < ROWS - 1:
        if world_data[y + 1][x] == -1:
            return True
    else:
        return False


def check_left_tile(y, x):
    # if not on the left-most column and the tile to the left is air
    if x > 0:
        if world_data[y][x - 1] == -1:
            return True
    else:
        return False


def check_right_tile(y, x):
    # if not on the right-most column and the tile to the right is air
    if x < COLS - 1:
        if world_data[y][x + 1] == -1:
            return True
    else:
        return False


def update_tile(y, x, new_tile):
    if new_tile > 7:
        if check_above_tile(y, x):
            if check_below_tile(y, x):
                if check_left_tile(y, x):
                    if check_right_tile(y, x):
                        new_tile = 22  # all sides tile
                    else:
                        new_tile = 17  # top-bottom-left tile
                else:
                    if check_right_tile(y, x):
                        new_tile = 19  # top-bottom-right tile
                    else:
                        new_tile = 18  # top-bottom tile
            else:
                if check_left_tile(y, x):
                    if check_right_tile(y, x):
                        new_tile = 21  # top-left-right tile
                    else:
                        new_tile = 9  # top-left tile
                else:
                    if check_right_tile(y, x):
                        new_tile = 11  # top-right tile
                    else:
                        new_tile = 10  # top tile
        else:
            if check_below_tile(y, x):
                if check_left_tile(y, x):
                    if check_right_tile(y, x):
                        new_tile = 20  # bottom-left-right tile
                    else:
                        new_tile = 14  # bottom-left tile
                else:
                    if check_right_tile(y, x):
                        new_tile = 16  # bottom-right tile
                    else:
                        new_tile = 15  # bottom tile
            else:
                if check_left_tile(y, x):
                    if check_right_tile(y, x):
                        new_tile = 23  # left-right tile
                    else:
                        new_tile = 12  # right tile
                else:
                    if check_right_tile(y, x):
                        new_tile = 13  # left tile
                    else:
                        new_tile = 8  # center tile

    # print(new_tile)
    return new_tile


# create buttons
save_button = button.Button(WIDTH // 2 + 60, HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(WIDTH // 2 + 60, HEIGHT + LOWER_MARGIN - 90, load_img, 1)
col_r_btn = button.Button(WIDTH + 210, HEIGHT + LOWER_MARGIN - 100, col_r_img, 1)
col_l_btn = button.Button(WIDTH + 90, HEIGHT + LOWER_MARGIN - 100, col_l_img, 1)
row_up_btn = button.Button(WIDTH + 150, HEIGHT + LOWER_MARGIN - 140, row_up_img, 1)
row_dn_btn = button.Button(WIDTH + 150, HEIGHT + LOWER_MARGIN - 60, row_dn_img, 1)
'''
arrow_up_btn = button.Button(WIDTH + 120, HEIGHT + LOWER_MARGIN - 120, arrow_up_img, 1)
arrow_dn_btn = button.Button(WIDTH + 120, HEIGHT + LOWER_MARGIN - 40, arrow_dn_img, 1)
arrow_l_btn = button.Button(WIDTH + 120, HEIGHT + LOWER_MARGIN - 120, arrow_l_img, 1)
arrow_r_btn = button.Button(WIDTH + 120, HEIGHT + LOWER_MARGIN - 40, arrow_r_img, 1)
'''

button_list = []
button_col = 0
button_row = 0
for i in range(9):
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

    # draw panels
    pygame.draw.rect(screen, "grey", (WIDTH + 1, 0, SIDE_MARGIN, HEIGHT + 1))
    pygame.draw.rect(screen, "grey", (0, HEIGHT + 1, WIDTH + SIDE_MARGIN, LOWER_MARGIN))

    # highlight file selector
    if mode == 1:
        if selector == 0:
            pygame.draw.rect(screen, "black", (40, 310, 40, 12))
        elif selector == 1:
            pygame.draw.rect(screen, "black", (122, 310, 10, 12))
        elif selector == 2:
            pygame.draw.rect(screen, "black", (130, 310, 9, 12))
        elif selector == 3:
            pygame.draw.rect(screen, "black", (141, 310, 9, 12))

    # draw information text
    draw_text(f'File: {regions[region]}/{regions[region]}_map_{alpha[sub]}{num_x}-{num_y}',
              font, WHITE, 10, HEIGHT + LOWER_MARGIN - 90)
    if mode == 1:
        draw_text('Mode: File Selection', font, WHITE, 10, HEIGHT + LOWER_MARGIN - 70)
        draw_text('Press LEFT or RIGHT to change selector', font, WHITE, 30, HEIGHT + LOWER_MARGIN - 50)
        draw_text('Press UP or DOWN to change file', font, WHITE, 30, HEIGHT + LOWER_MARGIN - 30)
    elif mode == -1:
        draw_text('Mode: Scroll', font, WHITE, 10, HEIGHT + LOWER_MARGIN - 70)
        draw_text('Use arrow keys to scroll map', font, WHITE, 30, HEIGHT + LOWER_MARGIN - 50)

    # save and load data
    # "region" signifies the folder the map is from, "sub" signifies the subregion the map
    # covers, "num_x" signifies the row and "num_y" signifies the column the section covers
    if save_button.draw(screen):
        save = True
        timer = 0  # reset timer
        with open(f"Map/{regions[region]}/{regions[region]}_map_{alpha[sub]}{num_x}-{num_y}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for row in world_data:
                writer.writerow(row)

    # draw save notification
    if save:
        save = fade_text("File Saved", font, (0, 0, 0), 10, 10, save, 80)
        timer += 1

    if load_button.draw(screen):
        scroll = 0
        new_world_data = []
        with open(f"Map/{regions[region]}/{regions[region]}_map_{alpha[sub]}{num_x}-{num_y}.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                temp_list1 = []
                for tile in row:
                    temp_list1.append(int(tile))
                new_world_data.append(temp_list1)

        ROWS = len(new_world_data)
        COLS = len(new_world_data[0])
        world_data = new_world_data

    # map size editor
    if col_l_btn.draw(screen):  # add a column to the left
        for row in world_data:
            row.insert(0, -1)
        COLS += 1
    if col_r_btn.draw(screen):  # add a column to the right
        for row in world_data:
            row.append(-1)
        COLS += 1
    if row_up_btn.draw(screen):  # add a row to the top
        new_row = []
        for y in range(0, len(world_data[0])):
            new_row.append(-1)
        world_data.insert(0, new_row)
        ROWS += 1
    if row_dn_btn.draw(screen):  # add a row to the bottom
        new_row = []
        for y in range(0, len(world_data[0])):
            new_row.append(-1)
        world_data.append(new_row)
        ROWS += 1

    # choose tile button
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    # highlight tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left and scroll_x > 0:
        scroll_x -= 5 * scroll_speed
    if scroll_right and scroll_x < (COLS * TILE_SIZE) - WIDTH:
        scroll_x += 5 * scroll_speed
    if scroll_up and scroll_y > 0:
        scroll_y -= 5 * scroll_speed
    if scroll_down and scroll_y < (ROWS * TILE_SIZE) - HEIGHT:
        scroll_y += 5 * scroll_speed

    # draw new tiles
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_x) // TILE_SIZE
    y = (pos[1] + scroll_y) // TILE_SIZE
    # print(pos[0], pos[1])

    # if the mouse is clicked on a tile space, draw a tile
    if 0 < pos[0] < WIDTH and 0 < pos[1] < HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            # if the new tile is different from the current tile, update to the new tile
            if world_data[y][x] != current_tile:
                world_data[y][x] = update_tile(y, x, current_tile)
        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    # event handler
    for event in pygame.event.get():
        # quit program
        if event.type == pygame.QUIT:
            run = False

        # key presses
        if event.type == pygame.KEYDOWN:
            # draw_text2 test
            '''if event.key == pygame.K_SPACE:
                test_hit = True'''

            # quit program
            if event.key == pygame.K_ESCAPE:
                run = False

            # mode selector
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
                mode *= -1
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5
                mode *= -1

            # scroller mode
            if mode < 0:
                if event.key == pygame.K_LEFT:
                    scroll_left = True
                elif event.key == pygame.K_RIGHT:
                    scroll_right = True
                elif event.key == pygame.K_UP:
                    scroll_up = True
                elif event.key == pygame.K_DOWN:
                    scroll_down = True

            # file selector mode
            elif mode > 0:
                if event.key == pygame.K_LEFT and selector > 0:
                    selector -= 1
                elif event.key == pygame.K_RIGHT and selector < 3:
                    selector += 1
                # region selector
                if selector == 0:
                    if event.key == pygame.K_UP and region < 3:
                        region += 1
                    elif event.key == pygame.K_DOWN and region > 0:
                        region -= 1
                # subregion selector
                elif selector == 1:
                    if event.key == pygame.K_UP:
                        sub += 1
                    elif event.key == pygame.K_DOWN and sub > 0:
                        sub -= 1
                # row selector
                elif selector == 2:
                    if event.key == pygame.K_UP:
                        num_x += 1
                    elif event.key == pygame.K_DOWN and num_x > 0:
                        num_x -= 1
                # column selector
                elif selector == 3:
                    if event.key == pygame.K_UP:
                        num_y += 1
                    elif event.key == pygame.K_DOWN and num_y > 0:
                        num_y -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False

    # test_hit = draw_text2("SPACE", font, (0, 0, 0), 10, 40, True, 70, test_hit)
    pygame.display.update()
    # print(save, timer, test_hit)
    # print(f"Rows: {ROWS}  World Y: {len(world_grid)}  Cols: {COLS}  World X: {len(world_grid[0])}  Mode: {mode}")

pygame.quit()

