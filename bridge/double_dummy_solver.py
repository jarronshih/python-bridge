def double_dummy_solver(board, trump, starting_player):
    return double_dummy_solver_using_gameState(GameState(board, trump, starting_player))

def double_dummy_solver_using_gameState(gameState):
    current_player = gameState.current_player
    candidate_cards = gameState.candidate();
    
    if candidate_cards.length == 0:
        return gameState.ns_trick_count
    
    if current_player == Player.NORTH or current_player == Player.SOUTH:
        max_trick = 0
        for card in candidate_cards:
            max_trick = max(max_trick, gameState.play_card(card))
            gameState.step_back()
        return max_trick
    else:
        min_trick = 13
        for card in candidate_cards:
            min_trick = min(min_trick, gameState.play_card(card))
            gameState.step_back()
        return min_trick
    
