from config import *
from BotDecisionTree import BotDecisionTree
from BotMinimax import BotMinimax
from BotConvNet import BotConvNet

import pdb

class Player:

  def __init__(self, boardObj, playerType, playerNum, depth, useDecisionTree, dynamicDepth):

    if not playerType in PLAYER_TYPES:
      raise ValueError('invalid bot player type')

    if not boardObj:
      raise ValueError('invalid board object')

    self.board = boardObj
    self.playerType = playerType
    self.bot = None

    if playerType == PLAYER_TYPE_DT:
      self.bot = BotDecisionTree(boardObj)
    elif playerType == PLAYER_TYPE_MM:
      self.bot = BotMinimax(boardObj, playerNum, depth, useDecisionTree, dynamicDepth)
    elif playerType == PLAYER_TYPE_CN:
      self.bot = BotConvNet(boardObj, playerNum)
    else: # human player
      pass


  def getPlayerType(self):
    return self.playerType

  def getNextMove(self, gameGUI):
    if self.bot:
      #print 'bot player get Next Move'
      return self.bot.getNextMove(gameGUI) # returns an object with x and y

    return None # human player, return None

