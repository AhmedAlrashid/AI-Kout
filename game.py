import random
from player import Player

# Define the ranks and suits
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7']
suits = ['♥', '♣', '♦', '♠']

# Build the deck: create cards for each suit, remove the 7♦, and add a Joker.
cards = {suit: [f"{rank}{suit}" for rank in ranks] for suit in suits}
cards['♦'].remove('7♦')
cards['J'] = ['Joker']  # Using 'J' as key for the Joker group
deck = [card for suit_cards in cards.values() for card in suit_cards]


class Game:
    def __init__(self, num_players=4, cards_per_player=8):
        self.num_players = num_players
        self.cards_per_player = cards_per_player
        self.deck = deck.copy()  # Work with a copy of the deck
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.defining_suit=None
        self.rounds_to_win=0
        self.player_to_beat=None

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

    def determine_current_suit(self,card):
        #whatever the card ends with is determined as the suit for that round
        return card[-1]
    
    #determine suit of the whole game 

    #to do: recurse the function over all players
    def determine_bigger_suit(self,player=None,rounds=5):
        for i in range (4):
            Player.potential_suit(f'Player {i+1}')

        player,rounds=Player.potential_suit

        suit=input("What suit would you like?")
        print(suit)
        return suit
