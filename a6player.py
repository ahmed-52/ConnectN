"""
The models classes to represent a player.

This module has a base class (Player) as well as a subclass (AIPlayer). You will need
to implement both to play against the computer. But it is sufficient to implement the
first to have two humans play against each other.

# Ahmed Abdulla
# 11/14/2023
"""
import introcs
import random
import connectn
from a6board import *
from a6consts import *


#### TASK 1 ####
class Player(object):
    """
    A class representing a human player.
    """
    # HIDDEN ATTRIBUTES
    # Attribute _name: The player name
    # Invariant: _name is a nonempty string
    #
    # Attribute _color: The player color
    # Invariant: _color is a string representing a valid color (e.g. either
    #            introcs.is_tkcolor or introcs.is_webcolor returns True).
    
    def setName(self,value):
        """
        Sets the player name
        
        IF value is the empty string, the name will be set to '<color> player'
        where the color value is capitalized. For example, if color is 'red',
        the name will be set to 'Red player'
        
        Parameter value: The new name
        Precondition: value is a string
        """
        assert isinstance(value,str)
        if value == "":
            self._name = self._color[:1].upper() + self._color[1:]+' player'
        else:
            self._name = value

    
    def getName(self):
        """
        Returns the player name
        """
        return self._name
    
    def getColor(self):
        """
        Returns the player color
        """
        return self._color
    
    def __init__(self,color,name=''):
        """
        Initializes a player with the given name and color.
        
        IF the name is the empty string, then the name will be set to '<color>
        player', where the color value is capitalized. For example, if color is
        'red', the name will be set to 'Red player'
        
        Parameter color: The new color
        Precondition: color is a string representing a valid color (e.g. either
                      introcs.is_tkcolor or introcs.is_webcolor returns True).
        
        Parameter name: The new name (default empty string)
        Precondition: name is a string
        """
        assert isinstance(color,str) and \
        introcs.is_webcolor(color) or introcs.is_tkcolor(color)
        assert isinstance(name,str)

        if name == '':
            self._name = color[:1].upper()+color[1:]+ " player"
        else:
            self._name = name
        self._color = color




    
    # WE HAVE IMPLEMENTED THIS FUNCTION FOR YOU
    # DO NOT MODIFY THIS METHOD
    def chooseMove(self,board):
        """
        Returns the current move for this player
        
        Parameter board: The board to choose from
        Precondition: board is a Board object that is not full
        """
        assert type(board) == Board
        assert not board.isFullBoard()
        # THIS IS HOW A HUMAN PLAYER MAKES A CHOICE
        return connectn.get_choice(self._color)


#### TASK 5 ####
class AIPlayer(Player):
    """
    A class representing an acceptable AI player.
    
    This class looks at each possible move and chooses the one it evaluates as
    the best.  If there is more than one "best" move, it returns a random
    selection from the best choices.
    
    Note that this AIPLayer is fairly simple, in that it does not consider
    possible responses of its opponent to its chosen move.  That would require
    an algorithm beyond the scope of this course.
    """
    # NO ADDITIONAL ATTRIBUTES BEYOND THOSE IN PLAYER

    def _scoreRun(self,board,run):
        """
        Returns the score of the given run.
        
        A run is either None or a tuple (r1,c1,r2,c2). If the run is None, this
        method returns SCORE_BAD.  Otherwise it returns the distance (see the
        function dist in board.py) of the run.
        
        Parameter board: The board to score from
        Precondition: board is a Board object
        
        Parameter run: The run to score
        Precondition: run is None or a tuple (r1,c1,r2,c2) of valid board
        positions.
        """
        assert isinstance(board,Board)
        assert isinstance(run,tuple) or run is None
        assert is_valid_run(board,run)

        if run is not None:
            r1,c1,r2,c2 = run
            return dist(board,r1,c1,r2,c2)
        else:
            return SCORE_BAD



    def _evaluate(self,board,r,c):
        """
        Returns the score of the current board state, assuming a piece placed
        at (r,c)
        
        This function finds all possible runs containing (r,c): vertical,
        horizontal, SWNE, and NWSE. It then scores each one and returns the
        highest score. If all scores are SCORE_BAD, it returns a value of 1
        (for the newly placed piece).
        
        If placing a piece guarantees a win, this returns the value SCORE_WIN
        
        Parameter board: The board to evaluate
        Precondition: board is a Board object
        
        Parameter r: The row of the last placed piece
        Precondition: r is an int and a valid row in the board; there is a
        color in (r,c)
        
        Parameter c: The column of the last placed piece
        Precondition: c is an int and a valid column in the board; there is a
        color in (r,c)
        """

        assert isinstance(board, Board)
        assert isinstance(r, int) and 0<= r < board.getHeight()
        assert isinstance(c, int) and  0 <= c < board.getWidth()
        assert not board.getColor(r,c) == NOBODY

        score = SCORE_BAD
        for length in range(board.getStreak(),1,-1):
            ver = board.findVertical(r, c, length)
            acr = board.findAcross(r, c, length)
            swne = board.findSWNE(r, c, length)
            nwse = board.findNWSE(r, c, length)

            ver = self._scoreRun(board,ver)
            acr = self._scoreRun(board,acr)
            swne = self._scoreRun(board,swne)
            nwse = self._scoreRun(board,nwse)
            
            if board.getStreak() in [ver, acr, swne, nwse]:
                return SCORE_WIN

            score = max(score, ver, acr, swne, nwse)

        return 1 if score == SCORE_BAD else score

        # HINT: If there is no immediate win, search 
        # for smaller streaks.
        # This require a a loop where you search 
        # for streaks of smaller values each step
        

    def _gatherMoves(self,board):
        """
        Returns a dictionary of acceptable moves in the board.
        
        A move is acceptable if there is space available in that column. So this
        dictionary will only have keys for columns that are valid.  The values
        for all keys will be SCORE_BAD.
        
        Parameter board: The board to evaluate
        Precondition: board is a Board object
        """
        assert isinstance(board, Board) 
        moves = {}
        for i in range (board.getWidth()):
            if not board.isFullColumn(i):
               moves[i]=SCORE_BAD
        return moves

    
    def _evaluateMoves(self,board,moves):
        """
        MODIFIES moves to include the score for each move.
        
        This method will compute a score for each move (column) in moves. To do
        this, it will actually need to first make the move, and then call
        _evaluate. However, since this is not the final move, it will need to
        undo the move using the method undoPlace in Board.
        
        Parameter board: The board to evaluate
        Precondition: board is a Board object
        
        Parameter moves: The moves to evaluate
        Precondition: moves is a dict whose keys are columns and values are scores
        """
        assert isinstance(board, Board)
        assert isinstance(moves, dict)
        assert is_valid_dict(board,moves)
        for c in moves:
            row = board.place(c,self._color)
            score = self._evaluate(board,row,c)
            moves[c] = score
            board.undoPlace()

        

    
    def _findBestMoves(self,board,moves):
        """
        Returns the list of the best moves.
        
        This method will return the keys (columns) of moves that 
        have the best score.
        The value will be returned as a list. If there is only one move with the best
        score, it returns a list of length 1. If there are ties for the best move, all
        best moves are included in the list.
        
        Parameter board: The board to evaluate
        Precondition: board is a Board object
        
        Parameter moves: The moves to evalutes
        Precondition: moves is a dict whose keys are columns and values are scores
        """
        # HINT: Use an accumulator to build the list of best moves, but reset it if you
        # find a better move
        assert isinstance(board,Board)
        assert is_valid_dict(board,moves)
        bestMoves = []
        maxscore = max(moves.values())
        for col, score in moves.items():
            if score == maxscore:
                bestMoves.append(col)
        return bestMoves
        
    
    def chooseMove(self,board):
        """
        Returns the current move for this player
        
        Parameter board: The board to choose from
        Precondition: board is a Board object that is not full
        """
        assert isinstance(board,Board)
        assert not board.isFullBoard()
        moves = self._gatherMoves(board)
        self._evaluateMoves(board, moves)
        bestMoves = self._findBestMoves(board, moves)
        if bestMoves:
            move = random.choice(bestMoves)
            connectn.set_choice(self._color, move) 
            return move
        else:
            return None
        
#### EXTRA CREDIT ####
class BetterAIPlayer(AIPlayer):
    # You are on your own
    # This new ai will block you from wining unlike 
    # the pervious one

    SCORE_BLOCK = 100000

    def _evaluateMoves(self, board, moves):

        opponent_color = 'red' if self._color != 'red' else 'yellow'
        for i in moves:
            
            row = board.place(i, self._color)
            ai_score = self._evaluate(board, row, i)
            board.undoPlace()

            
            row = board.place(i, opponent_color)
            opponent_score = self._evaluate(board, row, i)
            board.undoPlace()

            
            if opponent_score == SCORE_WIN:
                moves[i] = SCORE_BLOCK
            else:
                moves[i] = ai_score




#### HELPER FUNCTIONS ####
# DO NOT MODIFY
def is_valid_run(board,run):
    """
    Returns True if run is a valid run in board, False otherwise
    
    A valid run is one where run is None or run is a tuple (r1,c1,r2,c2) of ints
    where (r1,c1f) and (r2,c2) are valid board positions.
    
    Parameter board: The board to reference
    Precondition: board is a Board object
    
    Parameter run: The run to score
    Precondition: NONE (run can be anything)
    """
    assert type(board) == Board
    if run is None:
        return True
    if type(run) != tuple:
        return False
    if len(run) != 4:
        return False
    
    r1 = run[0]
    c1 = run[1]
    r2 = run[2]
    c2 = run[3]
    if (type(r1) != int or type(c1) != int 
        or type(r2) != int or type(c2) != int):
        return False
    
    return in_range(board,r1,c1) and in_range(board,r2,c2)


def is_valid_dict(board,moves):
    """
    Returns True if moves is a valid move dictionary.
    
    A valid move dictionary has valid columns as keys and integers >= 0 as values
    
    Parameter board: The board to reference
    Precondition: board is a Board object
    
    Parameter move: The move dictionary
    Precondition: NONE (move can be anything)
    """
    assert type(board) == Board
    if type(moves) != dict:
        return False
    
    for c in moves:
        if type(c) != int or c < 0 or c >= board.getWidth():
            return False
        if type(moves[c]) != int or moves[c] < 0:
            return False
    
    return True


