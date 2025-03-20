# test_game.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import patch
from game import beats, Game
from player import Player

class TestBeatsFunction(unittest.TestCase):
    def test_joker_always_wins(self):
        # Joker always beats any other card.
        self.assertTrue(beats("Joker", "A♣", "♣", "♦"))
        self.assertTrue(beats("Joker", "10♦", "♦", "♦"))
        # Nothing beats the Joker.
        self.assertFalse(beats("A♣", "Joker", "♣", "♦"))

    def test_trump_wins(self):
        # Given trump suit ♦, A♦ should beat K♣.
        self.assertTrue(beats("A♦", "K♣", "♣", "♦"))
        self.assertFalse(beats("K♣", "A♦", "♣", "♦"))

    def test_lead_suit_comparison(self):
        # With no trump interference, within the lead suit ♣, A♣ beats K♣.
        self.assertTrue(beats("A♣", "K♣", "♣", "♦"))
        self.assertFalse(beats("10♣", "J♣", "♣", "♦"))

class TestPossibleCardsMethod(unittest.TestCase):
    def test_possible_cards_includes_joker(self):
        player = Player("TestPlayer")
        player.hand = ["A♣", "Joker", "10♣"]
        allowed = player.possible_cards("♣")
        # Since lead suit is ♣, allowed cards should include cards that end with ♣
        # AND always include the Joker.
        self.assertIn("Joker", allowed)
        self.assertIn("A♣", allowed)
        self.assertIn("10♣", allowed)

    def test_possible_cards_when_no_lead(self):
        player = Player("TestPlayer")
        player.hand = ["A♦", "Joker", "K♠"]
        allowed = player.possible_cards(None)
        self.assertEqual(set(allowed), set(["A♦", "Joker", "K♠"]))

class TestPotentialSuitMethod(unittest.TestCase):
    def test_valid_bid(self):
        player = Player("TestPlayer")
        # Starting current_number_of_rounds is 5; thus, minimum bid is max(5, 5+1)=6.
        # We simulate an input of "7" which is valid.
        with patch("builtins.input", side_effect=["7"]):
            suiter, bid = player.potential_suit(current_suiter=None, current_number_of_rounds=5)
            self.assertEqual(bid, 7)
            self.assertEqual(suiter, "TestPlayer")

    def test_invalid_then_valid_bid(self):
        player = Player("TestPlayer")
        # First input is invalid (e.g. "4", below min bid of 6), then a valid bid "8".
        with patch("builtins.input", side_effect=["4", "8"]):
            suiter, bid = player.potential_suit(current_suiter=None, current_number_of_rounds=5)
            self.assertEqual(bid, 8)
            self.assertEqual(suiter, "TestPlayer")

    def test_pass_bid(self):
        player = Player("TestPlayer")
        # Simulate passing with input "0". Since passing doesn't update the bid,
        # current_number_of_rounds remains unchanged and suiter remains as given.
        with patch("builtins.input", side_effect=["0"]):
            suiter, bid = player.potential_suit(current_suiter=None, current_number_of_rounds=5)
            self.assertEqual(bid, 5)
            self.assertIsNone(suiter)

    


if __name__ == "__main__":
    unittest.main()
