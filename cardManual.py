# multiplayer_card_game.py
import random
import sys

def create_deck():
    # Use list comprehension to create a standard 52-card deck
    ranks = ['A'] + [str(x) for x in range(2, 11)] + ['J', 'Q', 'K']
    suits = ['♠', '♥', '♦', '♣']  # visually nice, can be replaced by letters
    deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
    return deck

def get_num_players():
    while True:
        raw = input("Enter number of players (integer between 2 and 52): ").strip()
        if not raw:
            print("Error: input cannot be empty.")
            continue
        if not raw.isdigit():
            print("Error: please enter a positive integer.")
            continue
        n = int(raw)
        if n < 2 or n > 52:
            print("Error: number of players must be between 2 and 52.")
            continue
        return n

def distribute_deck(deck, num_players):
    cards_per_player = len(deck) // num_players
    if cards_per_player == 0:
        raise ValueError("Too many players for a 52-card deck.")
    # Deal contiguous blocks after shuffling so distribution is fair
    hands = [deck[i*cards_per_player:(i+1)*cards_per_player] for i in range(num_players)]
    leftover = deck[num_players*cards_per_player:]
    return hands, leftover

def choose_cards_for_round(hands):
    # Randomly choose one card from each player's hand (and remove it)
    played = []
    for idx, hand in enumerate(hands):
        if not hand:
            # Shouldn't happen if rounds are controlled, but handle gracefully
            played.append(None)
            continue
        card = random.choice(hand)
        hand.remove(card)
        played.append(card)
    return played

def get_round_winner(num_players, round_number, played_cards):
    print(f"\n--- Round {round_number} ---")
    for i, card in enumerate(played_cards, start=1):
        print(f"Player {i}: {card}")
    while True:
        raw = input(f"Enter round winner (player number 1-{num_players}): ").strip()
        if not raw:
            print("Error: input cannot be empty.")
            continue
        if not raw.isdigit():
            print("Error: please enter a numeric player number.")
            continue
        p = int(raw)
        if p < 1 or p > num_players:
            print(f"Error: player number must be between 1 and {num_players}.")
            continue
        return p - 1  # zero-based index for internal use

def announce_final_winner(scores):
    print("\n=== Final Scores ===")
    for i, s in enumerate(scores, start=1):
        print(f"Player {i}: {s} rounds won")
    max_score = max(scores)
    winners = [i+1 for i, s in enumerate(scores) if s == max_score]
    if len(winners) == 1:
        print(f"\n🎉 Player {winners[0]} wins the game with {max_score} rounds won! 🎉")
    else:
        print(f"\nIt's a tie between players: {', '.join(map(str, winners))} with {max_score} rounds each.")

def main():
    print("=== Multi-player Round-based Card Game ===")
    num_players = get_num_players()

    deck = create_deck()
    random.shuffle(deck)
    hands, leftover = distribute_deck(deck, num_players)

    cards_per_player = len(hands[0])
    if leftover:
        print(f"Note: {len(leftover)} leftover card(s) were removed to ensure equal distribution.")
        # Optional: show leftover cards
        print(f"Leftover card(s): {', '.join(leftover)}")

    print(f"\nEach player will receive {cards_per_player} cards.")
    # Uncomment the following lines if you want to display each player's starting hand:
    # for i, h in enumerate(hands, start=1):
    #     print(f"Player {i} starting hand ({len(h)} cards): {', '.join(h)}")

    scores = [0] * num_players
    total_rounds = cards_per_player

    for round_num in range(1, total_rounds + 1):
        played = choose_cards_for_round(hands)
        # show played cards & get winner (input validated inside function)
        try:
            winner_idx = get_round_winner(num_players, round_num, played)
        except KeyboardInterrupt:
            print("\nGame interrupted by user. Exiting.")
            sys.exit(0)
        scores[winner_idx] += 1
        print(f"Player {winner_idx+1} wins Round {round_num}!\nCurrent scores: " +
              ", ".join(f"P{i+1}:{s}" for i, s in enumerate(scores)))

    announce_final_winner(scores)
    print("\nGame complete. Thanks for playing!")

if __name__ == "__main__":
    main()