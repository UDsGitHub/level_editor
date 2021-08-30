import pygame
from pygame.locals import *
pygame.init()

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int( width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # check mouseover and clicks
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[1] == 0:
                self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action