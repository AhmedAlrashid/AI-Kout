# player.py

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.current_number_of_rounds = 5  # Initial bid is set at 5.
        self.current_suiter = None

    def add_card(self, card):
        """Add a card to the player's hand."""
        self.hand.append(card)

    def possible_cards(self, lead_suit):
        """
        Return the list of cards the player can legally play given the trick’s lead suit.
        - The Joker is always allowed.
        - Otherwise, if the player has any cards matching the lead suit, those are allowed.
        (Now, even if the player has matching cards, the Joker is added if it exists.)
        """
        # If no lead suit is defined, any card is allowed.
        if lead_suit is None:
            return self.hand.copy()

        # All cards that follow the lead suit.
        allowed = [card for card in self.hand if card.endswith(lead_suit)]
        # Always add Joker if the player has it.
        if "Joker" in self.hand and "Joker" not in allowed:
            allowed.append("Joker")
        # If no cards match the lead suit, return the whole hand.
        if not allowed:
            return self.hand.copy()
        return allowed


    def potential_suit(self, current_suiter=None, current_number_of_rounds=0):
        """
        Ask the player how many rounds they are willing to take on.
        The bid must be strictly higher than the current maximum bid.
        The minimum allowed bid is max(5, current_number_of_rounds+1).
        Entering 0 will count as passing.
        If the bid is invalid (not 0 and less than the minimum), an exception is thrown and the player is prompted again.
        """
        # Calculate the minimum bid required.
        min_bid = max(5, current_number_of_rounds)
        
        while True:
            try:
                bid = int(input(f"{self.name}, how many rounds are you willing to take on? (Minimum is {min_bid}, enter 0 to pass): "))
                if bid == 0:
                    # Player passes.
                    return current_suiter, current_number_of_rounds
                if bid < min_bid:
                    raise ValueError(f"Bid must be at least {min_bid} or 0 to pass.")
                # Valid bid; update the current bid and suiter.
                current_number_of_rounds = bid
                current_suiter = self.name
                return current_suiter, current_number_of_rounds
            except ValueError as e:
                print(e)
                print("Please try again.")

    def __str__(self):
        return f"{self.name}: {self.hand}"
