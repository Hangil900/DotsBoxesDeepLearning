import sys
import pdb, copy, random, math, config

class BotMinimax:
  def __init__(self, board, playerNum, depth, useDecisionTree, dynamicDepth):
    self.board = board
    self.playerNum = playerNum
    self.otherNum = (playerNum +1) % 2
    self.depth = depth
    self.useDecisionTree = useDecisionTree
    self.movesTable = None
    self.dynamicDepth = dynamicDepth

  def getNextMove(self, gameGUI):
    if self.dynamicDepth:
      self.depth = self.__getDynamicDepth(gameGUI)
      #print "in dynamic depth!"
      #print self.depth

    self.movesTable = [{}, {}]
    moves = [set(), set()]
    alpha = -sys.maxint
    beta = sys.maxint
    score, move = self.getMinMax(self.depth, True, gameGUI, moves, alpha, beta)
    #print "Score: %d Move: %s" % (score, str(move))
    return move

  def __getDynamicDepth(self, gameGUI):
    possMoves = []
    for bar in gameGUI.bars:
      if not self.board.board.has_key(bar):
        possMoves.append(bar)
    x = len(possMoves)
    try:
      newDepth = math.floor(math.log(config.MAX_MOVES, x))
    except Exception as e:
      return 3
    return newDepth

  #Taken from decision tree. Used for the beggining parts of the game
  def __getNextMoveDT(self, possMoves):
    #print "IN DESCISION TREE"
    bestScore = None
    bestMove = None
    try:
      for bar in possMoves:
        score, captured = self.board._getMoveScore(bar)
        if bestScore is None or score >= bestScore:
          if score == bestScore:
            choice = random.choice([True, False])
            if choice:
              continue 
          bestScore = score
          bestMove = bar
      return bestScore, bestMove
    except Exception as e:
      pdb.set_trace()

  def getMinMax(self, depth, maxPlayer, gameGUI, moves, alpha, beta):
    if depth == 0 or self.board.isGameOver():
      myScore = self.board.getScores()[self.playerNum]
      otherScore = self.board.getScores()[self.otherNum]
      return (myScore - otherScore), None

    hashMoves = str(map(lambda x: sorted(list(x)), moves))
    if hashMoves in self.movesTable[maxPlayer]:
      # print "FOUND IT"
      return self.movesTable[maxPlayer][hashMoves]

    possMoves = []
    for bar in gameGUI.bars:
      if not self.board.board.has_key(bar):
        possMoves.append(bar)

    if self.useDecisionTree:
      percentFilled = 1- float(len(possMoves)) / len(gameGUI.bars)
      if percentFilled <= 0.4:
        return self.__getNextMoveDT(possMoves)

    #Randomize the order of possible moves we explore
    random.shuffle(possMoves)

    bestMove = None
    if maxPlayer:
      bestValue = -sys.maxint
      for bar in possMoves:
        currPlayer = self.board.player
        completedSquare = self.board.play(bar)
        moves[currPlayer].add(bar)

        if completedSquare:
          v, _ = self.getMinMax(depth-1, maxPlayer, gameGUI, moves, alpha, beta)
        else:
          v, _ = self.getMinMax(depth-1, not maxPlayer, gameGUI, moves, alpha, beta)

        if v > bestValue:
          bestMove = bar
          bestValue = v
        self.board.unplay(bar, currPlayer)
        moves[currPlayer].remove(bar)

        alpha = max(alpha, v)
        if self.useDecisionTree and  beta <= alpha:
          # print "\n\n Pruning!\n\n"
          break

    else:
      bestValue = sys.maxint
      for bar in possMoves:
        currPlayer = self.board.player
        completedSquare = self.board.play(bar)
        moves[currPlayer].add(bar)

        if completedSquare:
          v, _ = self.getMinMax(depth-1, maxPlayer, gameGUI, moves, alpha, beta)
        else:
          v, _ = self.getMinMax(depth-1, not maxPlayer, gameGUI, moves, alpha, beta)

        if v < bestValue:
          bestMove = bar
          bestValue = v
        self.board.unplay(bar, currPlayer)
        moves[currPlayer].remove(bar)

        beta = min(beta, v)
        if self.useDecisionTree and beta <= alpha:
          # print "\n\n PRUNING! \n\n"
          break

    self.movesTable[maxPlayer][hashMoves] = (bestValue, bestMove)    
    return bestValue, bestMove

