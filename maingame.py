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
        self.catplayer = Cat(self.width/3,self.height/2)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.catplayer.update(delta_t)

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
       
        for circle in self.model.circles:
            pygame.draw.circle(self.screen, circle.color, (int(circle.pos_x),int(circle.pos_y)), 15, 0)

        self.model.cat.catplayer.draw(self.screen)

class Circle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.pos_x = width
        self.pos_y = random.randint(0,height)
        self.vel_y = 0
        self.vel_x = 50
        rand_color = random.randint(0,3)
        color_converter = [(144,245,0),(7,185,152),(192,16,191),(255,230,59)]
        self.color = color_converter[rand_color]

    def update(self, delta_t):
        self.pos_x -= self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t

class Model():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cat = CatPlayer(self.width,self.height)
        self.circles = []
        self.notPressed = True

    def update(self, delta_t):
        self.cat.update(delta_t)
        for circle in self.circles:
            circle.update(delta_t)
        make_circle = random.randint(0,2000)
        if make_circle == 2000 and self.notPressed:
            self.circles.append(Circle(self.width, self.height))

    def switchMode(self):
        for circle in self.circles:
            circle.vel_x = 0
        #stop drawing circles

    def returnMode(self):
        for circle in self.circles:
            circle.vel_x = 50
        #start drawing circles


################################################################################

class NyanCat():
    """ The main Nyan Cat class """

    def __init__(self):
        """ Initialize the Nyan Cat game.  Use NyanCat.run to
            start the game """
        self.width = 1000
        self.height = 480
        self.model = Model(self.width, self.height)
        self.view = NyanView(self.model, self.width, self.height)
        self.controller = PygameKeyboardController(self.model)

    def run(self):
        """ the main runloop... loop until death """
        last_update = time.time()

        while True:
            self.view.draw()
            delta_t = time.time() - last_update
            pygame.display.update()
            self.model.update(delta_t)
            self.controller.process_events()
            last_update = time.time()

################################################################################

class PygameKeyboardController():
    def __init__(self, model):
        self.model = model

    def process_events(self):
        pygame.event.pump()
        if (pygame.mouse.get_pressed()[0]):
            self.model.switchMode()
            self.model.notPressed = False
        else:
            self.model.returnMode()
            self.model.notPressed = True


if __name__ == '__main__':
    game = NyanCat()
    game.run()