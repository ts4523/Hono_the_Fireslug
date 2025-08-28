import pygame
import time
import button
import Assets.Files.item_lists

# fonts
pygame.font.init()
TITLE = pygame.font.SysFont("timesnewroman", 30)
H1 = pygame.font.SysFont("timesnewroman", 20)
H2 = pygame.font.SysFont("timesnewroman", 15)
NORM = pygame.font.SysFont("timesnewroman", 12)
SUB = pygame.font.SysFont("timesnewroman", 10)

# constants
WIDTH, HEIGHT = 800, 600
INVTRY_W, INVTRY_H = 400, 340
INVTRY_X, INVTRY_Y = WIDTH - 450, 80
BUTTON_W = 80
BUTTON_H = 40
stall_width = 200
stall_height = 80

# global variables
invtry_box_w = INVTRY_W / 4
invtry_box_mar = 4
invtry_box_border = 4

# create screens
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fade_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
invtry_screen = pygame.Surface((INVTRY_W, INVTRY_H), pygame.SRCALPHA)
shop_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# create the main screen caption and background image
pygame.display.set_caption("Market")
BG = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/bg_market.jpg"), (WIDTH, HEIGHT))

# create images
Wood_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/wood_pix.png")
Meat_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/meat_pix.png")
Grain_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Icons/grain_pix.png")

# add images to dictionary
img_dict = {"Wood": Wood_img,
            "Meat": Meat_img,
            "Grain": Grain_img}

# create button images
resume_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/resume_btn.png").convert_alpha()
options_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/options_btn.png").convert_alpha()
quit_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/quit_btn.png").convert_alpha()
settings_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/settings_btn.png").convert_alpha()
controls_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/controls_btn.png").convert_alpha()
back_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/back_btn.png").convert_alpha()
exit_img = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/exit_btn.png"), (20, 15))
buy_img = pygame.transform.scale(pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/buy.png"), (BUTTON_W, BUTTON_H))
shop_img = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/shop_btn.png").convert_alpha()
left_arrow_gold = pygame.image.load("Hono_the_Fireslug/Assets/Images/Buttons/game_arrow_gold_left.png").convert_alpha()
right_arrow_gold = pygame.image.load(
    "Hono_the_Fireslug/Assets/Images/Buttons/game_arrow_gold_right.png").convert_alpha()


# create buttons
resume_button = button.Button(WIDTH / 2 - 102, 100, resume_img, 1)
options_button = button.Button(WIDTH / 2 - 102, 190, options_img, 1)
quit_button = button.Button(WIDTH / 2 - 102, 280, quit_img, 1)
settings_button = button.Button(WIDTH / 2 - 102, 200, settings_img, 1)
controls_button = button.Button(WIDTH / 2 - 102, 290, controls_img, 1)
back_button = button.Button(WIDTH / 2 - 102, 380, back_img, 1)
exit_button = button.Button((20 + stall_width - 20 - 5), (80 + 5), exit_img, 1)
buy_button = button.Button((WIDTH / 2 - 100), (HEIGHT - 80 - BUTTON_H / 2), buy_img, 1)
shop_button = button.Button(100, HEIGHT - 100, shop_img, 1)

# draw selector arrows
left_btn_gold = button.Button(20 + stall_width * (3 / 4) - 20 - 20, 80 + stall_height - 35, left_arrow_gold, 1)
right_btn_gold = button.Button(20 + stall_width * (3 / 4) + 20, 80 + stall_height - 35, right_arrow_gold, 1)


def render_txt(name, txt_type, color):
    txt = txt_type.render(f"{name}", 1, color)
    txt_width = txt.get_width()
    txt_height = txt.get_height()
    return name, txt, txt_width, txt_height


def draw_txt(txt, font, color, x, y):
    img = font.render(f"{txt}", 1, color)
    screen.blit(img, (x, y))


def draw_shop(first, qty):
    items, first, qty = Assets.Files.item_lists.get_items_test(first, qty)
    x = 20
    y = 80
    yes_shop = True

    # create each market stall
    for line in items:
        # draw the stall box
        pygame.draw.rect(shop_screen, [255, 255, 255, 180], [x, y, stall_width, stall_height], 0, 8)
        color = "black"
        '''# draw selector arrows
        left_btn = button.Button(x + stall_width * (3 / 4) - 20 - 20, stall_y + stall_height - 35,
                                 20, 30, left_arrow_gold)
        right_btn = button.Button(x + stall_width * (3 / 4) + 20, stall_y + stall_height - 35,
                                  20, 30, right_arrow_gold)'''
        left_btn = left_btn_gold
        right_btn = right_btn_gold

        # render list items as text
        name, txt, txt_width, txt_height = render_txt(line[0], H2, color)
        # it the item matches an image tag in the image dictionary, draw the image
        for tag, img in img_dict.items():
            if name == tag:
                shop_screen.blit(pygame.transform.scale(img, (stall_height, stall_height)),
                                 (x + stall_width / 4 - stall_height / 2, y))
        shop_screen.blit(txt, (x + stall_width * (3 / 4) - txt_width / 2, y + 5))
        # price text
        name, txt, txt_width, txt_height = render_txt(line[1], SUB, color)
        shop_screen.blit(txt, (x + BUTTON_W / 2 - txt_width / 2,
                               y + BUTTON_H / 2 - txt_height / 2))
        # quantity text
        name, txt, txt_width, txt_height = render_txt(line[2], NORM, color)
        shop_screen.blit(txt, (x + stall_width / 4 + stall_height / 2 - 10,
                               y + stall_height - txt_height - 15))

        if left_btn.draw(shop_screen):
            print('left')
        if right_btn.draw(shop_screen):
            print('right')
        if exit_button.draw(shop_screen):
            yes_shop = False

        y += 84

    return first, qty, yes_shop


def draw_invtry():
    # color inventory screen
    invtry_screen.fill([0, 0, 0, 150])

    # create Inventory title and draw in top center of inventory screen
    invtry_title = H1.render("INVENTORY", 1, "white")
    invtry_title_width = invtry_title.get_width()
    invtry_title_height = invtry_title.get_height()
    invtry_screen.blit(invtry_title, (INVTRY_W / 2 - invtry_title_width / 2, 5))

    # draw inventory item boxes on inventory screen below title
    # in 4x4 table with 4pxl width borders
    box_col = 0
    box_row = 0
    while box_row * invtry_box_w + invtry_box_w < INVTRY_H - invtry_title_height + 10:
        while box_col * invtry_box_w < INVTRY_W:
            pygame.draw.rect(invtry_screen, "lightgrey", [4 + box_col * invtry_box_w,
                                                          invtry_title_height + 10 + box_row * invtry_box_w,
                                                          invtry_box_w - 2 * invtry_box_mar,
                                                          invtry_box_w - 2 * invtry_box_mar], invtry_box_border, 8)
            box_col += 1
        box_row += 1
        box_col = 0


def draw(run, elapsed_time, first, qty, game_paused, yes_shop):
    # draw screens
    # screen.blit(BG, (0, 0))
    screen.blit(fade_screen, (0, 0))
    screen.blit(shop_screen, (0, 0))
    screen.blit(invtry_screen, (INVTRY_X, INVTRY_Y))

    # time_text = H1.render(f"Time: {round(elapsed_time)}s", 1, "white")
    # screen.blit(time_text, (10, 10))

    # check if game is paused
    if game_paused:
        if shop_button.draw(screen):
            game_paused = False
        name, txt, txt_width, txt_height = render_txt("Game is paused.", TITLE, "white")
        screen.blit(txt, (WIDTH / 2, HEIGHT / 2), )

    else:
        render_txt("Press Space to pause.", TITLE, "white")
        
    if buy_button.draw(screen):
        print('buy')
    if shop_button.draw(screen):
        first, qty, yes_shop = draw_shop(first, qty)
        draw_invtry()

    pygame.display.update()
    return run, first, qty


def market():
    # local variables
    game_paused = False
    menu_state = "main"
    run = True
    first = False
    qty = 0

    # game clock
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    while run:
        # clock.tick(60)
        # elapsed_time = time.time() - start_time

        # draw screens
        # screen.blit(BG, (0, 0))
        screen.fill("teal")
        screen.blit(fade_screen, (0, 0))
        screen.blit(shop_screen, (0, 0))
        screen.blit(invtry_screen, (INVTRY_X, INVTRY_Y))

        # time_text = H1.render(f"Time: {round(elapsed_time)}s", 1, "white")
        # screen.blit(time_text, (10, 10))

        # check if game is paused
        if game_paused:
            # check menu state
            if menu_state == "main":
                if resume_button.draw(screen):
                    game_paused = False
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    run = False
            elif menu_state == "options":
                if settings_button.draw(screen):
                    pass
                if controls_button.draw(screen):
                    pass
                if back_button.draw(screen):
                    menu_state = "main"

        if shop_button.draw(screen):
            menu_state = "market"
        else:
            draw_txt("Press SPACE to pause.", TITLE, "white", 450, 100)

            if buy_button.draw(screen):
                print('buy')
            if shop_button.draw(screen):
                first, qty, yes_shop = draw_shop(first, qty)
                draw_invtry()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False
                break

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    market()
