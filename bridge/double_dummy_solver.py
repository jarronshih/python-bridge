from .models import GameState, Player


def double_dummy_solver(board, trump, starting_player):
    return double_dummy_solver_using_gameState(GameState(board, trump, starting_player))


def double_dummy_solver_using_gameState(gameState):
    next_player = gameState.next_player
    candidate_cards = gameState.candidate_cards()

    if len(candidate_cards) == 0:
        return gameState.ns_trick_count

    if next_player == Player.NORTH or next_player == Player.SOUTH:
        max_trick = 0
        for card in candidate_cards:
            gameState.play_card(card)
            max_trick = max(max_trick, double_dummy_solver_using_gameState(gameState))
            gameState.step_back()
        return max_trick
    else:
        min_trick = 13
        for card in candidate_cards:
            gameState.play_card(card)
            min_trick = min(min_trick, double_dummy_solver_using_gameState(gameState))
            gameState.step_back()
        return min_trick
