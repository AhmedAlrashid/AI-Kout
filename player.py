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
    
    #to do: fix the 4th player error
    def potential_suit(self,current_suiter=None,current_number_of_rounds=5):
        rounds=int(input(f"How many rounds are you willing to take on? Minimum is {current_number_of_rounds} please enter 0 if you want to pass"))
        if rounds>current_number_of_rounds:
            current_number_of_rounds=rounds
            current_suiter=self.name
        #fix condition
        elif current_suiter is None and self.name=="Player 4":
            current_number_of_rounds=5
            current_suiter=self.name
        
        #updates globally the suiters and the current number_of_rounds
        self.current_number_of_rounds = current_number_of_rounds
        self.current_suiter = current_suiter
        return current_suiter,current_number_of_rounds

        
    def __str__(self):
        return f"{self.name}: {self.hand}"
