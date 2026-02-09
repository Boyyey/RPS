import random

# Beat a move
def beat(move):
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    elif move == "S":
        return "R"
    else:
        return random.choice(["R", "P", "S"])

# Advanced predictor: stores sequences of moves and what came next
class SequencePredictor:
    def __init__(self):
        self.history = []
        self.sequences = {}

    # Add last move to history
    def update(self, move):
        if move:
            self.history.append(move)
            # Build sequences of length 2 and 3
            for length in [2, 3]:
                if len(self.history) > length:
                    key = tuple(self.history[-length-1:-1])
                    next_move = self.history[-1]
                    if key not in self.sequences:
                        self.sequences[key] = {}
                    if next_move not in self.sequences[key]:
                        self.sequences[key][next_move] = 0
                    self.sequences[key][next_move] += 1

    # Predict next move based on sequence
    def predict(self):
        for length in [3, 2]:
            if len(self.history) >= length:
                key = tuple(self.history[-length:])
                if key in self.sequences:
                    # Choose most frequent next move
                    next_moves = self.sequences[key]
                    predicted = max(next_moves, key=next_moves.get)
                    return predicted
        return None  # No pattern found

# Global predictor instance (maintains state across calls)
predictor = SequencePredictor()

def player(prev_play, opponent_history=[]):
    # Update global predictor
    predictor.update(prev_play)

    # Also maintain opponent history if needed
    if prev_play != "":
        opponent_history.append(prev_play)

    # First move: random
    if not opponent_history:
        return random.choice(["R", "P", "S"])

    # Try pattern prediction first
    predicted_move = predictor.predict()
    if predicted_move:
        return beat(predicted_move)

    # Fallback: frequency-based strategy
    counts = {"R": 0, "P": 0, "S": 0}
    for move in opponent_history:
        counts[move] += 1
    most_frequent = max(counts, key=counts.get)
    return beat(most_frequent)

# Optional: testing block
if __name__ == "__main__":
    from RPS_game import play, quincy, random_bot, reflective, cycle

    bots = [quincy, random_bot, reflective, cycle]
    for bot in bots:
        print(f"\nPlaying against {bot.__name__}:")
        play(player, bot, 1000, verbose=True)
