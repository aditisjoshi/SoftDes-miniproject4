""" 
Aditi and Jess
SoftDes Mini-Project 4
Making a side-scrolling game with nyan cat based on One More Line
"""

import pygame
import random
import time

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """

    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class FlappyModel():
    """ Represents the game state of our Flappy bird clone """
    def __init__(self, width, height):
        """ Initialize the flappy model """
        self.width = width
        self.height = height
        self.bird = Bird(0,100)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.bird.update(delta_t)

class Bird():
    """ Represents the player in the game (the Flappy Bird) """
    def __init__(self,pos_x,pos_y):
        """ Initialize a Flappy bird at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 50
        self.vel_y = 0
        # TODO: don't depend on relative path
        self.image = pygame.image.load('nyan_cat.png')
        self.image.set_colorkey((255,255,255))

    def draw(self, screen):
        """ get the drawables that makeup the Flappy Bird Player """
        screen.blit(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))

    def update(self, delta_t):
        """ update bird due to passage of time """
        self.pos_x += self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t
        self.vel_y += 20*delta_t

    def flap(self):
        self.vel_y -= 5

class FlappyView():
    def __init__(self, model, width, height):
        """ Initialize the view for Flappy Bird.  The input model
            is necessary to find the position of relevant objects
            to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        self.model.bird.draw(self.screen)
        pygame.display.update()

class FlappyBird():
    """ The main Flappy Bird class """

    def __init__(self):
        """ Initialize the flappy bird game.  Use FlappyBird.run to
            start the game """
        self.model = FlappyModel(640, 480)
        self.view = FlappyView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)
        # we will code the controller later

    def run(self):
        """ the main runloop... loop until death """
        last_update = time.time()
        while True:
            self.view.draw()
            self.controller.process_events()
            delta_t = time.time() - last_update
            self.model.update(delta_t)
            last_update = time.time()

class PygameKeyboardController():
    def __init__(self, model):
        self.model = model
        self.space_pressed = False

    def process_events(self):
        pygame.event.pump()
        if not(pygame.key.get_pressed()[pygame.K_SPACE]):
            self.space_pressed = False
        elif not(self.space_pressed):
            self.space_pressed = True
            self.model.bird.flap()

if __name__ == '__main__':
    flappy = FlappyBird()
    flappy.run()