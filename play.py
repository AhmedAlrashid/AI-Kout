import random

# Define the ranks and suits
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7']
suits = ['♥', '♣', '♦', '♠']

# Build the deck: create cards for each suit, remove the 7♦, and add a Joker.
cards = {suit: [f"{rank}{suit}" for rank in ranks] for suit in suits}
cards['♦'].remove('7♦')
cards['J'] = ['Joker']  # Using 'J' as key for Joker group
deck = [card for suit_cards in cards.values() for card in suit_cards]


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        """Add a card to the player's hand."""
        self.hand.append(card)

    def possible_cards(self, first_suit_played):
        """
        Return the list of cards the player can legally play given the first suit played.
        Rules:
          - If a card matches the first suit (and isn't the Joker), it's allowed.
          - The Joker is always allowed.
          - If no cards match the suit (or the Joker), the full hand is allowed.
        """
        allowed = []
        for card in self.hand:
            if card != "Joker" and card.endswith(first_suit_played):
                allowed.append(card)
        if "Joker" in self.hand:
            allowed.append("Joker")
        if not allowed:
            allowed = self.hand.copy()
        return allowed

    def __str__(self):
        return f"{self.name}: {self.hand}"


class Game:
    def __init__(self, num_players=4, cards_per_player=8):
        self.num_players = num_players
        self.cards_per_player = cards_per_player
        self.deck = deck.copy()  # Copy the global deck to avoid modifying it
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]

    def shuffle_and_deal(self):
        """Shuffle the deck and deal cards to each player."""
        random.shuffle(self.deck)
        for i in range(self.cards_per_player * self.num_players):
            player = self.players[i % self.num_players]
            player.add_card(self.deck[i])

    def show_hands(self):
        """Print each player's hand."""
        for player in self.players:
            print(player)


# Example usage (not auto-playing the game):
if __name__ == "__main__":
    game = Game()
    game.shuffle_and_deal()
    game.show_hands()

    # For demonstration: Assume the first card played in a trick is of suit '♥'
    first_suit = '♥'
    print(f"\nPossible cards for {game.players[0].name} when first suit is '{first_suit}':")
    print(game.players[0].possible_cards(first_suit))
    print(f"\nPossible cards for {game.players[1].name} when first suit is '{first_suit}':")
    print(game.players[1].possible_cards(first_suit))
    print(f"\nPossible cards for {game.players[2].name} when first suit is '{first_suit}':")
    print(game.players[2].possible_cards(first_suit))
    print(f"\nPossible cards for {game.players[3].name} when first suit is '{first_suit}':")
    print(game.players[3].possible_cards(first_suit))
    
    