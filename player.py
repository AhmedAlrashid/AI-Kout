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
