from gui import GameGUI
from board import GameBoard
import time
import sys
import config

def _run(width, height, playerA, playerB, depth = 3, useDecisionTree= True, dynamicDepth= False):
  print "Running... "
  board = GameBoard(width, height, playerA, playerB, depth, useDecisionTree, dynamicDepth)
  board.turn = 1
  board.scores = [0, 0]
  try:
    gui = GameGUI(board)
    print "Hello"
  except Exception as e:
    pass

def _runStats(width, height, playerA, playerB, depth = 3, useDecisionTree= True, dynamicDepth= False):
  line = "%d, %d, %s, %s, %d, %d, %d\n" % (width, height, playerA, playerB, depth, useDecisionTree, dynamicDepth)
  writeToStats(line, useDecisionTree)

  start = time.clock()
  board = GameBoard(width, height, playerA, playerB, depth, useDecisionTree, dynamicDepth)
  board.turn = 1
  board.scores = [0, 0]
  try:
    gui = GameGUI(board)
  except Exception as e:
    pass
  end = time.clock()
  line = "%f\n\n" %(end - start)
  writeToStats(line, useDecisionTree)


def writeToStats(line, useDecisionTree):
  # fname = config.STATS_T if useDecisionTree else config.STATS_F
  fname = config.STATS_FILE
  with open(fname, 'a') as f:
    f.write(line)

def __runAllStats(useDecisionTree):
  playerA = 'decision-tree'
  playerB  = 'minimax'
  
  for width in range(3, 8):
    for i in range(20):
      for depth in range(3, 6):
        _runStats(width, width, playerA, playerB, depth = depth, useDecisionTree= useDecisionTree, dynamicDepth= False)
      _runStats(width, width, playerA, playerB, depth = 3, useDecisionTree= useDecisionTree, dynamicDepth= True)


def __runAllStats(useDecisionTree):
  playerA = 'decision-tree'
  playerB  = 'minimax'
  
  for width in range(3, 8):
    for i in range(10):
      # for depth in range(3, 6):
        depth = -1
        _runStats(width, width, playerA, playerB, depth = depth, useDecisionTree= useDecisionTree, dynamicDepth= True)

if __name__ == '__main__':
  # mode
  # args: width height playerAType playerBType
  if len(sys.argv[1:]) == 7:
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    playerA = sys.argv[3]
    playerB = sys.argv[4]
    depth = int(sys.argv[5])
    useTree = int(sys.argv[6])
    dynamicDepth = int(sys.argv[7])

    if not playerA in config.PLAYER_TYPES or not playerB in config.PLAYER_TYPES:
      raise ValueError('invalid player types')

    _run(width, height, playerA, playerB, depth = depth, useDecisionTree= useTree, dynamicDepth= dynamicDepth)
  else:
    print 'requires: width height playerAType playerBType, depth, useTree, dynamicDepth'
    
  # __runAllStats(True)
  # __runAllStats(True)

