import pygame


# button class
class Button:
    def __init__(self, x, y, image, scale):
        self.image = image
        self.image = pygame.transform.scale(image, (self.image.get_width()*scale, self.image.get_height()*scale))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw buttons
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class ColorButton:
    def __init__(self, x, y, width, height, image, color, border):
        self.color = pygame.draw.rect(image, color,
                                      [x - border, y - border, width + 2 * border, height + 2 * border])
        if image != "none":
            self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked cond
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw buttons
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
