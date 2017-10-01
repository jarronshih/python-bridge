from .models import Player, Trick


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
            if trick_winner in [Player.NORTH, Player.SOUTH]:
                self.ns_trick_count += 1

    def step_back(self):
        last_card = self.current_trick.step_back()
        if last_card is None:
            self.current_trick = self.previous_tricks.pop()
            if self.next_player == Player.NORTH or self.next_player == Player.SOUTH:
                self.ns_trick_count -= 1
            self.next_player = self.current_trick.starting_player.previous_player()
            last_card = self.current_trick.step_back()
        else:
            self.next_player = self.next_player.previous_player()
        self.board.get_hand(self.next_player).add_card(last_card)


def double_dummy_solver(board, trump, starting_player):
    return double_dummy_solver_using_gameState(GameState(board, trump, starting_player))


def double_dummy_solver_using_gameState(gameState):
    next_player = gameState.next_player
    candidate_cards = gameState.candidate_cards()

    if len(candidate_cards) == 0:
        return gameState.ns_trick_count

    if next_player in [Player.NORTH, Player.SOUTH]:
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
