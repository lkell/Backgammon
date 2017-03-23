import pygame
import numpy
pygame.font.init()


# Rgb color constants
GREEN = (100, 200, 0)
BROWN = (165,42,42)
WHITE = (255, 255, 255)
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (0, 255, 255)


class Text:
    """Class for displaying and manipulating text."""

    def __init__(self, string, position, size, color = BLACK):

        self.string = string
        self.position = position
        self.size = size
        self.color = color

    def setText(self, string):
        """Sets the string that is displayed to string."""
        self.string = string

    def draw(self, surface):
        """Draws the text to the surface."""
        self.myfont = pygame.font.SysFont('Monospace', self.size)
        self.label = self.myfont.render(self.string, 1, self.color)
        surface.blit(self.label, self.position)

    def resetText(self, string, surface, color = BLACK):
        """Resets the text to display a new string."""
        temp = self.color
        self.color = BLACK
        self.draw(surface)
        self.color = temp
        self.string = string
        self.draw(surface)  


class Rectangle:
    """Class for displaying and manipulating a rectangle."""

    def __init__(self, width, height, uL, color):
        self.width = width
        self.height = height
        self.uL = uL
        self.color = color

    def draw(self, surface):
        """Draws the rectangle to the surface."""
        pygame.draw.rect(surface, self.color,(self.uL[0], self.uL[1], self.width, self.height))
        pygame.draw.rect(surface, BLACK,(self.uL[0], self.uL[1], self.width, self.height), 1)

    def checkClick(self, position):
        """Given the mouse position, checks whether a player has clicked
           on the rectangle."""
        if position[0] > self.uL[0] and position[0] < self.uL[0] + self.width\
           and position[1] > self.uL[1] and position[1] < self.uL[1] + self.height:
            return True
        return False


class Triangle:
    """Class for displaying and manipulating a triangle."""

    def __init__(self, color, pointList, side):
        self.color = color
        self.point1 = pointList[0]
        self.point2 = pointList[1]
        self.point3 = pointList[2]
        self.side = side
        self.borderColor = BLACK
        self.borderWidth = 1

    def setBorder(self, color, width):
        """Sets the border color and width."""
        self.borderColor = color
        self.borderWidth = width

    def draw(self, surface):
        """Draws the triangle to surface."""
        pygame.draw.polygon(surface, self.color,
                            (self.point1, self.point2, self.point3))
        pygame.draw.polygon(surface, self.borderColor,
                            (self.point1, self.point2, self.point3),
                            self.borderWidth)

    def checkClick(self, position):
        """Given the mouse position, checks whether a player has clicked
           on the triangle."""
        if self.side == 'bottom':
            if position[0] > self.point2[0] and position[0] < self.point1[0] and\
               position[1] < self.point1[1] and position[1] > self.point3[1]:
                return True
        else:
            if position[0] < self.point2[0] and position[0] > self.point1[0] and\
               position[1] > self.point1[1] and position[1] < self.point3[1]:
                return True
        return False


class Circle:
    """Class for displaying and manipulating a circle."""

    def __init__(self, color, center, radius):

        self.color = color
        self.center = center
        self.radius = radius

    def draw(self, surface):
        """Draws the circle to the surface."""
        pygame.draw.circle(surface, self.color, self.center, self.radius)
        pygame.draw.circle(surface, BLACK, self.center, self.radius, 1)

    def moveTo(self, center):
        """Moves the circle to be centered at center."""
        self.center = center

    def setFillColor(self, color):
        """Sets the circle's fill color to color."""
        self.color = color

    def checkClick(self, pos):
        """Given the mouse position, checks whether a player has clicked
           on the circle."""
        if numpy.linalg.norm(numpy.array(pos) - numpy.array(self.center)) < self.radius:
            return True
        return False
