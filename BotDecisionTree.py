import random

class BotDecisionTree:
  def __init__(self, board):
    self.board = board

  def getNextMove(self, gameGUI):
    """
    Randomized 
    """
    bestScore = None
    bestMove = None

    for bar in gameGUI.bars:
      if not self.board.board.has_key(bar): # unused bar
        score, captured = self.board._getMoveScore(bar)
        if bestScore is None or score >= bestScore:

          if score == bestScore: # if same score, randomize
            choice = random.choice([True, False])
            if choice:
              continue 

          bestScore = score
          bestMove = bar

    return bestMove
