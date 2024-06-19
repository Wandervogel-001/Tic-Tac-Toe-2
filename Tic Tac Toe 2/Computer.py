import random

# Function to check for the winner
def check_winner(board):
    # Check rows
    for i in range(0, 7, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            return board[i]
    # Check columns
    for i in range(0, 3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            return board[i]
    # Check diagonals
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]
    return None


# Function to search for empty_indices
def empty_indices(board):
    return [i for i, spot in enumerate(board) if spot == ' ']


# Function for evaluating the board
def evaluate(board, depth, player_symbol, opponent):
    winner = check_winner(board)

    if winner == player_symbol:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif ' ' not in board[1:]:
        return 0

class Computer():
	def __init__(self, player_symbol, computer_symbol, difficulty):
		super().__init__()
		self.player_symbol = player_symbol
		self.computer_symbol = computer_symbol
		self.difficulty = difficulty

	# Function for Minimax Algorithm
	def minimax(self, board, depth, maximizingPlayer):
	    if check_winner(board) or ' ' not in board[1:]:
	        return evaluate(board, depth, self.computer_symbol, self.player_symbol) # Evaluate the move
	    depth += 1

	    if maximizingPlayer:
	        max_eval = float('-inf')
	        for move in empty_indices(board):
	            board[move] = self.computer_symbol
	            evaluation = self.minimax(board, depth, False) # Call the minimax function recursivly to evaluate the move
	            board[move] = ' '
	            max_eval = max(max_eval, evaluation)
	        return max_eval
	    else:
	        min_eval = float('inf')
	        for move in empty_indices(board):
	            board[move] = self.player_symbol
	            evaluation = self.minimax(board, depth, True)
	            board[move] = ' '
	            min_eval = min(min_eval, evaluation)
	        return min_eval


	# Function to get the computer's move in Easy Difficulty
	def get_random_computer_move(self, board):
		move = random.choice(empty_indices(board))
		return move


	# Function for getting the computer's move in Normal Difficulty
	def get_easy_computer_move(self, board):
	    # Check if there's a winning move
	    for move in empty_indices(board):
	        board[move] = self.computer_symbol
	        if check_winner(board):
	            board[move] = ' '
	            return move
	        board[move] = ' '
	    # If not, play randomly
	    return self.get_random_computer_move(board)


	# Function for getting the computer's move in Hard Difficulty
	def get_normal_computer_move(self, board):
		# Check if there's a winning or a defensive move
		for symbol in [self.player_symbol, self.computer_symbol]:
			for move in empty_indices(board):
				board[move] = symbol
				if check_winner(board):
					board[move] = ' '
					return move
				board[move] = ' '
			# If not, play randomly
			return self.get_random_computer_move(board)


	# Function to get the computer's move in Impossible Diffuclty
	def get_hard_computer_move(self, board):
		# If the board is empty, make a random move
		if len(empty_indices(board)) == 9:
			return self.get_random_computer_move(board)
		else:
			# Implement the minimax algorithm using the provided logic
			best_move = 0
			best_score = float('-inf')

			for move in empty_indices(board):
				board[move] = self.computer_symbol
				score = self.minimax(board, 1, False)
				board[move] = ' '

				if score > best_score:
					best_score = score
					best_move = move

			return best_move

	# Function for getting the computer's move
	def get_computer_move(self, board):
		if self.difficulty == 1:
			return self.get_random_computer_move(board)
		elif self.difficulty == 2:
			return self.get_easy_computer_move(board)
		elif self.difficulty == 3:
			return self.get_normal_computer_move(board)
		elif self.difficulty == 4:
			return self.get_hard_computer_move(board)

	def update(self, board):
		move = self.get_computer_move(board)
		board[move] = self.computer_symbol