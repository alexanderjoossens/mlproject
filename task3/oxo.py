
class OxoState:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player
    
    def is_terminal(self):
        # Check for a win
        for i in range(3):
            if self.board[i][0] != 0 and self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                return True
            if self.board[0][i] != 0 and self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                return True
        if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            return True
        if self.board[0][2] != 0 and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            return True
        # Check for a draw
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def evaluate(self):
        # Check for a win
        for i in range(3):
            if self.board[i][0] != 0 and self.board[i][0] == self.board[i][1] and self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == 'X':
                    return 1
                else:
                    return -1
            if self.board[0][i] != 0 and self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                if self.board[0][i] == 'X':
                    return 1
                else:
                    return -1
        if self.board[0][0] != 0 and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == 'X':
                return 1
            else:
                return -1
        if self.board[0][2] != 0 and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == 'X':
                return 1
            else:
                return -1
        # Otherwise, it's a draw
        return 0
    
    def make_move(self, move):
        i, j = move
        new_board = [row[:] for row in self.board]
        new_board[i][j] = 'X' if self.current_player == 0 else 'O'
        return OxoState(new_board, 1 - self.current_player)
    
    def get_possible_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves


def minimax(node, depth, maximizingPlayer, alpha, beta):
    if depth == 0 or node.is_terminal():
       