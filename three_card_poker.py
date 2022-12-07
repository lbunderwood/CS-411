# three_card_poker.py
# Created by Luke Underwood 2022-12-05
# Assignment 6 for CS 411 Analysis of Algorithms
# computes a return table for three card draw poker

import sys
from enum import Enum


Suit = Enum('Suit', ['HEART', 'SPADE', 'DIAMOND', 'CLUB'])


# Ordered high to low value, abbreviations correspond to:
# Royal Flush, Straight Flush, Three Aces, Three of a Kind, STraight, FLush, PaiR, and High Card
Hand = Enum('Hand', ['RF', 'SF', 'TA', 'TK', 'ST', 'FL', 'PR', 'HC'])


# Card class, groups value with suit 
# (1 = Ace, 11=J, 12=Q, 13=K, suit uses Suit enum)
class Card:
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
    def __str__(self):
        return str(self.val) + ", " + str(self.suit)
    def __repr__(self):
        return self.__str__()


# returns the monetary value of a hand, using Hand enum as input
def get_value(hand):
    vals = {Hand.RF : 250,
            Hand.SF : 50,
            Hand.TA : 100,
            Hand.TK : 40,
            Hand.ST : 10,
            Hand.FL : 5,
            Hand.PR : 1,
            Hand.HC : 0}
    return vals[hand]


# takes an array of three Cards, returns a member of Hand enum
def classify_hand(cards):
    cards = sorted(cards, key=lambda card: card.val)

    straight = False
    flush = False

    # identify flush
    if cards[0].suit == cards[1].suit and cards[1].suit == cards[2].suit:
        flush = True

    # royal flush/identify special case of Q K A straight
    if cards[0].val == 1 and cards[1].val == 12 and cards[2].val == 13:
        if flush:
            return Hand.RF
        else:
            straight = True

    # straight flush/identify straight
    if straight or (cards[0].val + 1 == cards[1].val and cards[1].val + 1 == cards[2].val):
        if flush:
            return Hand.SF
        else:
            straight = True

    # Three Aces
    if cards[0].val == 1 and cards[1].val == 1 and cards[2].val == 1:
        return Hand.TA

    # Three of a kind
    if cards[0].val == cards[1].val and cards[1].val == cards[2].val:
        return Hand.TK

    # Straight
    if straight:
        return Hand.ST

    # Flush
    if flush:
        return Hand.FL

    # Pair (due to sort no need to check 0 against 2)
    if cards[0].val == cards[1].val or cards[1].val == cards[2].val:
        return Hand.PR

    # High Card
    return Hand.HC


# calculates the frequencies for a given hold using combinations
def hold_freq_comb(cards, hold, deck):
    freq = {}
    for hand in Hand:
        freq[hand] = 0
    combs = 0

    # remove cards not being held from hand
    cards_temp = []
    for ind in hold:
        cards_temp.append(cards[ind])
    cards = cards_temp

    # no cards are held
    if len(hold) == 0:
        freq, combs = combination_frequencies(draw=False)

    # one card is held
    if len(hold) == 1:
        for i in range(len(deck) - 1):
            for j in range(i + 1, len(deck)):
                cards.extend([deck[i], deck[j]])
                freq[classify_hand(cards)] += 1
                combs += 1
                cards.remove(deck[i])
                cards.remove(deck[j])

    # two cards are held
    if len(hold) == 2:
        for card in deck:
            cards.append(card)
            freq[classify_hand(cards)] += 1
            combs += 1
            cards.remove(card)

    # three cards are held
    if len(hold) == 3:
        freq[classify_hand(cards)] += 1
        combs = 1

    return freq, combs


# calculates the stats for a given hold (hold contains indices of cards to hold)
def hold_return(cards, hold, deck):
    tot_ret = 0

    freq, total = hold_freq_comb(cards, hold, deck)
    for k, v in freq.items():
        prob = v / total
        ret = prob * get_value(k)
        tot_ret += ret

    return freq, tot_ret


# calculates the stats for the optimal hold for a given hand (called from combination_frequencies)
def best_hold(cards, deck):
    hold = []
    max_ret = -1
    temp_deck = deck.copy()

    # remove cards from deck, as they cannot be drawn again
    for card in cards:
        for d_card in temp_deck:
            if d_card.val == card.val and d_card.suit == card.suit:
                temp_deck.remove(d_card)

    for i in range(8):
        if i & 1:
            hold.append(0)
        if i & 2:
            hold.append(1)
        if i & 4:
            hold.append(2)
        freq, ret = hold_return(cards, hold, temp_deck)
        if ret > max_ret:
            best_hold = hold.copy()
            best_freq = freq.copy()
            max_ret = ret
        hold.clear()

    return best_hold, best_freq


# uses combination method to get frequencies and total combinations
def combination_frequencies(draw=True):
    freq = {}
    for hand in Hand:
        freq[hand] = 0

    deck = []
    for i in range(1, 14):
        for suit in Suit:
            deck.append(Card(i, suit))

    # iterate over first 50 cards
    combs = 0
    for i in range(len(deck) - 2):
        # iterate over cards between i and 51
        for j in range(i + 1, len(deck) - 1):
            # iterate over cards between j and 52
            for k in range(j + 1, len(deck)):
                if draw:
                    hold, hold_freq = best_hold([deck[i], deck[j], deck[k]], deck)
                    for k, v in hold_freq.items():
                        freq[k] += v
                        combs += v
                else:
                    freq[classify_hand([deck[i], deck[j], deck[k]])] += 1
                    combs += 1

    return freq, combs


# returns total return
def total_return():
    comb_freq, combs = combination_frequencies()

    prob = {}
    ret = {}
    tot_ret = 0

    for k, v in comb_freq.items():
        prob[k] = v / combs
        ret[k] = prob[k] * get_value(k)
        tot_ret += ret[k]

    return comb_freq, prob, ret, tot_ret


# finds all of the holds for a given hand and their stats (called from main only)
def holds(cards):
    hold = []
    all_holds = []
    returns = []
    deck = []
    for i in range(1, 14):
        for suit in Suit:
            deck.append(Card(i, suit))

    # remove cards from deck, as they cannot be drawn again
    for card in cards:
        for d_card in deck:
            if d_card.val == card.val and d_card.suit == card.suit:
                deck.remove(d_card)

    for i in range(8):
        if i & 1:
            hold.append(0)
        if i & 2:
            hold.append(1)
        if i & 4:
            hold.append(2)
        freq, ret = hold_return(cards, hold, deck)
        all_holds.append(hold.copy())
        returns.append(ret)
        hold.clear()

    return all_holds, returns


# Print a dict in a nice way
def printdict(dict):
    print("--------------------------------")
    for k, v in dict.items():
        print(k, " : ", v)
    print("--------------------------------\n")


def main():

    comb_freq, prob, ret, tot_ret = total_return()
    print("Combination Frequencies:")
    printdict(comb_freq)
    print("Probabilities:")
    printdict(prob)
    print("Return values:")
    printdict(ret)
    print("Total Return: ", tot_ret, "\n")

    # list of 10 interesting hands to test hold algorithms
    hands = [[Card(12, Suit.HEART), Card(13, Suit.HEART), Card(1, Suit.HEART)], # RF
            [Card(3, Suit.CLUB), Card(4, Suit.CLUB), Card(5, Suit.CLUB)],       # SF
            [Card(1, Suit.SPADE), Card(1, Suit.HEART), Card(1, Suit.DIAMOND)],  # TA
            [Card(6, Suit.SPADE), Card(6, Suit.HEART), Card(6, Suit.CLUB)],     # TK
            [Card(9, Suit.HEART), Card(10, Suit.CLUB), Card(11, Suit.SPADE)],   # ST
            [Card(5, Suit.HEART), Card(8, Suit.HEART), Card(1, Suit.HEART)],    # FL
            [Card(13, Suit.HEART), Card(13, Suit.CLUB), Card(2, Suit.HEART)],   # PR
            [Card(3, Suit.HEART), Card(7, Suit.DIAMOND), Card(12, Suit.CLUB)],  # HC
            [Card(2, Suit.HEART), Card(3, Suit.HEART), Card(7, Suit.SPADE)],    # HC - close to SF/FL/ST
            [Card(1, Suit.SPADE), Card(1, Suit.HEART), Card(13, Suit.HEART)],   # PR - example from class
            [Card(5, Suit.HEART), Card(6, Suit.HEART), Card(1, Suit.HEART)],    # FL - close to SF/ST
            ]
    deck = []
    for i in range(1, 14):
        for suit in Suit:
            deck.append(Card(i, suit))

    for hand in hands:
        print("\nHand: ", hand)
        print("--------------------------------")

        # print all holds and their returns
        hold_arr, returns = holds(hand)
        for i in range(len(hold_arr)):
            print(hold_arr[i], " : expected return = ", returns[i])

        # find optimal play and compare against algorithm, then print it
        max_ind = returns.index(max(returns))
        if hold_arr[max_ind] != best_hold(hand, deck)[0]:
            print(hold_arr[max_ind], best_hold(hand, deck)[0])
            raise
        print("Best hold: ", hold_arr[max_ind], ", E[x] = ", returns[max_ind])
        print("--------------------------------\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())