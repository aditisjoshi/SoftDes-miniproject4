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

    def move_circle(self,circ_dist,x_diff,status):
        """ update the cat's position when you've clicked """
        # finding theta
        while not status:
            theta = acos(x_diff/circ_dist)
            # print x_diff
            # print circ_dist
            # print theta
            angular_vel = 10
            linear_vel = angular_vel * circ_dist
            vel_x = linear_vel * cos(theta)
            vel_y = linear_vel * sin(theta)
            velocity = (vel_x, vel_y)
            # print velocity
            return velocity

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

    def find_closest(self,circles,center_cat,screen):
        """ finding the circle closest to the cat """
        dist_dict = {}
        for circle in circles:
            dist = sqrt(fabs((center_cat[0]-self.pos_x)**2 + (center_cat[1]-self.pos_y)**2))
            dist_dict[circle] = dist
        # find the smallest distance from the cat
        closest_circle = min(dist_dict, key=dist_dict.get)
        x_diff = fabs(center_cat[0] - closest_circle.pos_x)

        # draw a line from the cat to the closest circle
        pygame.draw.line(screen, closest_circle.color, center_cat, (closest_circle.pos_x,closest_circle.pos_y),2)

        return (dist_dict[closest_circle],x_diff)

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

    def update(self, delta_t, vel_x, vel_y):
        """ updates the state of the cat clone and of the circles """
        self.cat.update(delta_t, 0, 0)
        for circle in self.allcircles:
            circle.update(delta_t)
        make_circle = random.randint(0,1000)
        if make_circle == 1000 and self.notPressed:
            self.allcircles.append(Circle(self.width, self.height))

        circle_collision = self.cat.playerrepresentation.collides_with(self.allcircles)
        if len(circle_collision) != 0:
            print 'BANG circle!'

        ### Check for collisions of cat into any circle or inner walls
        if self.notPressed:
            if (self.cat.playerrepresentation.pos_y <= self.walls.wall1_inner_y_pos):
                print 'BANG WALL1'
            if (self.cat.playerrepresentation.pos_y >= self.walls.wall2_inner_y_pos-self.cat.playerrepresentation.img_height):
                print 'BANG Wall2'

        ### Creates the rectangles behind the circles
        for c in self.allcircles:
            self.screen.blit(c.circ, c.rect)

        self.screen.blit(self.cat.playerrepresentation.poptart, self.cat.playerrepresentation.rect)

    def switchMode(self,delta_t):
        """what it does when you hold the mouse down"""
        cat_position = [self.cat.playerrepresentation.pos_x, self.cat.playerrepresentation.pos_y]
        center_cat = [cat_position[0]+self.cat.playerrepresentation.img_width/2, cat_position[1]+self.cat.playerrepresentation.img_height/2]
        # stops the circles from moving
        print self.cat.playerrepresentation.vel_x
        if len(self.allcircles) > 0:
            for circle in self.allcircles:
                circle.vel_x = 0
            # calculate the distances between the circle and the cat
            (circ_dist, x_diff) = self.circles.find_closest(self.allcircles,center_cat, self.screen)

            # calculate the path and move the cat around the circle
            (vel_x, vel_y) = self.cat.playerrepresentation.move_circle(circ_dist,x_diff,self.notPressed)

            self.cat.playerrepresentation.update(delta_t,vel_x,vel_y)

    def returnMode(self):
        """returning back to state after mouse down"""
        # makes the circles move again
        for circle in self.allcircles:
            circle.vel_x = 50
        #start drawing circles

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
            self.controller.process_events()
            pygame.display.update()
            last_update = time.time()
            pygame.display.update()
            if self.model.notPressed:
                self.model.update(delta_t, 0, 0)
            else:
                self.model.switchMode(delta_t)
                pygame.display.update()


################################################################################

class PygameKeyboardController():
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