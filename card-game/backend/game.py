import random
from typing import List
from enum import Enum


class Suit(str, Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"


class Card:
    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value

    def to_dict(self):
        return {
            "suit": self.suit.value,
            "value": self.value,
            "display": self.get_display_value()
        }

    def get_display_value(self) -> str:
        if self.value == 1:
            return "A"
        elif self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        else:
            return str(self.value)


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        self.cards = []
        for suit in Suit:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            self.reset()
        return self.cards.pop()


class HighLowGame:
    def __init__(self):
        self.deck = Deck()
        self.current_card: Card = None
        self.score = 0
        self.streak = 0
        self.new_game()

    def new_game(self):
        self.deck.reset()
        self.current_card = self.deck.draw()
        self.score = 0
        self.streak = 0
        return self.get_state()

    def guess(self, is_higher: bool) -> dict:
        next_card = self.deck.draw()

        # 予想が正しいかチェック
        if is_higher:
            correct = next_card.value > self.current_card.value
        else:
            correct = next_card.value < self.current_card.value

        # 同じ値の場合は不正解
        if next_card.value == self.current_card.value:
            correct = False

        if correct:
            self.score += 10
            self.streak += 1
        else:
            self.streak = 0

        result = {
            "correct": correct,
            "previous_card": self.current_card.to_dict(),
            "next_card": next_card.to_dict(),
            "score": self.score,
            "streak": self.streak
        }

        self.current_card = next_card

        return result

    def get_state(self) -> dict:
        return {
            "current_card": self.current_card.to_dict() if self.current_card else None,
            "score": self.score,
            "streak": self.streak
        }
