import types
from Player import Player
from config import *
import numpy as np

import pdb

def right(x):
  """Helper function: argument x must be a dot.
  Returns dot right of x."""
  return (x[0]+1,x[1])

def upper(x):
  """Helper function: argument x must be a dot.
  Returns dot above (actually below) x."""
  return (x[0], x[1]+1)

def cartesian( v1, v2 ):
  """ Helper function
  returns cartesian product of the two
  'sets' v1, v2"""
  return tuple([(x,y) for x in v1 for y in v2])

class GameBoard:
  def __init__(self, width=5, height=5, playerA=PLAYER_TYPE_HUMAN, playerB=PLAYER_TYPE_HUMAN, depth = 3, useDecisionTree= True, dynamicDepth= False):
    """Initializes a rectangular gameboard."""
    self.width, self.height = width, height
    assert 2 <= self.width and 2 <= self.height,\
           "Game can't be played on this board's dimension."
    self.board = {}
    self.squares = {}
    self.player = 0
    self.players = {
      0: Player(self, playerA, 0, depth, useDecisionTree, dynamicDepth),
      1: Player(self, playerB, 1, depth, useDecisionTree, dynamicDepth),
    }

    self.board_state_size = (self.width-1) * self.height * 2
    self.board_state = np.zeros(shape = (1,  (self.width-1) * self.height * 2))
    self.empty_states = set()

    for i in range(self.board_state_size):
      self.empty_states.add(i)
    
    self.scores = [0,0]

    self.move_to_state = {}

    for dot in cartesian(range(self.width), range(self.height)):
      if dot[0] < self.width - 1:
        move = (dot, right(dot))
        ind = self.__convert_move_to_state(move)
        self.move_to_state[move] = ind

      if dot[1] < self.height - 1:
        move = (dot, upper(dot))
        ind = self.__convert_move_to_state(move)
        self.move_to_state[move] = ind

  def __convert_move_to_state(self, move):
    if move[0][1] == move[1][1]:
      # Right move
      ind = move[0][1]* (2 * self.width - 1) + move[0][0]
    else:
      # Upper move
      ind = ((move[1][1] -1) * self.width +
             move[1][1] * (self.width -1) + move[0][0])
    return ind

  def isGameOver(self):
    """Returns true if no more moves can be made.

    The maximum number of moves is equal to the number of possible
    lines between adjacent dots.  I'm calculating this to be
    $2*w*h - h - w$; I think that's right.  *grin*
    """
    w, h = self.width, self.height
    return len(self.board.keys()) == 2*w*h - h - w



  def _isSquareMove(self, move):
    """Returns a true value if a particular move will create a
    square.  In particular, returns a list of the the lower left
    corners of the squares captured by a move.
    """
    b = self.board
    mmove = self._makeMove       ## just to make typing easier
    ((x1, y1), (x2, y2)) = move
    captured_squares = []
    if self._isHorizontal(move):
      for j in [-1, 1]:
        if (b.has_key(mmove((x1, y1), (x1, y1-j)))
            and b.has_key(mmove((x1, y1-j), (x1+1, y1-j)))
            and b.has_key(mmove((x1+1, y1-j), (x2, y2)))):
            captured_squares.append(min([(x1, y1), (x1, y1-j),
                                         (x1+1, y1-j), (x2, y2)]))
    else:
      for j in [-1, 1]:
        if (b.has_key(mmove((x1, y1), (x1-j, y1)))
            and b.has_key(mmove((x1-j, y1), (x1-j, y1+1)))
            and b.has_key(mmove((x1-j, y1+1), (x2, y2)))):
            captured_squares.append(min([(x1, y1), (x1-j, y1),
                                         (x1-j, y1+1), (x2, y2)]))
    return captured_squares

    score, captured = self._getMoveScore(move)
    return captured

  def _getMoveScore(self, move):
    """
    Returns score of a move and captured squares.
    Score
      2 = completes two squares with this move
      1 = completes one square with this move
      0 = does not complete any square and 
          does not set up a square for the next player
      -1 = sets up a square for the next player
    """
    score = 0
    captured = []
    b = self.board
    mmove = self._makeMove
    ((x1, y1), (x2, y2)) = move

    if self._isHorizontal(move):
      for j in [-1, 1]:
        neighbors = 0

        if b.has_key(mmove((x1, y1), (x1, y1-j))):
          neighbors += 1
        if b.has_key(mmove((x1, y1-j), (x1+1, y1-j))):
          neighbors += 1
        if b.has_key(mmove((x1+1, y1-j), (x2, y2))):
          neighbors += 1

        if neighbors == 3:
          score += 1
          captured.append(min([(x1, y1), (x1, y1-j),
                              (x1+1, y1-j), (x2, y2)]))
        elif neighbors == 2: # sets up square for the other player
          score -= 1

    else:
      for j in [-1, 1]:
        neighbors = 0
        if b.has_key(mmove((x1, y1), (x1-j, y1))):
          neighbors += 1
        if b.has_key(mmove((x1-j, y1), (x1-j, y1+1))):
          neighbors += 1
        if b.has_key(mmove((x1-j, y1+1), (x2, y2))):
          neighbors += 1

        if neighbors == 3:
          score += 1
          captured.append(min([(x1, y1), (x1-j, y1),
                             (x1-j, y1+1), (x2, y2)]))
        elif neighbors == 2:
          score -= 1

    return score, captured


  def _isHorizontal(self, move):
    "Return true if the move is in horizontal orientation."
    return abs(move[0][0] - move[1][0]) == 1


  def _isVertical(self, move):
    "Return true if the move is in vertical orientation."
    return not self.isHorizontal(self, move)


  def play(self, move):
    """Place a particular move on the board.  If any wackiness
    occurs, raise an AssertionError.  Returns a list of
    bottom-left corners of squares captured after a move."""
    assert (self._isGoodCoord(move[0]) and
            self._isGoodCoord(move[1])),\
            "Bad coordinates, out of bounds of the board."
    move = self._makeMove(move[0], move[1])
    assert(not self.board.has_key(move)),\
               "Bad move, line already occupied."
    self.board[move] = self.player
    
    ind = self.move_to_state[move]
    self.board_state[0][ind] = self.player * 2 -1
    self.empty_states.remove(ind)
    
    ## Check if a square is completed.
    square_corners = self._isSquareMove(move)
    if square_corners:
      for corner in square_corners:
        self.squares[corner] = self.player
    else:
      self._switchPlayer()

    return square_corners

  """
  ADDED BY HANGIL
  """
  def unplay(self, move, currPlayer):
    """
    Remove a move from a board
    """
    move = self._makeMove(move[0], move[1])
    assert(self.board.has_key(move), "move exists, can remove")
    self.board.pop(move, None)
    square_corners = self._isSquareMove(move)
    if square_corners:
      for corner in square_corners:
        self.squares.pop(corner, None)
    self.player = currPlayer

    ind = self.move_to_state[move]
    self.board_state[0][ind] = 0
    self.empty_states.add(ind)
    
    return square_corners

  def getScores(self):
    scores = [0,0]
    for key in self.squares.keys():
      scores[self.squares[key]] +=1
    return scores

  def _switchPlayer(self):
    self.player = (self.player + 1) % 2


  def getPlayer(self): 
    return self.player, self.players[self.player]


  def getSquares(self):
    """Returns a dictionary of squares captured.  Returns
    a dict of lower left corner keys marked with the
    player who captured them."""
    return self.squares


  def __str__(self):
    """Return a nice string representation of the board."""
    buffer = []
    
    ## do the top line
    for i in range(self.width-1):
      if self.board.has_key(((i, self.height-1), (i+1, self.height-1))):
        buffer.append("+--")
      else: buffer.append("+  ")
    buffer.append("+\n")

    ## and now do alternating vertical/horizontal passes
    for j in range(self.height-2, -1, -1):
      ## vertical:
      for i in range(self.width):
        if self.board.has_key(((i, j), (i, j+1))):
          buffer.append("|")
        else:
          buffer.append(" ")
        if self.squares.has_key((i, j)):
          buffer.append("%s " % self.squares[i,j])
        else:
          buffer.append("  ")
      buffer.append("\n")

      ## horizontal
      for i in range(self.width-1):
        if self.board.has_key(((i, j), (i+1, j))):
          buffer.append("+--")
        else: buffer.append("+  ")
      buffer.append("+\n")

    return ''.join(buffer)



  def _makeMove(self, coord1, coord2):
    """Return a new "move", and ensure it's in canonical form.
    (That is, force it so that it's an ordered tuple of tuples.)
    """
    ## TODO: do the Flyweight thing here to reduce object creation
    xdelta, ydelta = coord2[0] - coord1[0], coord2[1] - coord1[1]
    assert ((abs(xdelta) == 1 and abs(ydelta) == 0) or
            (abs(xdelta) == 0 and abs(ydelta) == 1)),\
            "Bad coordinates, not adjacent points."
    if coord1 < coord2:
      return (coord1, coord2)
    else:
      return (tuple(coord2), tuple(coord1))


  def _isGoodCoord(self, coord):
    """Returns true if the given coordinate is good.

    A coordinate is "good" if it's within the boundaries of the
    game board, and if the coordinates are integers."""
    return (0 <= coord[0] < self.width
            and 0 <= coord[1] < self.height
            and isinstance(coord[0], types.IntType)
            and isinstance(coord[1], types.IntType))
  


# def _test(width, height):
#   """A small driver to make sure that the board works.  It's not
#   safe to use this test function in production, because it uses
#   input()."""
#   board = GameBoard(width, height)
#   turn = 1
#   scores = [0, 0]
#   while not board.isGameOver():
#     player, _ = board.getPlayer()
#     print "Turn %d (Player %s)" % (turn, player)
#     print board
#     move = input("Move? ")
#     squares_completed = board.play(move)
#     if squares_completed:
#       print "Square completed."
#       scores[player] += len(squares_completed)
#     turn = turn + 1
#     print "\n"
#   print "Game over!"
#   print "Final board position:"
#   print board
#   print
#   print "Final score:\n\tPlayer 0: %s\n\tPlayer 1: %s" % \
#         (scores[0], scores[1])



if __name__ == "__main__":
  """If we're provided arguments, try using them as the
  width/height of the game board."""
  import sys
  # if len(sys.argv[1:]) == 2:
  #   _test(int(sys.argv[1]), int(sys.argv[2]))
  # elif len(sys.argv[1:]) == 1:
  #   _test(int(sys.argv[1]), int(sys.argv[1]))
  # else:
  #   _test(5, 5)
