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

class CatPlayer():
    """ Represents the game state of our Nyan Cat clone """
    def __init__(self, width, height):
        """ Initialize the player """
        self.width = width
        self.height = height
        self.cat = Cat(0,100)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.cat.update(delta_t)

class Cat():
    """ Represents the player in the game (the Nyan Cat) """
    def __init__(self,pos_x,pos_y):
        """ Initialize a Nyan Cat at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 50
        self.vel_y = 0
        # TODO: don't depend on relative path
        self.image = pygame.image.load('nyan_cat.png')
        self.image.set_colorkey((255,255,255))

    def draw(self, screen):
        """ get the drawables that makeup the Nyan Cat Player """
        screen.blit(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))

    def update(self, delta_t):
        self.pos_x += self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t

class NyanView():
    def __init__(self, model, width, height):
        """ Initialize the view for Nyan Cat.  The input model
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
        self.model.cat.draw(self.screen)
        pygame.display.update()

class Wall():
    def __init__(self, model, width, height): 
        self.screen = pygame.display.set_mode((width, height))
        self.model = model

    def draw(self): 
        pygame.draw.rect(self.screen, (255,20,147), (0,0,640,20),0)
        pygame.draw.rect(self.screen, (255,20,147), (0,460,640,20),0)
        pygame.display.update()

class NyanCat():
    """ The main Nyan Cat class """

    def __init__(self):
        """ Initialize the Nyan Cat game.  Use NyanCat.run to
            start the game """
        self.model = CatPlayer(640, 480)
        self.view = NyanView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)
        self.wall = Wall(self.model, 640, 480)
        # we will code the controller later

    def run(self):
        """ the main runloop... loop until death """
        last_update = time.time()
        while True:
            self.wall.draw()
            self.view.draw()
            delta_t = time.time() - last_update
            self.model.update(delta_t)
            self.controller.process_events()
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

    def space_pressed(self):
        pass

if __name__ == '__main__':
    cat = NyanCat()
    cat.run()