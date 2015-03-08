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
        self.cat = Cat(self.width/3,self.height/2)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.cat.update(delta_t)

class Cat(pygame.sprite.Sprite):
    """ Represents the player in the game (the Nyan Cat) """
    def __init__(self,pos_x,pos_y):
        """ Initialize a Nyan Cat at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
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
        self.width = width
        self.height = height

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # Draw the walls of the game
        wall_color = (255,20,147)
        wall_thick = 20
        wall_margin = 50
        # Draw top wall
        pygame.draw.rect(self.screen, wall_color, (0,wall_margin,self.width,wall_thick),0)
        # Draw bottom wall
        pygame.draw.rect(self.screen, wall_color, (0,self.height-wall_margin-wall_thick,self.width,wall_thick),0)
        self.model.cat.draw(self.screen)
        # pygame.display.update()

class Circles():
    def __init__(self, model, width, height):
        self.model = model
        self.screen = pygame.display.set_mode((width, height))
        self.pos_x = random.randint(int(self.model.cat.pos_x),640)
        self.pos_y = random.randint(0,480)
        self.vel_y = 0
        self.vel_x = 50

    def draw(self): 
        color = random.randint(0,3)
        color_converter = [(144,245,0),(7,185,152),(192,16,191),(255,230,59)]
        pygame.draw.circle(self.screen, color_converter[color], (int(self.pos_x),int(self.pos_y)), 15, 0)
        # pygame.display.update()

    def update(self, delta_t):
        self.pos_x -= self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t


################################################################################
class NyanCat():
    """ The main Nyan Cat class """

    def __init__(self):
        """ Initialize the Nyan Cat game.  Use NyanCat.run to
            start the game """
        # fps = 30
        # clock = pygame.time.Clock()
        width = 1000
        height = 480
        self.model = CatPlayer(width, height)
        self.view = NyanView(self.model, width, height)
        self.model = CatPlayer(640, 480)
        self.view = NyanView(self.model, width, height)
        self.circles = Circles(self.model, width, height)
        self.controller = PygameKeyboardController(self.model,self.circles)
        # we will code the controller later

    def run(self):
        """ the main runloop... loop until death """
        last_update = time.time()

        while True:
            self.view.draw()
            self.circles.draw()
            pygame.display.update()
            delta_t = time.time() - last_update
            self.model.update(delta_t)
            self.circles.update(delta_t)
            self.controller.process_events()
            last_update = time.time()
            # clock.tick(fps)

################################################################################

class PygameKeyboardController():
    def __init__(self, model, circles):
        self.model = model
        self.circles = circles

    def process_events(self):
        pygame.event.pump()
        if (pygame.mouse.get_pressed()[0]):
            self.model.cat.vel_x = 0
            self.circles.vel_x = 0
        else:
            self.model.cat.vel_x = 0
            self.circles.vel_x = 50

if __name__ == '__main__':
    cat = NyanCat()
    cat.run()