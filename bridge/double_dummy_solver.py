from .models import Player, Trick

PLAYER_NS = {Player.NORTH, Player.SOUTH}


class GameState:
    def __init__(self, board, trump, starting_player):
        self.board = board
        self.trump = trump
        self.next_player = starting_player
        self.previous_tricks = []
        self.current_trick = Trick(trump, starting_player)
        self.ns_trick_count = 0

    def candidate_cards(self):
        current_suit = self.current_trick.trick_suit()
        return self.board.get_hand(self.next_player).candidate_cards(current_suit)

    def play_card(self, card):
        self.board.get_hand(self.next_player).play_card(card)

        trick_winner = self.current_trick.play_card(card)
        if trick_winner is None:
            self.next_player = self.next_player.next_player()
        else:
            self.next_player = trick_winner
            self.previous_tricks.append(self.current_trick)
            self.current_trick = Trick(self.trump, trick_winner)
            if trick_winner in PLAYER_NS:
                self.ns_trick_count += 1

    def step_back(self):
        last_card = self.current_trick.step_back()
        if last_card is None:
            self.current_trick = self.previous_tricks.pop()
            if self.next_player in PLAYER_NS:
                self.ns_trick_count -= 1
            self.next_player = self.current_trick.starting_player.previous_player()
            last_card = self.current_trick.step_back()
        else:
            self.next_player = self.next_player.previous_player()
        self.board.get_hand(self.next_player).add_card(last_card)


def double_dummy_solver(board, trump, starting_player):
    return double_dummy_solver_using_gameState(GameState(board, trump, starting_player))


def double_dummy_solver_using_gameState(gameState, alpha=0, beta=13):
    candidate_cards = gameState.candidate_cards()

    if gameState.next_player in PLAYER_NS:
        max_trick = 0

        # For end case
        try:
            card = next(candidate_cards)
            gameState.play_card(card)
            max_trick = max(max_trick, double_dummy_solver_using_gameState(gameState, alpha=alpha, beta=beta))
            gameState.step_back()
        except StopIteration:
            return gameState.ns_trick_count

        for card in candidate_cards:
            alpha = max(alpha, max_trick)
            if alpha >= beta:
                break

            gameState.play_card(card)
            max_trick = max(max_trick, double_dummy_solver_using_gameState(gameState, alpha=alpha, beta=beta))
            gameState.step_back()
        return max_trick
    else:
        min_trick = 13

        # For end case
        try:
            card = next(candidate_cards)
            gameState.play_card(card)
            min_trick = min(min_trick, double_dummy_solver_using_gameState(gameState, alpha=alpha, beta=beta))
            gameState.step_back()
        except StopIteration:
            return gameState.ns_trick_count

        for card in candidate_cards:
            beta = min(beta, min_trick)
            if alpha >= beta:
                break

            gameState.play_card(card)
            min_trick = min(min_trick, double_dummy_solver_using_gameState(gameState, alpha=alpha, beta=beta))
            gameState.step_back()
        return min_trick
