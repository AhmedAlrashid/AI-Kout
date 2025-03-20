# game.py

import random
from player import Player  # Import the Player class from player.py

# Define the ranks and suits.
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7']
suits = ['♥', '♣', '♦', '♠']

# Build the deck:
# Create cards for each suit, remove the 7♦, and add a Joker.
cards = {suit: [f"{rank}{suit}" for rank in ranks] for suit in suits}
cards['♦'].remove('7♦')
cards['J'] = ['Joker']  # Using 'J' as key for the Joker group.
deck = [card for suit_cards in cards.values() for card in suit_cards]

# Define rank values for comparison (higher value means stronger card).
RANK_VALUES = {'A': 8, 'K': 7, 'Q': 6, 'J': 5, '10': 4, '9': 3, '8': 2, '7': 1}


def beats(card1, card2, lead_suit, trump_suit):
    """
    Returns True if card1 beats card2, given the lead suit and trump suit.
    
    Rules:
      - The Joker always beats any other card.
      - If card2 is the Joker, nothing beats it.
      - A trump card (e.g. hearts) beats any card that is not trump.
      - If both cards are trump, the one with the higher rank wins.
      - If neither card is trump, then if card1 follows the lead suit and card2 does not, card1 wins.
      - If both follow the lead suit, the card with the higher rank wins.
      - Otherwise, card1 does not beat card2.
    """
    # Joker cases.
    if card1 == "Joker":
        return True
    if card2 == "Joker":
        return False

    suit1 = card1[-1]
    suit2 = card2[-1]
    
    # Check for trump.
    if suit1 == trump_suit and suit2 != trump_suit:
        return True
    if suit1 != trump_suit and suit2 == trump_suit:
        return False
    if suit1 == trump_suit and suit2 == trump_suit:
        return RANK_VALUES.get(card1[:-1], 0) > RANK_VALUES.get(card2[:-1], 0)
    
    # Neither card is trump.
    # If card1 follows lead suit and card2 doesn't, card1 wins.
    if suit1 == lead_suit and suit2 != lead_suit:
        return True
    if suit1 != lead_suit and suit2 == lead_suit:
        return False
    if suit1 == lead_suit and suit2 == lead_suit:
        return RANK_VALUES.get(card1[:-1], 0) > RANK_VALUES.get(card2[:-1], 0)
    
    # If neither card is trump or lead suit, then card1 does not beat card2.
    return False


class Game:
    def __init__(self, num_players=4, cards_per_player=8):
        self.num_players = num_players
        self.cards_per_player = cards_per_player
        self.deck = deck.copy()  # Work with a copy of the deck.
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.defining_suit = None  # Overall trump (e.g., hearts).
        self.rounds_to_win = 0
        self.player_to_beat = None

    def shuffle_and_deal(self):
        """Shuffle the deck and deal cards to each player."""
        random.shuffle(self.deck)
        for i in range(self.cards_per_player * self.num_players):
            player = self.players[i % self.num_players]
            player.add_card(self.deck[i])

    def show_hands(self):
        """Display each player's hand."""
        for player in self.players:
            print(player)

    def determine_current_suit(self, card):
        """
        Determine the suit for the trick based on the given card.
        (e.g., '7♦' -> '♦').
        """
        # We assume the card is not the Joker for leading.
        return card[-1]

    def determine_bigger_suit(self):
        """
        Loop through all players to decide who will define the trump suit.
        Each player must bid higher than the current maximum (starting at 5).
        The player with the highest valid bid gets to choose the trump suit.
        """
        current_suiter = None
        current_rounds = 5  # Starting bid.

        for p in self.players:
            current_suiter, current_rounds = p.potential_suit(current_suiter, current_rounds)

        if current_suiter:
            suit = input(f"{current_suiter}, what suit would you like to define for the game? ")
            print(f"{current_suiter} has chosen {suit} as trump!")
            self.defining_suit = suit
            self.suiter = current_suiter  # <-- Store the winning player's name.
            return suit
        else:
            print("No one made a valid bid. Defaulting trump suit to '♣'.")
            self.defining_suit = '♣'
            return '♣'


    def play_trick(self):
        """
        Play one trick (small round).
        The player immediately to the right of the suiter starts the trick.
        """
        if self.defining_suit is None:
            print("Trump suit not set. Cannot play trick.")
            return

        if not hasattr(self, "suiter"):
            print("No suiter; cannot determine starting player. Aborting trick.")
            return

        # Find the index of the suiter.
        suiter_index = next(i for i, p in enumerate(self.players) if p.name == self.suiter)
        starting_index = (suiter_index + 1) % self.num_players

        # First player leads; no lead suit is enforced.
        current_winner = None
        winning_card = None
        lead_suit = None

        print("\n--- Starting a new trick ---")
        for i in range(self.num_players):
            player_index = (starting_index + i) % self.num_players
            player = self.players[player_index]
            # For the lead player, allow any card.
            if i == 0:
                print(f"{player.name}, it's your turn to lead.")
                print("Your hand:", player.hand)
                while True:
                    card = input("Choose a card to play: ")
                    if card in player.hand:
                        # If the card is Joker, disallow as lead.
                        if card == "Joker":
                            print("Cannot lead with the Joker. Please choose another card.")
                        else:
                            player.hand.remove(card)
                            current_winner = player
                            winning_card = card
                            lead_suit = self.determine_current_suit(card)
                            print(f"{player.name} leads with {card}. (Lead suit: {lead_suit})")
                            break
                    else:
                        print("You don't have that card. Try again.")
            else:
                # For subsequent players, enforce following the lead suit if possible.
                legal_cards = player.possible_cards(lead_suit)
                print(f"{player.name}, it's your turn. Your legal cards: {legal_cards}")
                while True:
                    card = input("Choose a card to play: ")
                    if card in player.hand:
                        # If the card is not in legal cards and legal cards is not the whole hand, disallow.
                        if card not in legal_cards and set(legal_cards) != set(player.hand):
                            print(f"You must follow suit ({lead_suit}) if possible. Try again.")
                        else:
                            player.hand.remove(card)
                            print(f"{player.name} plays {card}.")
                            # Determine if this card beats the current winning card.
                            if beats(card, winning_card, lead_suit, self.defining_suit):
                                current_winner = player
                                winning_card = card
                            break
                    else:
                        print("You don't have that card. Try again.")

        print(f"\n{current_winner.name} wins the trick with {winning_card}!")
        return current_winner

# if __name__ == "__main__":
#     game = Game()
#     game.shuffle_and_deal()
#     game.show_hands()
#     trump = game.determine_bigger_suit()
#     print("Trump suit is:", trump)
#     # Play one trick.
#     game.play_trick()
