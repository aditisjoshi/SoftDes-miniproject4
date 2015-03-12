""" 
Aditi and Jess
SoftDes Mini-Project 4
Making a side-scrolling game with nyan cat based on One More Line
"""

import pygame
from pygame.locals import *
import random
import time
from math import sqrt,fabs, cos, sin, acos


class DrawableSurface(object):
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

class CatPlayer(object):
    """ Represents the game state of our Nyan Cat clone """
    def __init__(self, width, height):
        """ Initialize the player """
        self.width = width
        self.height = height
        self.playerrepresentation = Cat(self.width/3,self.height/2)

    def update(self, delta_t, vel_x, vel_y):
        """ Updates the model and its constituent parts """
        self.playerrepresentation.update(delta_t, vel_x, vel_y)

################################################################################ HERE STARTS ALL THE OBJECTS TO BE DRAWN (cat, walls, circles)

class Cat(pygame.sprite.Sprite):
    """ Represents the player in the game (the Nyan Cat) """
    def __init__(self,pos_x,pos_y):
        """ Initialize a Nyan Cat at the specified position
            pos_x, pos_y """
        self.img_width = 71
        self.img_height = 44.5
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cat_position = [pos_x,pos_y]
        self.center_cat = [self.cat_position[0]+self.img_width/2, self.cat_position[1]+self.img_height/2]
        # TODO: don't depend on relative path
        self.image = pygame.image.load('nyan_cat.png')
        self.image.set_colorkey((255,255,255)) 
        self.poptart = pygame.Surface((self.img_width, self.img_height))
        self.mask = pygame.mask.from_surface(self.poptart)
        self.vel_x = 0
        self.vel_y = 0

    @property
    def rect(self):
        """Get the cat's position, width, and height, as a pygame.Rect."""
        return Rect(self.pos_x, self.pos_y, self.img_width, self.img_height)

    def draw(self, screen):
        """ get the drawables that makeup the Nyan Cat Player """
        screen.blit(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))

    def update(self, delta_t, vel_x, vel_y): 
        """Updates the players representation (the Nyan Cat)'s position """
        self.pos_x += vel_x*delta_t
        self.pos_y += vel_y*delta_t

    def move_circle(self,x_diff,y_diff,circ_dist):
        """ update the cat's velocity when the mouse is clicked so that a
        circular path can be followed"""
        scalar = 2000
        vel_x = y_diff/circ_dist * scalar
        vel_y = -x_diff/circ_dist * scalar
        return (vel_x, vel_y)

    def collides_with(self, circle):
        """Get whether the cat collides with a circle in this Circle class.
        Arguments:
        cat: The cat that should be tested for collision with this circle.
        """
        return pygame.sprite.spritecollide(self, circle, False)

class Walls(object):
    """ creating a class for the walls"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Define the wall position
        self.wall_color = (255,20,147)
        self.wall_thick = 20
        self.wall_margin = 50
        self.wall1_outer_y_pos = self.wall_margin
        self.wall1_inner_y_pos = self.wall_margin+self.wall_thick
        self.wall2_outer_y_pos = self.height-self.wall_margin-self.wall_thick
        self.wall2_inner_y_pos = self.height-self.wall_margin

    def draw(self, screen):
        """Draw the walls of the game"""
        # Draw wall1 (top)
        pygame.draw.rect(screen, self.wall_color, (0,self.wall1_outer_y_pos,self.width,self.wall_thick),0)
        # Draw wall2 (bottom)
        pygame.draw.rect(screen, self.wall_color, (0,self.wall2_inner_y_pos,self.width,self.wall_thick),0)

class Circle(pygame.sprite.Sprite):
    """ the Cat is one sprite, the Circles are the second sprite"""
    def __init__(self, width, height):
        """ Intialize the view for the circles. The color is randomly generated and the y position is random (inside the walls)
            this also takes in the wall position/color but the model draws them """
        self.width = width
        self.height = height
        self.radius = 15
        
        # taking in wall information so that they know where to draw the circles
        self.walls = Walls(self.width, self.height)
        self.pos_x = self.width
        lower_bound = self.walls.wall1_inner_y_pos+(self.radius*2)
        upper_bound = self.walls.wall2_inner_y_pos-(self.radius*2)
        self.pos_y = random.randint(lower_bound, upper_bound)
        self.vel_y = 0
        self.vel_x = 50
        rand_color = random.randint(0,3)
        color_converter = [(144,245,0),(7,185,152),(192,16,191),(255,230,59)]
        self.color = color_converter[rand_color]

        # for collision detection
        self.circ = pygame.Surface((self.radius, self.radius))
        self.mask = pygame.mask.from_surface(self.circ)

    @property
    def rect(self):
        """Get the Rect which contains this circle."""
        return Rect(self.pos_x, self.pos_y, self.radius, self.radius)

    def draw(self, screen):
        """ drawing the circles """
        pygame.draw.circle(screen, self.color, (int(self.pos_x),int(self.pos_y)), self.radius, 0)

    def update(self, delta_t):
        """updates the circles position according to time"""
        self.pos_x -= 10*self.vel_x*delta_t
        self.pos_y += 10*self.vel_y*delta_t

################################################################################ HERE STARTS THE MODEL

class Model(object):
    """the model of the game (takes in the two sprites - the circles and the cat)"""
    def __init__(self, width, height):
        """ititalizaing the model with bot the circles (and empty list) and the cat as well as drawing the walls"""
        self.width = width
        self.height = height
        self.cat = CatPlayer(self.width,self.height)
        self.allcircles = []
        self.circles = Circle(self.width,self.height)
        self.walls = Walls(self.width, self.height)
        self.screen = pygame.display.set_mode((width, height))
        self.notPressed = True
        self.run = True
        self.pushnumber = 0

    def update(self, delta_t, vel_x, vel_y):
        """ updates the state of the cat clone and of the circles """
        self.cat.update(delta_t, 0, 0)
        for circle in self.allcircles:
            circle.update(delta_t)
        make_circle = random.randint(0,500)
        if make_circle == 500 and self.notPressed:
            self.allcircles.append(Circle(self.width, self.height))

        circle_collision = self.cat.playerrepresentation.collides_with(self.allcircles)
        if len(circle_collision) != 0:
            print 'loss'
            self.run = False

        # Check for collisions of cat into any circle or inner walls
        if self.notPressed:
            if (self.cat.playerrepresentation.pos_y <= self.walls.wall1_inner_y_pos):
                print 'loss'
                self.run = False
            if (self.cat.playerrepresentation.pos_y >= self.walls.wall2_inner_y_pos-self.cat.playerrepresentation.img_height):
                print 'loss'
                self.run = False

        ### Creates the rectangles behind the circles
        for c in self.allcircles:
            self.screen.blit(c.circ, c.rect)

        self.screen.blit(self.cat.playerrepresentation.poptart, self.cat.playerrepresentation.rect)

    def switchMode(self,delta_t, counter):
        """what it does when you hold the mouse down"""
        cat_position = [self.cat.playerrepresentation.pos_x, self.cat.playerrepresentation.pos_y]
        center_cat = [cat_position[0]+self.cat.playerrepresentation.img_width/2, cat_position[1]+self.cat.playerrepresentation.img_height/2]
        
        # stops the circles from moving
        if len(self.allcircles) > 0:
            for circle in self.allcircles:
                circle.vel_x = 0
            # calculates the distance between the circle and the cat and the difference between their x pos.
            dist_dict = {}
            for circle in self.allcircles:
                dist = sqrt((center_cat[0]-circle.pos_x)**2 + (center_cat[1]-circle.pos_y)**2)
                dist_dict[circle] = dist
            
            # find the smallest distance from the cat
            closest_circle = min(dist_dict, key=dist_dict.get)

            x_diff = (self.cat.playerrepresentation.center_cat[0] - closest_circle.pos_x)
            y_diff = (self.cat.playerrepresentation.center_cat[1] - closest_circle.pos_y)
            circ_dist = dist_dict[closest_circle]

            # increase counter to jump to next function (aroundCircle)
            counter += 1
            return closest_circle, circ_dist, counter
        
        #the mouse is clicked when there are no circles
        else:
            return 0,0,0

    def aroundCircle(self, nearest_circ, diag_dist, delta_t, screen):
        """ move around the closest circle """
        # draw a line from the cat to the closest circle
        pygame.draw.line(screen, nearest_circ.color, (self.cat.playerrepresentation.pos_x + self.cat.playerrepresentation.img_width/2, self.cat.playerrepresentation.pos_y + self.cat.playerrepresentation.img_height/2), (nearest_circ.pos_x,nearest_circ.pos_y),2)
        x_diff = (self.cat.playerrepresentation.pos_x + self.cat.playerrepresentation.img_width/2 - nearest_circ.pos_x)
        y_diff = (self.cat.playerrepresentation.pos_y + self.cat.playerrepresentation.img_height/2 - nearest_circ.pos_y)
        circ_dist = diag_dist
        (vel_x, vel_y) = self.cat.playerrepresentation.move_circle(x_diff,y_diff,circ_dist)
        self.cat.playerrepresentation.update(delta_t,vel_x,vel_y)

    def returnMode(self):
        """returning back to state after mouse down"""
        # makes the circles move again
        for circle in self.allcircles:
            circle.vel_x = 50

        self.pushnumber = 0

################################################################################ HERE STARTS THE VIEW

class NyanView():
    """the view of the game"""
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

        #drawing the screen
        self.screen.fill((0,51,102))

        #drawing the walls
        self.model.walls.draw(self.screen)

        #drawing the cat
        self.model.cat.playerrepresentation.draw(self.screen)
       
        #drawing the circles
        for circle in self.model.allcircles:
            circle.draw(self.screen)

################################################################################ GAME ON!

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

        while self.model.run:
            self.view.draw()
            delta_t = time.time() - last_update
            self.controller.process_events()
            pygame.display.update()
            last_update = time.time()
            pygame.display.update()
            if self.model.notPressed:
                self.model.update(delta_t, 0, 0)
            else:
                if self.model.pushnumber == 0:
                    nearest_circ, diag_dist, self.model.pushnumber = self.model.switchMode(delta_t,self.model.pushnumber)
                # when the mouse is continued to press...
                elif self.model.pushnumber > 0:
                    self.model.aroundCircle(nearest_circ, diag_dist, delta_t, self.model.screen)
                
                pygame.display.update()

################################################################################

class PygameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def process_events(self):
        pygame.event.pump()
        if (pygame.mouse.get_pressed()[0]):
            self.model.notPressed = False
        else:
            self.model.returnMode()
            self.model.notPressed = True


if __name__ == '__main__':
    game = NyanCat()
    game.run()