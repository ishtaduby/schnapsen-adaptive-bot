from __future__ import annotations
from typing import Optional

from schnapsen.game import Bot, PlayerPerspective, Move


# Schnapsen card points
RANK_POINTS = {
    "ACE": 11,
    "TEN": 10,
    "KING": 4,
    "QUEEN": 3,
    "JACK": 2,
}


def points_of_move(move: Move) -> int:
    """Points of a move's card (0 for non-card moves)."""
    card = getattr(move, "card", None)
    if card is None:
        return 0
    return RANK_POINTS.get(card.rank.name, 0)


def is_trump(move: Move, trump_suit) -> bool:
    card = getattr(move, "card", None)
    return card is not None and card.suit == trump_suit


class AdaptiveThresholdBot(Bot):
    """
    Threshold-switching bot:
    - Below threshold: passive (avoid trumps, shed low-point cards)
    - At/above threshold: aggressive (prefer trumps, play high-point cards)
    """

    def __init__(self, threshold: int, name: Optional[str] = "Adaptive") -> None:
        super().__init__(name)
        self.threshold = threshold

    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        current_score = perspective.get_my_score().direct_points
        moves = list(perspective.valid_moves())
        trump_suit = perspective.get_trump_suit()

        trump_moves = [m for m in moves if is_trump(m, trump_suit)]
        non_trump_moves = [m for m in moves if getattr(m, "card", None) is not None and not is_trump(m, trump_suit)]
        other_moves = [m for m in moves if getattr(m, "card", None) is None]  # marriages/exchange etc.

        # Optional: prioritize non-card "special" moves if they exist (often beneficial)
        # If you want to keep it simplest, you can delete this block.
        if other_moves:
            return other_moves[0]

        # PASSIVE: avoid trumps, play lowest-point card
        if current_score < self.threshold:
            if non_trump_moves:
                return min(non_trump_moves, key=points_of_move)
            # if only trumps are available
            return min(moves, key=points_of_move)

        # AGGRESSIVE: prefer trumps, play highest-point card
        else:
            if trump_moves:
                return max(trump_moves, key=points_of_move)
            return max(moves, key=points_of_move)
