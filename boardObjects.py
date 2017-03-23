import pygame
#import numpy
import graphicalObjects
import random
#pygame.font.init()

# Board dimension constants
WIN_LENGTH = 900
WIN_HEIGHT = 500
B_WIDTH = 572 #width of the inner box of the board
B_HEIGHT = 460 #height of the inner box of the board
WIN_CENTER = (450, 250)
T_HEIGHT = 180 #height of triangles on the board
T_WIDTH = 44 #width of the triangles on the board
C1_RADIUS = 20 #radius of each checker
SIDE = 25

# RGB color constants
GREEN = (100, 200, 0)
BROWN = (165,42,42)
WHITE = (255, 255, 255)
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Bar:
    """Class for the bar area of the board."""

    def __init__(self, team, board):

        self.board = board
        self.team = team

        # Creats bar for RED player
        if self.team == RED:
            self.bar = graphicalObjects.Rectangle(T_WIDTH, (B_HEIGHT + 38)/2,(WIN_CENTER[0] - T_WIDTH/2, WIN_CENTER[1]), BROWN)

        # Creates bar for WHITE player
        else:
            self.bar = graphicalObjects.Rectangle(T_WIDTH, (B_HEIGHT + 38)/2,(WIN_CENTER[0] - T_WIDTH/2, WIN_CENTER[1] - (B_HEIGHT + 38) / 2), BROWN)
                                 
        self.checkers = []
        self.empty = True #True if bar contains no checkers
        self.active = False #True if bar belongs to current player's team

    def draw(self, surface):
        """Draws the bar to the surface."""
        self.bar.draw(surface)

    def drawCheckers(self, surface):
        """Draws each checker on the bar to the surface."""
        for checker in self.checkers:
            checker.draw(surface)

    def checkersAmount(self):
        """Returns the numbers of checker that are on the bar."""
        return len(self.checkers)
        
    def addChecker(self, checker):
        """Adds checker to bar."""
        self.checkers.append(checker)
      
    def returnChecker(self):
        """Returns the bottom-most checker from the bar."""
        return self.checkers[0]
   
    def removeChecker(self):
        """Removes the top-most checker from Point"""
        self.checkers.pop(0)
 
    def isEmpty(self):
        """Returns True if bar is empty and False if otherwise."""
        return self.empty

    def organize(self):
        """Stacks each checker that belongs to the bar so that they all lie
        in a straight line centered at bar's midpoint."""
        for i in range(len(self.checkers)):
            
            # Stack's checkers on red player's side of the bar
            if self.team == RED:
                self.checkers[i].moveTo((WIN_CENTER[0], int(WIN_CENTER[1]\
                + .5 * B_HEIGHT - C1_RADIUS - (i % 5) * 2 * C1_RADIUS)))
            
            # Stacks checkers on white player's side of the bar
            else:
                self.checkers[i].moveTo((WIN_CENTER[0], int(WIN_CENTER[1]\
                - .5 * B_HEIGHT + C1_RADIUS + (i % 5) * 2 * C1_RADIUS)))

    def update(self):
        """Updates the self.empty attribute."""
        self.empty = not len(self.checkers)

    def setActiveTurn(self):
        """Makes piece active if it's checkers correspond to the active team."""
        if self.board.getTurn() == self.team and not self.isEmpty():
            self.active = True
        else:
            self.active = False


class CheckerBox:
    """Graphical object that stores checkers that leave the board."""

    def __init__(self, surface):
        self.box = graphicalObjects.Rectangle(T_WIDTH, B_HEIGHT,
                             (WIN_CENTER[0] + (B_WIDTH + 40) / 2 + T_WIDTH - \
                              T_WIDTH/2, WIN_CENTER[1]-B_HEIGHT/2), BROWN)

        self.redCheckers = []
        self.whiteCheckers = []
        self.surface = surface

    def draw(self, surface):
        """Draws the checker box to the surface."""
        self.box.draw(surface)

    def drawCheckers(self, surface):
        """Draws each of the checkers on the checker box to the surface."""
        for checker in self.whiteCheckers:
            checker.draw(self.surface)
        for checker in self.redCheckers:
            checker.draw(self.surface)

    def addChecker(self, checker):
        """Adds checker to appropriate side in the bar."""
    
        # Adds red checker to red side
        if checker.getColor() == RED:
            self.redCheckers.append(checker)
            checker.moveTo((int((WIN_CENTER[0] + (B_WIDTH + 40) / 2 + T_WIDTH)),\
            int(WIN_CENTER[1] - C1_RADIUS - (len(self.redCheckers) - 1) * \
            C1_RADIUS / 1.5)))
            self.redCheckers.append(checker)
        
        # Adds white checker to white side
        else:
            self.whiteCheckers.append(checker)
            checker.moveTo((int((WIN_CENTER[0] + (B_WIDTH + 40) / 2 + T_WIDTH)),\
            int(WIN_CENTER[1] - C1_RADIUS + B_HEIGHT/2 - (len(self.whiteCheckers)\
            - 1) * C1_RADIUS / 1.5)))
            self.whiteCheckers.append(checker)


class Dice:
    """A graphical object that rolls when clicked."""

    def __init__(self, board, surface):

        self.board = board

        self.die1 = graphicalObjects.Rectangle(SIDE, SIDE, (WIN_CENTER[0] + 40, WIN_CENTER[1]), WHITE)
        self.die2 = graphicalObjects.Rectangle(SIDE, SIDE, (WIN_CENTER[0] + 80, WIN_CENTER[1]), WHITE)

        #Starting numbers
        self.die1_num = 1
        self.die2_num = 3

        self.die1_face = graphicalObjects.Text('1', (WIN_CENTER[0] + 46, WIN_CENTER[1]), 18)
        self.die2_face = graphicalObjects.Text('3', (WIN_CENTER[0] + 86, WIN_CENTER[1]), 18)

        self.points = None
        self.active = True
        self.surface = surface

    def draw(self, surface):
        """Draws the dice to the surface."""
        self.die1.draw(surface)
        self.die2.draw(surface)
        self.die1_face.draw(surface)
        self.die2_face.draw(surface)

    def checkClick(self, pos):
        """Given the mouse position, checkes whether a player has clicked
           on the dice."""
        if self.die1.checkClick(pos) or self.die2.checkClick(pos):
            self.handleMouseRelease()

    def handleMouseRelease(self):
        """Instructs the dice to roll when clicked."""
        self.roll()

    def roll(self):
        """Rolls both die. Updates the number values accordingly and sets the
           active variable to false."""
        if self.active:
            self.die1_num = random.randrange(1, 7)
            self.die1_face.setText(str(self.die1_num))
            self.die2_num = random.randrange(1, 7)
            self.die2_face.setText(str(self.die2_num))
            self.active = False
            self.board.getDiceNumbers()
            self.board.possibleBarMoves()
            self.draw(self.surface)
            pygame.display.flip()

    def getNumbers(self):
        """Returns the number of both die faces as a tuple."""
        if self.die1_num == self.die2_num:
            numList = [self.die1_num] * 4
            return sorted(numList)
        return sorted([self.die1_num, self.die2_num])

    def isActive(self):
        """Returns the active value for Dice."""
        return self.active

    def makeActive(self):
        """Sets the active variable to true."""
        self.active = True

    def addPoints(self, points):
        """Adds the board's points to Dice."""
        self.points = points


class Point:
    """Class for the points on the board. Interacts with the players."""

    def __init__(self, x, y, side, board, dice, color, surface):

        self.number = None
        self.color = color

        # Following variable is True if the player is allowed to make a move
        # from the board's clicked point to here.
        self.isValidMove = False
        self.board = board
        self.dice = dice
        self.side = side
        self.surface = surface

        # Coordinates for the right-most vertex
        self.x = x
        self.y = y

        # Constructs the shape graphic if it is on the bottom row
        if side == 'bottom':
            self.triangle = graphicalObjects.Triangle(self.color, ((x, y), (x - T_WIDTH, y),
                                                 (x - T_WIDTH/2, y - T_HEIGHT)), side)

        # Constructs the shape graphic if it is on the top row
        else:
            self.triangle = graphicalObjects.Triangle(self.color, ((x, y), (x + T_WIDTH, y),
                                                  (x + T_WIDTH/2, y + T_HEIGHT)), side)

        self.checkers = []
        self.open = True #True if point contains no checkers
        self.blot = False #True if point contains only one checker
        self.team = None #Corresponds to the color of the occupying team
        self.active = False #True if Point's checkers belong to current player
        self.clicked = False #True player wants to move checkers from here

    def checkClick(self, pos):
        """Given the mouse position, checks whether a player has clicked
           on the point."""
        if self.triangle.checkClick(pos):
            self.handleMouseRelease()

    def draw(self, surface):
        """Draws Triangle to screen."""
        self.triangle.draw(surface)

    def drawCheckers(self, surface):
        """Draws the checkers to the surface."""
        for checker in self.checkers:
            checker.draw(surface)
                            
    def handleMouseRelease(self):
        """This method determines what happens when a player selects a point."""
        emptyBar = self.board.isCurrentBarEmpty() #True if current bar is empty
        
        # Attempts to bear checker from clicked triangle off if correct 
        # conditions are met; returns from function if piece is born off
        if self.board.isCurrentPlayerHome():
            if self.active and not (self.board.isPieceClicked() \
            or self.dice.isActive()):
                if self.board.attemptBearOff(self):
                    return
        
        # Checks conditons for moving checkers assuming there is no checker on 
        # current player's bar
        if emptyBar:
            if self.clicked:
                self.undoClick()
            elif self.active and not (self.clicked or \
            self.board.isPieceClicked() or self.dice.isActive()):
                self.click()
            elif self.isValidMove and not self.dice.isActive(): 
                self.board.moveChecker(self)
        
        # Calls the corresponding function if there is a piece of the current
        # player's bar
        else:
            if self.isValidMove:
                self.board.moveCheckerFromBar(self)

    def undoClick(self):
        """Deactivates the clicked piece so that it is no longer considered 
        'clicked' by the board and deactivates the pieces that were considered
        potential moves based on the clicked piece."""
        self.clicked = False
        self.setBorder(BLACK, 1)
        self.board.undoPossibleMoves(self.number)

    def click(self):
        """Sets the point as clicked, changes border color and width, and 
        computes the possible moves using the available dice numbers and 
        the clicked clicked point as the starting position."""
        self.clicked = True
        self.setBorder(YELLOW, 3)
        self.board.possibleMoves(self.number)
    
    def checkersAmount(self):
        """Returns the number of checkers that are on the piece."""
        return len(self.checkers)
    
    def addChecker(self, checker):
        """Adds the given checker object to Point"""
        self.checkers.append(checker)
    
    def removeChecker(self):
        """Removes the top-most checker from Point"""
        self.checkers.pop(0)
    
    def returnChecker(self):
        """Returns the bottom-most checker on the piece."""
        return self.checkers[0]
    
    def isOpen(self):
        """Returns True if point is open and false if otherwise."""
        return self.open

    def isBlot(self):
        """Returns True if point is a blot and false if otherwise."""
        return self.blot
    
    def isClicked(self):
        """Returns True if point is clicked and False otherwise."""
        return self.clicked
    
    def getTeam(self):
        """Returns the color of the occupying team. Returns None if Point is 
        open."""
        return self.team
    
    def getTeamIndex(self):
        """Returns the index corresponding to the point's occupying checkers."""
        if self.getTeam() == 'red':
            return 0
        return 1
    
    def setColor(self, color):
        """Sets the fill color of Point to color"""
        self.triangle.setFillColor(color)
    
    def setBorder(self, color, width):
        """Sets the border color and width of point."""
        self.triangle.setBorder(color, width)
        self.board.drawBoard()
        
    def organize(self):
        """Stacks each Checker that belongs to Point so that they all lie in a
        straight line centered at Point's midpoint"""
        if self.side == 'bottom':
            for i in range(len(self.checkers)):
                self.checkers[i].moveTo((int(self.x - T_WIDTH / 2), 
                                          int(self.y - C1_RADIUS 
                                          - (i % 5) * 2 * C1_RADIUS)))
        else: 
            for i in range(len(self.checkers)):
                self.checkers[i].moveTo((int(self.x + T_WIDTH / 2), 
                                          int(self.y + C1_RADIUS 
                                          + (i % 5) * 2 * C1_RADIUS)))
    
    def update(self):
        """Updates important attributes of Point. Should be called at the end
        of each turn."""
        self.open = not len(self.checkers)
        if len(self.checkers) == 1:
            self.blot = True
        else:
            self.blot = False
        if len(self.checkers) != 0:
            self.team = self.checkers[0].getColor()
        else:
            self.team = None
    
    def setActiveTurn(self):
        """Makes piece active if it's checkers correspond to the active team."""
        if self.board.getTurn() == self.team:
            self.active = True
        else:
            self.active = False

    def isActive(self):
        """Returns True if the piece is active."""
        return self.active

    def setValidMove(self, value):
        """Sets the valid move attribute."""
        self.isValidMove = value
    
    def addNumber(self, number):
        """Sets the number of the point to number."""
        self.number = number
        
    def getNumber(self):
        """Returns the point's number."""
        return self.number


class Checker:
    """Class for the checker pieces. This class is not interractive."""

    def __init__(self, color):

        self.color = color
        self.center = (0, 0)
        self.checker = graphicalObjects.Circle(self.color, self.center, C1_RADIUS)

    def checkClick(self, surface):
        """Given the mouse position, checks whether a player has clicked
           on the checker."""
        return self.checker.checkClick(surface)

    def draw(self, surface):
        """Draws Checker to surface"""
        self.checker.draw(surface)

    def getColor(self):
        """Returns the color of Checker"""
        return self.color

    def getPlayerIndex(self):
        """Returns the player index corresponding to the checker's color."""
        if self.color == RED:
            return 0
        return 1

    def moveTo(self, center):
        """Moves Checker so it is centered at the given center"""
        self.checker.moveTo(center)


class TurnChanger:
    """Object that changes the turn when clicked."""

    def __init__(self, board):

        self.board = board

        # Creates button and text objects
        self.button = graphicalObjects.Circle(RED, (70, 165), 64)
        self.text1 = graphicalObjects.Text('CHANGE TURN', (35, 135), 12)
        self.text2 = graphicalObjects.Text('click button if you', (13, 165), 10)
        self.text3 = graphicalObjects.Text('have no valid moves', (13, 175), 10)

    def draw(self, surface):
        """Draws the turnchanger to the surface."""
        self.button.draw(surface)
        self.text1.draw(surface)
        self.text2.draw(surface)
        self.text3.draw(surface)

    def checkClick(self, pos):
        """Given the mouse postion, checks whether a player has clicked
           on the turn changer."""
        if self.button.checkClick(pos):
            self.board.changeTurn()

    def setFillColor(self, color):
        """Sets the fill color to the turn changer button to color."""
        self.button.setFillColor(color)

