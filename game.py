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
      - A trump card beats any card that is not trump.
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
    if suit1 == lead_suit and suit2 != lead_suit:
        return True
    if suit1 != lead_suit and suit2 == lead_suit:
        return False
    if suit1 == lead_suit and suit2 == lead_suit:
        return RANK_VALUES.get(card1[:-1], 0) > RANK_VALUES.get(card2[:-1], 0)
    
    return False


class Game:
    def __init__(self, num_players=4, cards_per_player=8):
        self.num_players = num_players
        self.cards_per_player = cards_per_player
        self.deck = deck.copy()  # Work with a copy of the deck.
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.defining_suit = None  # Overall trump suit.
        self.suiter = None         # Winning bidder (used for determining first trick).
        self.bid_value = 5         # The bid (target) that the bidding team must meet.
        # Track team wins: team A: players 1 & 3, team B: players 2 & 4.
        self.team_wins = {"A": 0, "B": 0}

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
            self.suiter = current_suiter
            self.bid_value = current_rounds  # The bid becomes the target.
            return suit
        else:
            print("No one made a valid bid. Defaulting trump suit to '♣'.")
            self.defining_suit = '♣'
            self.suiter = None
            return '♣'

    def play_trick(self, starting_index):
        """
        Play one trick (small round) starting from the provided player index.
        The first player leads (cannot lead with Joker) and their card sets the lead suit.
        Subsequent players must follow suit if possible.
        Returns the index of the trick winner.
        """
        if self.defining_suit is None:
            print("Trump suit not set. Cannot play trick.")
            return None

        current_winner = None
        winning_card = None
        lead_suit = None

        print("\n--- Starting a new trick ---")
        for i in range(self.num_players):
            player_index = (starting_index + i) % self.num_players
            player = self.players[player_index]
            # Lead player
            if i == 0:
                print(f"{player.name}, it's your turn to lead.")
                print("Your hand:", player.hand)
                while True:
                    card = input("Choose a card to play: ")
                    if card in player.hand:
                        if card == "Joker":
                            print("Cannot lead with the Joker. Please choose another card.")
                        else:
                            player.hand.remove(card)
                            current_winner = player_index
                            winning_card = card
                            lead_suit = self.determine_current_suit(card)
                            print(f"{player.name} leads with {card}. (Lead suit: {lead_suit})")
                            break
                    else:
                        print("You don't have that card. Try again.")
            else:
                legal_cards = player.possible_cards(lead_suit)
                print(f"{player.name}, it's your turn. Your legal cards: {legal_cards}")
                while True:
                    card = input("Choose a card to play: ")
                    if card in player.hand:
                        if card not in legal_cards and set(legal_cards) != set(player.hand):
                            print(f"You must follow suit ({lead_suit}) if possible. Try again.")
                        else:
                            player.hand.remove(card)
                            print(f"{player.name} plays {card}.")
                            # Determine if this card beats the current winning card.
                            if beats(card, winning_card, lead_suit, self.defining_suit):
                                current_winner = player_index
                                winning_card = card
                            break
                    else:
                        print("You don't have that card. Try again.")
        winner = self.players[current_winner]
        print(f"\n{winner.name} wins the trick with {winning_card}!")
        # Update team wins.
        if winner.name in ["Player 1", "Player 3"]:
            self.team_wins["A"] += 1
        else:
            self.team_wins["B"] += 1
        for p in self.players:
            print(f"{p.name} hand: {p.hand}")
        return current_winner

    def play_game(self):
        """
        Play the full game.
        - First, determine trump via bidding.
        - Then play up to as many tricks as there are cards per player.
        - The first trick is played starting with the player to the right of the suiter.
        - Each subsequent trick is led by the winner of the previous trick.
        - After each trick, check if the bidding team has reached their bid or if it is impossible for them to do so.
        - At the end, if the bidding team wins at least as many tricks as their bid, they win the game;
        otherwise, the opposing team wins.
        """
        trump = self.determine_bigger_suit()
        print("Trump suit is:", trump)

        # Determine the bidding team.
        if self.suiter in ["Player 1", "Player 3"]:
            bidding_team = "A"
            other_team = "B"
        else:
            bidding_team = "B"
            other_team = "A"

        print(f"Bidding team is Team {bidding_team} with target {self.bid_value} tricks.")

        total_rounds = self.cards_per_player

        # Set starting index for the first trick.
        if self.suiter is not None:
            suiter_index = next(i for i, p in enumerate(self.players) if p.name == self.suiter)
            starting_index = (suiter_index + 1) % self.num_players
        else:
            # If no one bid, arbitrarily start with Player 1.
            starting_index = 0

        # Play one trick per card in hand, with early termination check.
        for trick in range(total_rounds):
            print(f"\n--- Trick {trick+1} ---")
            starting_index = self.play_trick(starting_index)
            if starting_index is None:
                break  # Abort if trick couldn't be played.

            # Check early termination conditions.
            remaining_rounds = total_rounds - (trick + 1)
            current_bidding_wins = self.team_wins[bidding_team]
            
            # If the bidding team has already met their target.
            if current_bidding_wins >= self.bid_value:
                print("Bidding team has reached their bid target early. Ending game.")
                break
            # Or if it is impossible for the bidding team to reach their target.
            elif current_bidding_wins + remaining_rounds < self.bid_value:
                print("Bidding team can no longer reach their bid target. Ending game early.")
                break

        print("\n--- Game Over ---")
        print("Team scores:", self.team_wins)
        if self.team_wins[bidding_team] >= self.bid_value:
            print(f"Team {bidding_team} (the bidding team) wins the game!")
        else:
            print(f"Team {other_team} wins the game!")



