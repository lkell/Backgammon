import pygame
#import numpy
import boardObjects
import graphicalObjects

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


class Board:
    """Top-level class for the backgammon game. Contains all the game objects as
       attributes."""

    def __init__(self, surface):

        self.won = False
        self.surface = surface
        self.background = graphicalObjects.Rectangle(B_WIDTH, B_HEIGHT, (int(WIN_CENTER[0]-B_WIDTH/2), int(WIN_CENTER[1]-B_HEIGHT/2)), GREEN)
        self.outer = graphicalObjects.Rectangle(B_WIDTH + 40, B_HEIGHT + 38, (int(WIN_CENTER[0] - (B_WIDTH + 40)/2), int(WIN_CENTER[1] - (B_HEIGHT + 38)/2)), BROWN)

        # Creates the bar where the checkers go when the point is hit
        self.bar = []
        self.bar.append(boardObjects.Bar(RED, self))
        self.bar.append(boardObjects.Bar(WHITE, self))

        # Creates the box where checkers are placed when they leave the board
        self.checkerBox = boardObjects.CheckerBox(self.surface)

        # Creates the players and sets the first turn to red
        self.players = []
        for color in [RED, WHITE]:
            self.players.append(Player(color, self))
        self.currentPlayer = 0

        # Creates message which displays who's turn it is
        self.message = graphicalObjects.Text\
                       ('It\'s ' + self.getCurrentString() 
                        + '\'s turn!', (20, 60), 12, WHITE)
        
        # Creates the game dice

        self.dice = boardObjects.Dice(self, self.surface)


        # Creates a list that contains all the board points

        self.points = []

        # Creates the points for the bottom row
        for i in range(13):
            if i != 6:
                if i % 2 == 0:
                    # Creates white points
                    self.points.append(boardObjects.Point(
                        (WIN_CENTER[0] + .5 * B_WIDTH)
                        -(i * (T_WIDTH)), WIN_CENTER[1]
                        + .5 * B_HEIGHT, 'bottom', self, 
                        self.dice, BEIGE, self.surface))
                else:
                    # Creates red points
                    self.points.append(boardObjects.Point(
                        (WIN_CENTER[0] + .5 * B_WIDTH)
                        -(i * (T_WIDTH)), WIN_CENTER[1]
                        + .5 * B_HEIGHT, 'bottom', self, 
                        self.dice, BLACK, self.surface))

        # Creates the points for the top row
        for i in range(13):
            if i != 6:
                if i % 2:
                    self.points.append(boardObjects.Point(
                        (WIN_CENTER[0] - .5 * B_WIDTH) + 
                        (i * (T_WIDTH)), WIN_CENTER[1] - 
                        .5 * B_HEIGHT, 'top', self, 
                        self.dice, BEIGE, self.surface))
                else:
                    self.points.append(boardObjects.Point(
                        (WIN_CENTER[0] - .5 * B_WIDTH) + 
                        (i * (T_WIDTH)), WIN_CENTER[1] - 
                        .5 * B_HEIGHT, 'top', self, 
                        self.dice, BLACK, self.surface))


        # Places checkers on the points for starting game position
        for _ in range(2):
            self.points[0].addChecker(boardObjects.Checker(RED))
            self.points[23].addChecker(boardObjects.Checker(WHITE))
        for _ in range(3):
            self.points[7].addChecker(boardObjects.Checker(WHITE))
            self.points[16].addChecker(boardObjects.Checker(RED))
        for _ in range(5):
            self.points[5].addChecker(boardObjects.Checker(WHITE))
            self.points[11].addChecker(boardObjects.Checker(RED))
            self.points[12].addChecker(boardObjects.Checker(WHITE))
            self.points[18].addChecker(boardObjects.Checker(RED))

        self.pointsSetUp()

        # Indicates that there is no clicked piece 
        self.clickedPiece = None

        self.dice.addPoints(self.points)

        # List of dice numbers that can be used to make a move
        self.diceNumbers = []

        # Creates button that changes turns and indicates who's turn it is
        self.turnchanger = boardObjects.TurnChanger(self)

        self.turnchanger.draw(self.surface)

        # Adds point list to each player
        for player in self.players:
            player.addPoints(self.points)

        self.drawBoard()

    def isGameWon(self):
        # Returns true if the game is won
        return self.won

    def drawBoard(self):
        """Draws all the board's graphical objects to the surface and
           updates the display."""
        self.outer.draw(self.surface)
        self.background.draw(self.surface)
        for point in self.points:
            point.draw(self.surface)
            point.drawCheckers(self.surface)
        self.dice.draw(self.surface)
        self.message.draw(self.surface)
        self.checkerBox.draw(self.surface)
        self.checkerBox.drawCheckers(self.surface)
        for bar in self.bar:
            bar.draw(self.surface)
            bar.drawCheckers(self.surface)
        pygame.display.flip()

    def checkClick(self, pos):
        """Checks to see if a player has clicked on any of the
           interractive board elements."""
        self.dice.checkClick(pos)
        self.turnchanger.checkClick(pos)
        for point in self.points:
            point.checkClick(pos)

    def getCurrentString(self):
        """Returns string corresponding to current player's color."""
        if self.getTurn() == RED:
            return 'red'
        return 'white'

    def checkWinner(self, surface):
        """Checks whether the current player has cleared all checkers."""
        winner = True
        
        # Checks for winner
        for point in self.points:
            if point.getTeam() == self.getTurn():
                winner = False
        
        # Displays winner message if there is a winner
        if winner:
            self.surface.fill(BLACK)
            winText = graphicalObjects.Text(self.getCurrentString() + ' wins!', WIN_CENTER, 20)
            winText.draw(self.surface)
            self.won = True

    def isCurrentPlayerHome(self):
        """Returns True if the current player's checkers are all home by
        checking whether the current player has checkers in any pieces that are
        not in the home area.."""
        
        #creates corresponding starting and ending points for each player
        if self.getTurn() == RED:
            start = 0
            end = 18
        else:
            start = 6
            end = 24
        
        #checks whether the current player has checkers on corresponding points
        for i in range(start, end):
            if self.points[i].getTeam() == self.getTurn():
                return False
        
        return True
    
    def getDiceNumbers(self):
        """Updates the diceNumbers list to match the current dice numbers."""
        self.diceNumbers = []
        for num in self.dice.getNumbers():
            self.diceNumbers.append(num)

    def pointsSetUp(self):
        """Performs important setup methods for points."""
        self.background.draw(self.surface)
        for i in range(len(self.points)):
            self.points[i].organize()
            self.points[i].update()
            self.points[i].addNumber(i)
            self.points[i].setActiveTurn()   

    def organizeAndUpdate(self):
        """Stacks the checkers for each point and updates key attributes."""    
        for point in self.points:
            point.organize()
            point.update()

    def setPointsToTurn(self):
        """Sets all the points whose checkers correspond to the active team 
        to active."""
        for point in self.points:
            point.setActiveTurn()
    
    def getTurn(self):
        """Returns the color corresponding to whos turn it is."""
        return self.players[self.getCurrentPlayer()].getColor()
    
    def getCurrentPlayer(self):
        """Returns the index integer representing the current player."""
        return self.currentPlayer
        
    def isCurrentBarEmpty(self):
        """Returns true if the active player's bar is empty, false otherwise."""
        return self.bar[self.getCurrentPlayer()].isEmpty()
    
    def changeTurn(self):
        """Changes the current player and updates the active statuses of the 
        board pieces to correspond with the current player."""
        # Undoes clicked pieces and removes potential moves from the bar area
        for point in self.points:
            if point.isClicked():
                point.undoClick()
        if not self.bar[self.currentPlayer].isEmpty():
            self.undoPossibleBarMoves()
        
        # Changes by turn changing the currentPlayer index and updating all the 
        # necessary board objects
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.dice.makeActive()
        for point in self.points:
            point.setActiveTurn()
        for bar in self.bar:
            bar.update()
            bar.setActiveTurn()
        self.message.resetText('It\'s ' + self.getCurrentString() + '\'s turn!', self.surface)
        self.turnchanger.setFillColor(self.getTurn())
        self.turnchanger.draw(self.surface)
        pygame.display.flip()

    def possibleMoves(self, startingPiece):
        """Determines the possible moves based on the clicked piece and the
        available numbers on the dice."""
        self.clickedPiece = startingPiece
        for num in self.diceNumbers:
            nextPoint = startingPiece + num * ((-1) ** self.currentPlayer)
            
            #sets points as valid moves if a move can be made to them from the
            #clicked piece
            if nextPoint < len(self.points) and nextPoint >= 0:
                if self.points[nextPoint].isOpen()\
                or self.points[nextPoint].isBlot()\
                or self.points[nextPoint].getTeam() == self.getTurn():
                    self.points[nextPoint].setValidMove(True)
                    self.points[nextPoint].setBorder(RED, 3)
                
    def possibleBarMoves(self):
        """Determines the possible moves based on whether there are checkers in
        the current player's bar and the available numbers on the dice."""
        
        if not self.bar[self.currentPlayer].isEmpty(): 
            # Creates point index for the corresponding current player
            for num in self.diceNumbers:
                if self.currentPlayer == 0:
                    potentialPoint = num - 1
                else: 
                    potentialPoint = num * (-1) 
                
                # Sets points as valid moves if a move can be made to them from
                # the bar
                if self.points[potentialPoint].isOpen()\
                or self.points[potentialPoint].isBlot()\
                or self.points[potentialPoint].getTeam() == self.getTurn():
                    self.points[potentialPoint].setValidMove(True)
                    self.points[potentialPoint].setBorder(RED, 3)

    def undoPossibleMoves(self, startingPiece):
        """Resets all pieces that were possible moves from the previous
        clicked piece."""
        self.clickedPiece = None #Indicates that the board has no clicked piece
        for num in self.diceNumbers:
            nextPoint = startingPiece + num * ((-1) ** self.currentPlayer)
            if nextPoint < len(self.points) and nextPoint >= 0:
                self.points[nextPoint].setValidMove(False)
                self.points[nextPoint].setBorder(BLACK, 1)
    
    def undoPossibleBarMoves(self):
        """Resets all points that were previously possible moves from the bar"""
        for num in self.diceNumbers:
            if self.currentPlayer == 0:
                potentialPoint = num - 1
            else:
                potentialPoint = num * (-1)
            self.points[potentialPoint].setValidMove(False)
            self.points[potentialPoint].setBorder(BLACK, 1)
    
    def moveChecker(self, point):
        """Moves checker from the clicked piece to point."""
        
        clickedPiece = self.clickedPiece
        
        # Checks whether the new point should be hit and calls the the pointHit
        # method if necessary
        if point.isBlot() and \
        point.getTeam() != self.points[clickedPiece].getTeam():
            self.pointHit(point)
        
        # Adds checker to new point and updates the new point correspondingly
        point.addChecker(self.points[self.clickedPiece].returnChecker())
        point.organize()
        point.update()
        point.setActiveTurn()
        
        # Removes checker from the clicked point and updates the point
        self.points[clickedPiece].removeChecker()
        self.points[clickedPiece].organize()
        self.points[clickedPiece].update()
        self.points[clickedPiece].setActiveTurn()
        self.points[clickedPiece].undoClick()
        
        # Updates available dice numbers
        self.diceNumbers.remove((point.getNumber() - clickedPiece)
                                 * (-1) ** self.currentPlayer)
        
        # Changes turn if necessary
        if not len(self.diceNumbers):
            self.changeTurn()

        self.drawBoard()
    
    def moveCheckerFromBar(self, point):
        """Moves checker from the bar to point."""
        
        # Calls the pointHit method if checker moves to a point occupied by
        # the opposing player
        if point.isBlot() and\
        point.getTeam() != self.getTurn():
            self.pointHit(point)
        
        # Adds checker to the new point and organizes and updates that point
        point.addChecker(self.bar[self.currentPlayer].returnChecker())
        point.organize()
        point.update()
        point.setBorder(BLACK, 1)
        point.setValidMove(False)
        point.setActiveTurn()
        
        # Removes checker from bar and updates the bar accordingly
        self.bar[self.currentPlayer].removeChecker()
        self.bar[self.currentPlayer].organize()
        self.bar[self.currentPlayer].update()
        self.bar[self.currentPlayer].setActiveTurn()
        
        # Removes the corresponding dice number from the dice number list
        if self.currentPlayer == 0:
            self.diceNumbers.remove(point.getNumber() + 1)
        else:
            self.diceNumbers.remove(24 - point.getNumber())
        
        # Changes turn if necessary
        if not len(self.diceNumbers):
            self.changeTurn()
            return

        self.bar[self.getCurrentPlayer()].draw(self.surface)
        self.bar[self.getCurrentPlayer()].drawCheckers(self.surface)
        pygame.display.update()
        
        # Removes possible moves from the bar now that the move has been made
        if self.bar[self.currentPlayer].isEmpty():
            self.undoPossibleBarMoves()
    
    def attemptBearOff(self, point):
        """Bears checker off if possible. Returns True if bear off occurs."""
        
        # Creates the values to be compared to dice numbers for both teams
        for num in self.diceNumbers:
            if self.getTurn() == RED:
                compare = 24 - point.getNumber()
            else:
                compare = point.getNumber() + 1
            
            # If the dice number is sufficiently large enough, the point's 
            # checker piece leaves the board for good and is placed in the 
            # checkerBox, indicating that it is no longer in play
            if num >= compare:
                self.checkerBox.addChecker(point.returnChecker())
                point.removeChecker()
                point.organize()
                point.update()
                point.setActiveTurn()
                self.diceNumbers.remove(num)
                self.drawBoard()
                
                # Checks whether the current player has won the game yet
                self.checkWinner(self.surface)
                
                # Changes teams if all the dice numbers are used up
                if not len(self.diceNumbers) and not self.isGameOver():
                    self.changeTurn()
                
                return True #This value indicates that bear off was successful
        
        return False


    def pointHit(self, point):
        """Removes current checker occupying point and adds it to the bar."""
        self.bar[(self.currentPlayer + 1)%2].addChecker(point.returnChecker())
        self.bar[(self.currentPlayer + 1) % 2].organize()
        self.bar[(self.currentPlayer + 1) % 2].update()
        point.removeChecker()
    
    def isPieceClicked(self):
        """Returns False if there is no clicked piece on the board and none 
        otherwise."""
        if self.clickedPiece is None:
            return False
        return True

    def setPointsActive(self):
        """Sets all the points on the board that are occupied by the current 
        player as active."""
        for point in self.points:
            point.setActive()


class Player:
    """A non-graphical object representing a player in the game."""
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.points = []
        
    def addPoints(self, points):
        """Adds all the points to player."""
        self.points = points
    
    def getColor(self):
        """Returns the color corresponding to player."""
        return self.color


screen = pygame.display.set_mode((WIN_LENGTH, WIN_HEIGHT))
clock = pygame.time.Clock()
board = Board(screen)
running = True

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.checkClick(event.pos)
    if board.isGameWon():
        answer = input('Press any key to play again ')
        board = Board(screen)
    
