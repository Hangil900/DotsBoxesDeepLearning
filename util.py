import config, pdb
from matplotlib import pyplot as plt



def parseTimeStats():
	statsDict = {}
	for filename in config.STATS:
		with open(filename, 'r') as f:
			lines = f.readlines()
			index = 0
			while(index +2 < len(lines)):
				lineA = lines[index].split(',')
				if len(lineA) == 7:
					statsLine = lineA
					scoreLine = lines[index+1].split(',')
					time = float(lines[index+2].strip())

					board = (int(statsLine[0]), int(statsLine[1]))
					playerA = statsLine[2].strip()
					playerB = statsLine[3].strip()
					depth = int(statsLine[4])
					scoreA = int(scoreLine[1])
					scoreB = int(scoreLine[3])
					useTree = int(statsLine[5])
					useDynamic = int(statsLine[6])

					if useDynamic:
						depth = -1
					if not board in statsDict:
						statsDict[board] = {}

					if not depth in statsDict[board]:
						statsDict[board][depth] = {}
						statsDict[board][depth][0] = [[], []]
						statsDict[board][depth][1] = [[], []]
						statsDict[board][depth][2] = [[], []]

					if filename == config.STATS_F:
						statsDict[board][depth][0][0].append(time)
						statsDict[board][depth][0][1].append(scoreB)
					elif filename == config.STATS_T:
						statsDict[board][depth][1][0].append(time)
						statsDict[board][depth][1][1].append(scoreB)

					else:
						statsDict[board][depth][2][0].append(time)
						statsDict[board][depth][2][1].append(scoreB)

					index += 3
				else:
					index += 1

	print "-----------------------TIMING STATS---------------------\n\n"
	allX = []
	allY = []
	boardOrder = []
	for board in statsDict:
		Y = []
		X = []
		if board[0] <= 6:
			boardOrder.append(board[0])
		else:
			continue
		for depth in statsDict[board]:
			if depth == 5:
				for useTree in statsDict[board][depth]:
					try:
						X.append(useTree)
						currDict = statsDict[board][depth][useTree]
						avgTime = sum(currDict[0]) / len(currDict[0])
						totalScore = sum(currDict[1])
						totalTime = sum(currDict[0])
						timePerScore = totalTime/ totalScore
						Y.append(timePerScore)
						print "Board: %s, depth: %d, useTree: %s, Avg TIME: %f" % (str(board), depth, str(useTree), avgTime)
					except Exception as e:
						pdb.set_trace()
		allY.append(Y)
		allX.append(X)

	print allX
	print allY
	print boardOrder
	colors = ['red', 'blue', 'yellow', 'black']
	plt.figure()

	for i in range(len(allX)):
		scattered = plt.scatter(allX[i], allY[i], colors = colors[i])

	plt.legend((notTree, useTree),
       ('normal', 'useTree'),
       scatterpoints=1,
       loc='lower right',
       ncol=2,
       fontsize=8)

	plt.xlabel('Depth')
	plt.ylabel('Score Difference')
	title = 'Minimax Normalized Score Diff: %s' % (str(board))
	plt.title( title)
	plt.savefig("./plots/scoreDiff/%s.png" %(title) )

def parseStats():
	statsDict = {}
	for filename in config.STATS[2:]:
		with open(filename, 'r') as f:
			lines = f.readlines()
			index = 0
			while(index +2 < len(lines)):
				lineA = lines[index].split(',')
				if len(lineA) == 7:
					statsLine = lineA
					scoreLine = lines[index+1].split(',')
					time = float(lines[index+2].strip())

					board = (int(statsLine[0]), int(statsLine[1]))
					playerA = statsLine[2].strip()
					playerB = statsLine[3].strip()
					depth = int(statsLine[4])
					scoreA = int(scoreLine[1])
					scoreB = int(scoreLine[3])
					useTree = int(statsLine[5])
					useDynamic = int(statsLine[6])
					if useDynamic:
						depth = -1

					if not board in statsDict:
						statsDict[board] = {}

					if not depth in statsDict[board]:
						statsDict[board][depth] = {}

					if not useTree in statsDict[board][depth]:
						statsDict[board][depth][useTree] = {}
						statsDict[board][depth][useTree]['entries'] = []
						statsDict[board][depth][useTree]['wins'] = {playerA: 0, playerB: 0, config.DRAW: 0}
						statsDict[board][depth][useTree]['time'] = []



					entry = ((playerA, scoreA), (playerB, scoreB))
					statsDict[board][depth][useTree]['entries'].append(entry)
					statsDict[board][depth][useTree]['time'].append(time)

					index += 3
				else:
					index += 1

	print "\n\n ----------WINNING STATS------------ \n\n"
	for board in statsDict:
		for depth in statsDict[board]:
			for useTree in statsDict[board][depth]:
				currDict = statsDict[board][depth][useTree]
				entries = currDict['entries']
				wins = currDict['wins']
				totalA = 0
				totalB = 0
				for ((playerA, scoreA), (playerB, scoreB)) in entries:
					if not playerA in wins:
						print playerA
						wins[playerA] = 0
					if not playerB in wins:
						print playerB
						wins[playerB] = 0
					if not config.DRAW in wins:
						wins[config.DRAW] = 0

					if scoreA > scoreB:
						wins[playerA] +=1
					if scoreA < scoreB:
						wins[playerB] +=1
						
					else:
						wins[config.DRAW] +=1


					totalA += scoreA
					totalB += scoreB

				avgDiff = float(totalB- totalA) / len(entries)

				currDict['wins'] = wins

				if (wins[playerB]) > (wins[playerA]):
					currDict['winner'] = config.PLAYER_TYPE_MM
				elif wins[playerB] < wins[playerA]:
					currDict['winner'] = config.PLAYER_TYPE_DT
				else:
					currDict['winner'] = "draw"

				avgDiff = avgDiff / ((board[0] -1) ** 2)
				currDict['avgDiff'] = avgDiff
				winningPercentage = float(wins[playerB]) / (len(entries))
				currDict['winRate'] = winningPercentage

				print "Board: %s, depth: %d, useTree: %s, wins: %s, avg score diff: %f, winning rates: %f" % (str(board), depth, str(useTree), str(wins), avgDiff, winningPercentage)

	print "\n\n ----------TIMING STATS------------ \n\n"
	for board in statsDict:
		for depth in statsDict[board]:
			for useTree in statsDict[board][depth]:
				currDict = statsDict[board][depth][useTree]
				avgTime = sum(currDict['time']) / len(currDict['time'])
				print "Board: %s, depth: %d, useTree: %s, Avg TIME: %f" % (str(board), depth, str(useTree), avgTime)

	# pdb.set_trace()
	return statsDict

def getDepthAvgScorePlots():
	statsDict = parseStats()

	for board in statsDict:
		X = []
		Y_avgDiff = [[],[]]
		Y_winRate = [[],[]]
		for depth in statsDict[board]:
			if depth == -1:
				continue
			X.append(depth)
			for useTree in statsDict[board][depth]:
				currDict = statsDict[board][depth][useTree]
				Y_avgDiff[useTree].append(currDict['avgDiff'])
				Y_winRate[useTree].append(currDict['winRate'])

		try:
			plt.figure()
			notTree = plt.scatter(X,Y_avgDiff[0],color='red')
			useTree = plt.scatter(X,Y_avgDiff[1],color='blue')
			
			plt.legend((notTree, useTree),
	           ('normal', 'useTree'),
	           scatterpoints=1,
	           loc='lower right',
	           ncol=2,
	           fontsize=8)

			plt.xlabel('Depth')
			plt.ylabel('Average Score Difference')
			title = 'Minimax Normalized Avg Score Diff: %s' % (str(board))
			plt.title( title)
			plt.savefig("./plots/scoreDiff/%s.png" %(title) )

			plt.figure()
			notTree= plt.scatter(X,Y_winRate[0],color='red')
			useTree = plt.scatter(X,Y_winRate[1],color='blue')
			
			plt.legend((notTree, useTree),
	           ('normal', 'useTree'),
	           scatterpoints=1,
	           loc='lower right',
	           ncol=2,
	           fontsize=8)

			plt.xlabel('Depth')
			plt.ylabel('Average Win Rate')
			title = 'Minimax Avg Win Rate %s' % (str(board))
			plt.title(title)
			plt.savefig("./plots/winRate/%s.png" % (title) )
		except Exception as e:
			pass
			# pdb.set_trace()

def getDepthScorePlots():
	statsDict = parseStats()
	for board in statsDict:
		X = [[],[]]
		Y_Diff = [[],[]]
		for depth in statsDict[board]:
			if depth == -1:
				continue
			for useTree in statsDict[board][depth]:
				currDict = statsDict[board][depth][useTree]
				for ((playerA, scoreA), (playerB, scoreB)) in currDict['entries']:
					X[useTree].append(depth)
					diff = float(scoreB - scoreA) / ((board[0] -1) **2)
					Y_Diff[useTree].append(diff)

		try:
			plt.figure()
			notTree = plt.scatter(X[0],Y_Diff[0],color='red', alpha = 0.3)
			useTree = plt.scatter(X[1],Y_Diff[1],color='blue', alpha = 0.3)
			
			plt.legend((notTree, useTree),
	           ('normal', 'useTree'),
	           scatterpoints=1,
	           loc='lower right',
	           ncol=2,
	           fontsize=8)

			plt.xlabel('Depth')
			plt.ylabel('Score Difference')
			title = 'Minimax Normalized Score Diff: %s' % (str(board))
			plt.title( title)
			plt.savefig("./plots/scoreDiff/%s.png" %(title) )

		except Exception as e:
			pdb.set_trace()
			pass

def getBoardDepthPlot():
	statsDict = parseStats()
	X = [[], [], []]
	Y = [[], [], []]
	for board in statsDict:
		for depth in statsDict[board]:
			if depth == -1:
				continue
			for useTree in statsDict[board][depth]:
				currDict = statsDict[board][depth][useTree]

				if not useTree:
					if currDict['winner'] == config.PLAYER_TYPE_DT:
						Y[0].append(board[0])
						X[0].append(depth)		
					elif currDict['winner'] == config.PLAYER_TYPE_MM:
						Y[1].append(board[0])
						X[1].append(depth)
					else:
						Y[2].append(board[0])
						X[2].append(depth)

				# for ((playerA, scoreA), (playerB, scoreB)) in currDict['entries']:
				# 	if scoreA > scoreB:
				# 		Y[0].append(board[0])
				# 		X[0].append(depth)
				# 	if scoreA < scoreB:
				# 		Y[1].append(board[0])
				# 		X[1].append(depth)
				# 	else:
				# 		Y[2].append(board[0])
				# 		X[2].append(depth)

	try:
		# pdb.set_trace()
		plt.figure()
		losses = plt.scatter(X[0],Y[0],color='red', alpha= 1)
		wins = plt.scatter(X[1],Y[1],color='blue', alpha=1 )
		draws = plt.scatter(X[2],Y[2] ,color='grey', alpha=1)


		plt.legend((wins, losses, draws),
           ('wins', 'losses', 'draws'),
           scatterpoints=1,
           loc='lower right',
           ncol=2,
           fontsize=8)

		plt.xlabel('Depth')
		plt.ylabel('Board Size')
		title = 'Board Size vs. Depth'
		plt.title( title)
		plt.savefig("./plots/%s.png" %(title) )

	except Exception as e:
		pdb.set_trace()	
		pass


if __name__ == '__main__':
	# getDepthAvgScorePlots()
	# getDepthScorePlots()
	# getBoardDepthPlot()
	parseStats()
	# parseTimeStats()
