import random
from art import logo

NUM_DECKS = 1           # number of 52-card decks in the shoe
DEALER_HITS_SOFT_17 = False  # True = dealer hits soft 17; False = dealer stands

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["♠", "♥", "♦", "♣"]

def build_deck(num_decks=1):
    """Return a new list representing a shuffled shoe of num_decks decks.
       Each card is a (rank, suit) tuple, e.g. ('A','♠') or ('10','♦')."""
    deck = []
    for _ in range(num_decks):
        for r in RANKS:
            for s in SUITS:
                deck.append((r, s))
    random.shuffle(deck)
    return deck


def deal(deck, n=1):
    """Deal n cards from the top (start) of the list. Mutates the deck."""
    if n > len(deck):
        raise RuntimeError("Shoe is out of cards")
    dealt = deck[:n]
    del deck[:n]
    return dealt


def card_str(card):
    """Nicely format a single card tuple like ('A','♠') -> 'A♠'."""
    r, s = card
    return f"{r}{s}"


def hand_str(hand):
    """Render a list of card tuples as 'A♠ 9♦'."""
    return " ".join(card_str(c) for c in hand)


def card_value(rank):
    """Base value for a card rank. Ace defaults to 11; we adjust later."""
    if rank == "A":
        return 11
    if rank in {"10", "J", "Q", "K"}:
        return 10
    return int(rank)


def score_hand(hand):
    """
    Compute blackjack-style scoring with multiple Aces handled.
    Returns a dict:
      {
        'total': int,
        'is_blackjack': bool,   # natural 21 on first two cards
        'is_bust': bool,
        'is_soft': bool         # at least one Ace still counted as 11
      }
    """
    ranks = [r for (r, _) in hand]
    total = sum(card_value(r) for r in ranks)
    ace_count = ranks.count("A")
    demoted = 0

    # Demote Aces (11 -> 1) until total <= 21 or no more Aces to demote
    while total > 21 and demoted < ace_count:
        total -= 10
        demoted += 1

    is_bust = total > 21
    is_blackjack = (len(hand) == 2 and total == 21)
    # Soft = there exists at least one Ace still counted as 11
    is_soft = (ace_count - demoted) > 0 and not is_bust

    return {
        "total": total,
        "is_blackjack": is_blackjack,
        "is_bust": is_bust,
        "is_soft": is_soft,
    }


def dealer_should_hit(score, hits_soft_17=False):
    """
    Decide if dealer should hit given a score dict from score_hand().
    hits_soft_17: if True, dealer hits on soft 17; otherwise stands.
    """
    if score["is_bust"] or score["is_blackjack"]:
        return False
    if score["total"] < 17:
        return True
    if score["total"] == 17 and score["is_soft"] and hits_soft_17:
        return True
    return False


def compare_scores(player_score, dealer_score):
    """
    Return 'player', 'dealer', or 'push' based on standard rules.
    Natural blackjack wins over a non-blackjack 21.
    """
    if player_score["is_bust"]:
        return "dealer"
    if dealer_score["is_bust"]:
        return "player"

    if player_score["is_blackjack"] and not dealer_score["is_blackjack"]:
        return "player"
    if dealer_score["is_blackjack"] and not player_score["is_blackjack"]:
        return "dealer"

    if player_score["total"] > dealer_score["total"]:
        return "player"
    if player_score["total"] < dealer_score["total"]:
        return "dealer"
    return "push"


def render_line(label, hand, reveal_all=True):
    """
    Build one line of display for a hand.
    Example:
      Your cards: [A♠ 9♦] → 20 (hard)
      Dealer's cards: [K♥ ?]  (hidden)
    """
    if not reveal_all:
        if hand:
            visible = f"{card_str(hand[0])} ?"
        else:
            visible = "?"
        return f"{label}: [{visible}]  (hidden)"

    s = score_hand(hand)
    soft_hard = "soft" if s["is_soft"] else "hard"
    postfix = " BLACKJACK!" if s["is_blackjack"] else ""
    return f"{label}: [{hand_str(hand)}] → {s['total']} ({soft_hard}){postfix}"


def prompt_yes_no(msg):
    while True:
        ans = input(msg).strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please type 'y' or 'n'.")


def prompt_hit_stand():
    while True:
        ans = input("Type 'h' to hit, 's' to stand: ").strip().lower()
        if ans in {"h", "hit"}:
            return "hit"
        if ans in {"s", "stand"}:
            return "stand"
        print("Please type 'h' or 's'.")


def play_round():
    deck = build_deck(NUM_DECKS)

    # Initial deal
    player = deal(deck, 2)
    dealer = deal(deck, 2)

    print(logo)
    print(render_line("Dealer's cards", dealer, reveal_all=False))
    print(render_line("Your cards", player, reveal_all=True))

    ps = score_hand(player)
    ds = score_hand(dealer)

    # Natural blackjack short-circuit
    if ps["is_blackjack"] or ds["is_blackjack"]:
        print(render_line("Dealer's cards", dealer, reveal_all=True))
        outcome = compare_scores(ps, ds)
        print_outcome(outcome, ps, ds)
        return

    # Player turn
    while True:
        ps = score_hand(player)
        if ps["is_bust"] or ps["is_blackjack"]:
            break
        action = prompt_hit_stand()
        if action == "hit":
            player.extend(deal(deck, 1))
            print(render_line("Your cards", player, reveal_all=True))
        else:
            break

    ps = score_hand(player)
    if ps["is_bust"]:
        print(render_line("Your cards", player, reveal_all=True))
        print(render_line("Dealer's cards", dealer, reveal_all=True))
        print_outcome("dealer", ps, ds)
        return

    # Dealer plays out
    while True:
        ds = score_hand(dealer)
        if not dealer_should_hit(ds, hits_soft_17=DEALER_HITS_SOFT_17):
            break
        dealer.extend(deal(deck, 1))

    # Final reveal + result
    ps = score_hand(player)
    ds = score_hand(dealer)
    print(render_line("Your cards", player, reveal_all=True))
    print(render_line("Dealer's cards", dealer, reveal_all=True))
    outcome = compare_scores(ps, ds)
    print_outcome(outcome, ps, ds)


def print_outcome(outcome, ps, ds):
    if outcome == "player":
        reason = (
            "blackjack!"
            if ps["is_blackjack"] and not ds["is_blackjack"]
            else "dealer busts!"
            if ds["is_bust"]
            else "higher total!"
        )
        print(f"You win — {reason}")
    elif outcome == "dealer":
        reason = (
            "dealer blackjack."
            if ds["is_blackjack"] and not ps["is_blackjack"]
            else "you busted."
            if ps["is_bust"]
            else "lower total."
        )
        print(f"Dealer wins — {reason}")
    else:
        print("Push — same total.")


if __name__ == "__main__":
    while prompt_yes_no("Do you want to play a game of Blackjack? Type 'y' or 'n': "):
        play_round()
    print("Goodbye!")
