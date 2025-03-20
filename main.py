from game import Game

if __name__ == "__main__":
#     # Create a game instance
#     game = Game()
#     game.shuffle_and_deal()
#     game.show_hands()

#     # For demonstration: assume the first card played in a trick has suit '♥'
#     first_suit = '♥'
#     for player in game.players:
#         print(f"\nPossible cards for {player.name} when first suit is '{first_suit}':")
#         print(player.possible_cards(first_suit))

#     print(game.determine_current_suit('8♥'))

#     player.potential_suit()

#     game.determine_bigger_suit()

    game = Game()
    game.shuffle_and_deal()
    game.show_hands()
    trump = game.determine_bigger_suit()
    print("Trump suit is:", trump)
    # Play one trick.
    game.play_trick()
