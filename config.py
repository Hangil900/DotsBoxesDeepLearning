PLAYER_TYPE_HUMAN = 'human'
PLAYER_TYPE_DT = 'decision-tree'
PLAYER_TYPE_MM = 'minimax'
PLAYER_TYPE_DQN = 'dqn'

MAX_MOVES = 2500000
STATS = "STATS.csv"
STATS_T = "STATS-True.csv"
STATS_F = "STATS-False.csv"
STATS_FILE = 'STATS.csv'
STATS= [STATS_T, STATS_F, STATS_FILE]

PLAYER_TYPES = [PLAYER_TYPE_HUMAN, PLAYER_TYPE_DT,
                PLAYER_TYPE_MM, PLAYER_TYPE_DQN]
PLAYER_TYPES_BOT = [PLAYER_TYPE_DT, PLAYER_TYPE_MM, PLAYER_TYPE_DQN]
DRAW = 'DRAW'



# DQN configurations

DQN_path = "./dqn2"

DQN_h_size = 256
DQN_width = 5
DQN_height = 5
DQN_state_size = (DQN_width - 1) * DQN_height * 2
DQN_batch_size = 32
DQN_update_freq = 4
DQN_num_episodes = 10000
DQN_pre_train_steps = 500

DQN_handle_invalid_moves = False
DQN_use_minimax_moves = True

# Eddy use:

# Case 1:
# DQN_use_minimax_moves = False
# num_episodes = 20000
# num_pre_train_steps = 20000

# Case 2:
# Make sure to change DQN_path name
# DQN_use_minimax_moves = False
# DQN_num_episodes = 20000
# DQN_num_pre_train_steps = 10000
