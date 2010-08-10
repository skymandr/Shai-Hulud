#! /usr/bin/env python

import pygame, random

# to implement:
# people

class Worm:
    """ A Worm. """

# Dictionary of allowed directions:
    _compass = {
        pygame.K_UP: (0, -1),
        pygame.K_w:  (0, -1),
        pygame.K_k:  (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_x:    (0, 1),
        pygame.K_j:    (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_a:    (-1, 0),
        pygame.K_h:    (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_d:     (1, 0),
        pygame.K_l:     (1, 0),
        pygame.K_q:     (-1, -1),
        pygame.K_e:     (1, -1),
        pygame.K_c:     (1, 1),
        pygame.K_z:     (-1, 1)
    }

    def __init__(self, surface, x, y, length, worm_colour=(126,84,0), \
                 sand_colour=(210,168,0), dude_colour=(0,0,0), \
                 spice_colour=(168,126,0)):
        self.surface = surface
        self.x, self.y = x, y
        self.length = length
        self.dir_x, self.dir_y = (0, -1)
        self.body = []
        self.crashed = False
        self.worm_colour = worm_colour
        self.sand_colour = sand_colour
        self.dude_colour = dude_colour
        self.spice_colour = spice_colour
        self.spice_eaten = 0
        self.dudes_eaten = 0

    def key_event(self, event):
        """ Handle key events that affect the Worm """
        try:
            self.dir_x, self.dir_y = Worm._compass[event.key]
        except KeyError:
            pass
   
    def move(self):
        """ Move the Worm! """ 
        w, h = self.surface.get_size()
        self.x += self.dir_x
        self.y += self.dir_y
        self.x = self.x % w
        self.y = self.y % h

        r, g, b, a = self.surface.get_at((self.x, self.y))
        if (r, g, b) == self.sand_colour:
            pass
        elif (r, g, b) == self.spice_colour:
            self.spice_eaten += 1
        elif (r, g, b) == self.dude_colour:
            self.dudes_eaten += 1
        else:
            self.crashed = True

        self.body.insert(0, (self.x, self.y))

        if len(self.body) > self.length:
            self.surface.set_at(self.body[-1], self.sand_colour)
            self.body.pop()

    def draw(self):
        """" Draw Worm. """
        for x, y in self.body:
            self.surface.set_at((x, y), self.worm_colour)

class Dude:
    """ A Dude. It should do a random walk."""
    
    collected = 0    

    def __init__(self, surface, x=-1, y=-1, dude_colour=(0, 0, 0), worm_colour=(126, 84, 0), \
                 spice_colour=(168, 126, 0), sand_colour=(210, 168, 0)):    
        self.dude_colour = dude_colour
        self.worm_colour = worm_colour
        self.spice_colour = spice_colour
        self.sand_colour = sand_colour
        self.surface = surface
        w, h = self.surface.get_size()
        if x < 0 or x >= w or y < 0 or y >= h:
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            r, g, b, a = self.surface.get_at((x, y))
            while (r, g, b) == self.worm_colour:
                x = random.randint(0, w-1)
                y = random.randint(0, h-1)
                r, g, b, a = self.surface.get_at((x, y))
        self.x = x
        self.y = y
        self.alive = True

    def move(self): 
        """ Move the Dude. """
        if not self.alive:
             return
        r, g, b, a = self.surface.get_at((self.x, self.y))
        if (r, g, b) == self.worm_colour:
            self.alive = False
            return
        self.surface.set_at((self.x, self.y), self.sand_colour)
        w, h = self.surface.get_size()
        x_dir = random.randint(-1, 1)
        y_dir = random.randint(-1, 1)
        new_x = (self.x + x_dir) % w
        new_y = (self.y + y_dir) % h
        r, g, b, a = self.surface.get_at((new_x, new_y))
        if (r,g,b) != self.worm_colour and (r,g,b) != self.dude_colour:
            self.x = new_x
            self.y = new_y
        if (r, g, b) == self.spice_colour:
            Dude.collected += 1
        
    def draw(self):
        """ Draws the Dude if alive. """
        if self.alive:
            self.surface.set_at((self.x, self.y), self.dude_colour)

class Spice:
    """ The Worm is the Spice! Spice blooms. """

    def __init__(self, surface, spice_colour=(168, 126, 0), sand_colour=(210, 168, 0)):
        self.spice_colour = spice_colour
        self.sand_colour = sand_colour
        self.surface = surface

    def spice_bloom(self, x=-1, y=-1):
        """ Make the Spice bloom. """
        w, h = self.surface.get_size()
        if x < 0 or x >= w or y < 0 or y >= h:
            x = random.randint(1, w-2)
            y = random.randint(1, h-2)
            r, g, b, a = self.surface.get_at((x, y))
            while (r, g, b) != self.sand_colour and (r, g, b) != self.spice_colour:
                x = random.randint(1, w-2)
                y = random.randint(1, h-2)
                r, g, b, a = self.surface.get_at((x, y))
            if (r, g, b) == self.sand_colour:
                self.surface.set_at((x, y), self.spice_colour)
            else:
                if self.surface.get_at((x+1, y)) == self.sand_colour:
                    self.surface.set_at((x+1, y), self.spice_colour)
                if self.surface.get_at((x+1, y+1)) == self.sand_colour:
                    self.surface.set_at((x+1, y+1), self.spice_colour)
                if self.surface.get_at((x, y+1)) == self.sand_colour:
                    self.surface.set_at((x, y+1), self.spice_colour)
                if self.surface.get_at((x-1, y+1)) == self.sand_colour:
                    self.surface.set_at((x-1, y+1), self.spice_colour)
                if self.surface.get_at((x-1, y)) == self.sand_colour:
                    self.surface.set_at((x-1, y), self.spice_colour)
                if self.surface.get_at((x-1, y-1)) == self.sand_colour:
                    self.surface.set_at((x-1, y-1), self.spice_colour)
                if self.surface.get_at((x, y-1)) == self.sand_colour:
                    self.surface.set_at((x, y-1), self.spice_colour)
                if self.surface.get_at((x+1, y-1)) == self.sand_colour:
                    self.surface.set_at((x+1, y-1), self.spice_colour)

# Window settings:
width = 640
height = 480

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

# Some colours:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
worm_colour  = (168, 84, 0)
sand_colour  = (210, 168, 0)
dude_colour  = blue
spice_colour = (210, 126, 0) 
rock_colour = (84, 42, 0)

# Make Worm:
w = Worm(screen, width/2, height/2, 64, worm_colour, sand_colour, \
         dude_colour, spice_colour)

# Make spice:
s = Spice(screen, spice_colour, sand_colour)

# Prepare sand and fill with spice:
n_spice = 32768 
p_spice = 0.1
screen.fill(sand_colour)
for n in range(n_spice):
    s.spice_bloom()

# Populate dunes with dudes:
n_dudes = 512
dudes = []
for n in range(n_dudes):
    dudes.insert(0, Dude(screen, -1, -1, dude_colour, worm_colour, \
                         spice_colour, sand_colour))

while running:
    w.draw()
    w.move()
    w.draw()
    for d in dudes:
        d.move()
        d.draw()
    if 1.0*random.randint(0, 1000)/1000. <= p_spice:
        s.spice_bloom()   

    if w.crashed:
        print "Crash!"
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
            print "Quit game."
        elif event.type == pygame.KEYDOWN:
            w.key_event(event)

    pygame.display.flip()
    clock.tick(100)

print "Spice eaten: {0} \nDudes eaten: {1} \nSpice stolen: {2}".format( \
      w.spice_eaten, w.dudes_eaten, Dude.collected)
