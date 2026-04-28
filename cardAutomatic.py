import random
import sys

# -------------------------------
# CREATE DECK (using list comprehension)
# -------------------------------
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10'] + ['J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']
    return [f"{rank}{suit}" for suit in suits for rank in ranks]


# -------------------------------
# GET NUMBER OF PLAYERS
# -------------------------------
def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2–52): "))
            if n < 2 or n > 52:
                print("Error: Enter between 2 and 52 players.")
            else:
                return n
        except ValueError:
            print("Error: Please enter a valid number.")


# -------------------------------
# DISTRIBUTE CARDS EQUALLY
# -------------------------------
def distribute_cards(deck, num_players):
    cards_per_player = len(deck) // num_players
    hands = [deck[i * cards_per_player:(i + 1) * cards_per_player] for i in range(num_players)]
    leftover = deck[num_players * cards_per_player:]
    return hands, leftover


# -------------------------------
# GET CARD VALUE
# -------------------------------
def get_card_value(card):
    rank = card[:-1]  # remove suit

    if rank == 'A':
        return 14
    elif rank == 'K':
        return 13
    elif rank == 'Q':
        return 12
    elif rank == 'J':
        return 11
    else:
        return int(rank)


# -------------------------------
# DECIDE ROUND WINNER
# -------------------------------
def decide_winner(cards):
    values = [get_card_value(card) for card in cards]
    max_value = max(values)

    winners = [i for i, v in enumerate(values) if v == max_value]
    return winners


# -------------------------------
# MAIN GAME
# -------------------------------
def main():
    print("=== Automatic Multi-Player Card Game ===")

    num_players = get_num_players()

    deck = create_deck()
    random.shuffle(deck)

    hands, leftover = distribute_cards(deck, num_players)

    if leftover:
        print(f"\nNote: {len(leftover)} leftover card(s) removed for equal distribution.")

    cards_per_player = len(hands[0])
    scores = [0] * num_players

    print(f"\nEach player gets {cards_per_player} cards.\n")

    # -------------------------------
    # PLAY ROUNDS
    # -------------------------------
    for round_num in range(1, cards_per_player + 1):
        print(f"\n--- Round {round_num} ---")

        played_cards = []

        # Each player plays a random card
        for i in range(num_players):
            card = random.choice(hands[i])
            hands[i].remove(card)
            played_cards.append(card)
            print(f"Player {i+1}: {card}")

        # Decide winner automatically
        winners = decide_winner(played_cards)

        if len(winners) == 1:
            winner = winners[0]
            print(f"🏆 Player {winner+1} wins this round!")
            scores[winner] += 1
        else:
            print("⚖️ Tie between players:", [w+1 for w in winners])

    # -------------------------------
    # FINAL RESULT
    # -------------------------------
    print("\n=== Final Scores ===")
    for i, score in enumerate(scores):
        print(f"Player {i+1}: {score}")

    max_score = max(scores)
    final_winners = [i+1 for i, s in enumerate(scores) if s == max_score]

    if len(final_winners) == 1:
        print(f"\n🎉 Player {final_winners[0]} is the OVERALL WINNER! 🎉")
    else:
        print(f"\n🤝 It's a tie between players: {final_winners}")

    print("\nGame Over!")


# -------------------------------
# RUN PROGRAM
# -------------------------------
if __name__ == "__main__":
    main()