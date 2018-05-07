import config, random
from board import GameBoard
import pdb
import numpy as np

class Environment():

	def __init__(self, size):

	  self.player = 0
	  self.playerA = 'human'
	  self.playerB = 'minimax'
	  self.depth = 5
	  self.useDecisionTree = 1
	  self.dynamicDepth = 1
	  self.board = GameBoard(size, size, self.playerA, self.playerB,
                                 self.depth, self.useDecisionTree,
                                 self.dynamicDepth)

          self.bars = {}
          self.width, self.height = self.board.width, self.board.height
          self.bars = self.board.bars

          # Parameters useful for NN.
          self.board_state_size =  (self.width-1) * self.height * 2
          


	def __step(self, move):

	  reward = 0

          playerNum, playerObj = self.board.getPlayer()

          assert playerNum == self.player

    	  board = self.board
    	  targets = board.play(move)
    	  if targets:
      	    for target in targets:
              board.scores[playerNum] += 1
              reward +=1

    	  if board.isGameOver():
    	    return board.board_state, reward, 1

    	  playerNum, playerObj = self.board.getPlayer()

          count = 0
          discount = 0.9

    	  while playerNum != self.player:
	    nextMove = playerObj.getNextMove(self)
              
	    targets = board.play(nextMove)
	    if targets:
	      for target in targets:
	        board.scores[playerNum] += 1 * (discount ** count)
	        reward -= 1 * (discount ** count)

	    if board.isGameOver():
    	      return board.board_state, reward, 1

    	    playerNum, playerObj = self.board.getPlayer()

	  return board.board_state, reward, -1

        def step(self, ind):
          if ind not in self.board.empty_states:
            # Bad move, punish
            print "Shouldn't be a bad move"
            return self.board.board_state, -self.board_state_size / 2, 0
          
          move = self.board.state_to_move[ind]
          return self.__step(move)

	def test_run(self):
	  finished = False

          reward = 0

	  while not finished:
	    playerNum, playerObj = self.board.getPlayer()
	    nextMove = playerObj.getNextMove(self)
	    s, r, finished = self.step(nextMove)
            reward += r
            assert reward == (self.board.scores[0] - self.board.scores[1])
	    #print s, r, finished


        def reset(self):
          size = self.width
          self.board = GameBoard(size, size, self.playerA, self.playerB,
                                 self.depth, self.useDecisionTree,
                                 self.dynamicDepth)
          
          return self.board.board_state

        def action_space_sample(self):
          num_left = len(self.board.empty_states)
          ind = int(random.random() * num_left)
          return list(self.board.empty_states)[ind]


        def test_board_state(self):
          prev = np.copy(self.board.board_state)
          for i in range(self.board_state_size):
            move = self.board.state_to_move[i]
            self.board._GameBoard__update_board_state(move)
            if (prev == self.board.board_state).all():
              pdb.set_trace()

            prev = np.copy(self.board.board_state)

          print self.board.board_state

          pdb.set_trace()


if __name__ == '__main__':
  env = Environment(5)
  env.test_board_state()















