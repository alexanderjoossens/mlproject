import math

def minimax(node, depth, maximizingPlayer, alpha, beta):
    if depth == 0 or node.is_terminal():
        return node.evaluate(), None

    if maximizingPlayer:
        value = -math.inf
        best_move = None
        for move in node.get_possible_moves():
            child_node = node.make_move(move)
            child_value, _ = minimax(child_node, depth - 1, False, alpha, beta)
            if child_value > value:
                value = child_value
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = math.inf
        best_move = None
        for move in node.get_possible_moves():
            child_node = node.make_move(move)
            child_value, _ = minimax(child_node, depth - 1, True, alpha, beta)
            if child_value < value:
                value = child_value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move

if __name__ == "__main__":
    # Define the board
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    # Define the players
    players = ["X", "O"]
    # Define the current player
    current_player = 0
    # Define the current state
    current_state = State(board, current_player)
    # Define the depth
    depth = 2
    # Define the alpha and beta values
    alpha = -math.inf
    beta = math.inf
    # Find the best move
    value, move = minimax(current_state, depth, True, alpha, beta)
    # Print the best move
    print(move)


    import math
