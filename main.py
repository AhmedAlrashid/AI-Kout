from game import Game

if __name__ == "__main__":
    # Create a game instance
    game = Game()
    game.shuffle_and_deal()
    game.show_hands()

    # For demonstration: assume the first card played in a trick has suit '♥'
    first_suit = '♥'
    for player in game.players:
        print(f"\nPossible cards for {player.name} when first suit is '{first_suit}':")
        print(player.possible_cards(first_suit))
