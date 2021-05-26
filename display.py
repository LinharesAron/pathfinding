import pygame
import math
from random import randrange

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)

    def __mul__(self, f):
        return Point( self.x * f, self.y * f)

    def __truediv__ (self, f):
        return Point( self.x / f, self.y /f)

    @property
    def sqrt_magnetude(self):
        return float(self.x * self.x + self.y * self.y)

    @property
    def magnetude(self):
        return float(math.sqrt(self.x * self.x + self.y * self.y))

    def heading(self, target):
        return target - self

    def distance_to(self, target):
        return self.heading(target).magnetude

    def direction_to(self, target):
        heading = self.heading(target)
        return heading / heading.magnetude

    def dot(self, to):
        return self.x * to.x + self.y * to.y

    def angle(self, to):
        denominator = math.sqrt(self.sqrt_magnetude * to.sqrt_magnetude)
        if denominator < k_epsilon_normal_sqrt:
            return 0
        
        dot = min(1, max(self.dot(to) / denominator, -1))
        return math.acos(dot)

class Window:
    def __init__(self, width, height, title, grid_size = 5):
        self.width, self.height = width, height
        pygame.init()

        self.surface = pygame.display.set_mode((width, height))

        pygame.display.set_caption(title)
        background_colour = (255,255,255)
        self.surface.fill(background_colour)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Ariel', 35)

        self.running = True
        self.diameter = self.width / grid_size
        self.radius = self.diameter / 2

    def draw_grid(self):
        width_cell, height_cell = (math.ceil(self.width/self.diameter), math.ceil(self.height/self.diameter))
        self.grid = [[0 for _ in range(width_cell)] for _ in range(height_cell)]

        for x in range(width_cell):
            for y in range(height_cell):
                self.draw_square(Point(x, y))

    def center_square(self, point):
        return self.radius + (point.x * self.diameter), self.radius + (point.y * self.diameter)

    def draw_circle(self, point, colour=(0,0,255), thickness=0):
        x, y = self.center_square(point)
        pygame.draw.circle(self.surface, colour, (x, y), self.radius, thickness)
    
    def draw_square(self, point, colour=(0,0,0), thickness=1):
        pygame.draw.rect(self.surface, colour, (point.x * self.diameter, point.y * self.diameter, self.diameter, self.diameter), thickness)

    def point_on_circle(self, radius, diameter, point, direction):
        angle = forward.angle(direction)
        
        difx = radius * math.sin(angle)
        dify = radius * math.cos(angle)

        if direction.x < 0:
            difx *= -1

        return radius + (point.x * diameter) + difx, radius + (point.y * diameter) + dify

    def draw_line(self, point_origin, point_destiny, colour=(0,0,0), thickness=1):
        o_x, o_y = self.point_on_circle(self.radius, self.diameter, point_origin, point_origin.direction_to(point_destiny))
        d_x, d_y = self.point_on_circle(self.radius, self.diameter, point_destiny, point_destiny.direction_to(point_origin))

        pygame.draw.line(self.surface, colour, 
                    (o_x, o_y), 
                    (d_x, d_y), thickness)
    
    def draw_letter(self, point, letter, thickness=10, colour=(255,255,255)):
        l = self.font.render(letter, thickness, colour)
        x, y = self.center_square(point)
        self.surface.blit(l, (x, y))

    def run(self, func_action):
        while self.running:
            for event in pygame.event.get():
                func_action(event)
            
            pygame.display.flip()
            self.clock.tick(60)

    def stop(self):
        self.running = False

    def is_quit(self, event):
        return event == pygame.QUIT
    
k_epsilon_normal_sqrt = 1e-15
forward = Point(0, 1)   