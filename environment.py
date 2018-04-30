
import config, random
from board import GameBoard

def cartesian( v1, v2 ):
  """ Helper function
  returns cartesian product of the two
  'sets' v1, v2"""
  return tuple([(x,y) for x in v1 for y in v2])

def right(x):
  """Helper function: argument x must be a dot.
  Returns dot right of x."""
  return (x[0]+1,x[1])


def upper(x):
  """Helper function: argument x must be a dot.
  Returns dot above (actually below) x."""
  return (x[0], x[1]+1)


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
          self.board_state_size =  (self.width-1) * self.height * 2

          self.state_to_move = {}
          self.move_to_state = {}

	  for dot in cartesian(range(self.width), range(self.height)):
	    if dot[0] < self.width - 1:
              move = (dot, right(dot))
              ind = self.__convert_move_to_state(move)
              self.state_to_move[ind] = move
              self.move_to_state[move] = ind
	      self.bars[move] = None
	    if dot[1] < self.height - 1:
              move = (dot, upper(dot))
              ind = self.__convert_move_to_state(move)
              self.state_to_move[ind] = move
              self.move_to_state[move] = ind
	      self.bars[move] = None

          self.board.move_to_state = self.move_to_state

        def __convert_move_to_state(self, move):
          if move[0][1] == move[1][1]:
            # Right move
            ind = move[0][1]* (2 * self.width - 1) + move[0][0]
          else:
            # Upper move
            ind = ((move[1][1] -1) * self.width +
                   move[1][1] * (self.width -1) + move[0][0])
          return ind


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
    	    return board.board_state, reward, True

    	  playerNum, playerObj = self.board.getPlayer()

    	  while playerNum != self.player:
	    nextMove = playerObj.getNextMove(self)
              
	    targets = board.play(nextMove)
	    if targets:
	      for target in targets:
	        board.scores[playerNum] += 1
	        reward -= 1

	    if board.isGameOver():
    	      return board.board_state, reward, True

    	    playerNum, playerObj = self.board.getPlayer()

	  return board.board_state, reward, False

        def step(self, ind):
          if self.board.board_state[0][ind] != 0:
            # Bad move, punish
            return self.board.board_state, -self.board_state_size / 2, False
          
          move = self.state_to_move[ind]
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
          
          self.board.move_to_state = self.move_to_state

          return self.board.board_state

        def action_space_sample(self):
          num_left = len(self.board.empty_states)
          ind = int(random.random() * num_left)

          for action in self.board.empty_states:
            if ind == 0:
              return action
            else:
              ind -= 1

          pdb.set_trace()


if __name__ == '__main__':
  env = Environment(3)
  env.test_run()















