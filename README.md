# dots-and-boxes

Requires:
-Python Tk Inter (to install run: sudo apt-get install python-tk)

How to Run:

Player Type = {human, decision-tree, minimax}

Command = python main.py "board width" "board height" "player A type" "player B type" "search depth" "use dt heuristic = 0(no) or 1(yes)" "use dynamic depth heuristic = 0(no) or 1(yes)"


ex) 5 by 5 board with decision-tree(heuristic) + minimax(search depth=5, ab pruning) vs. decision-tree

>> python main.py 5 5 minimax decision-tree 5 1 0


ex) 7 by 7 board with dynamic depth(heuristic) + minimax(ab pruning) vs. decision-tree

>> python main.py 7 7 minimax decision-tree 5 1 1


ex) 7 by 7 board with dynamic depth(heuristic) + minimax(ab pruning) vs. human player

>> python main.py 7 7 minimax human 5 1 1
