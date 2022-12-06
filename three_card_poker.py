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


# uses permutation method to get frequencies and total combinations
def permutation_return(deck):
    freq = {}
    for hand in Hand:
        freq[hand] = 0

    # calculate frequencies
    perms = 0
    for card1 in deck:
        for card2 in deck:
            if card1 == card2: continue
            for card3 in deck:
                if card1 == card3 or card2 == card3: continue
                freq[classify_hand([card1, card2, card3])] += 1
                perms += 1

    return freq, perms



# uses combination method to get frequencies and total combinations
def combination_return(deck):
    freq = {}
    for hand in Hand:
        freq[hand] = 0

    # iterate over first 50 cards
    combs = 0
    for i in range(len(deck) - 2):
        # iterate over cards between i and 51
        for j in range(i + 1, len(deck) - 1):
            # iterate over cards between j and 52
            for k in range(j + 1, len(deck)):
                freq[classify_hand([deck[i], deck[j], deck[k]])] += 1
                combs += 1

    return freq, combs


# returns total return
def total_return():
    deck = []
    for i in range(1, 14):
        for suit in Suit:
            deck.append(Card(i, suit))

    perm_freq, perms = permutation_return(deck)
    comb_freq, combs = combination_return(deck)

    prob = {}
    ret = {}
    tot_ret = 0

    # calculate probabilities
    for k, v in perm_freq.items():
        this_prob = v / perms

        # throw an error if permutation and combination methods got different answers
        if this_prob == comb_freq[k] / combs:
            prob[k] = this_prob
        else:
            raise

    vals = {Hand.RF : 250,
            Hand.SF : 50,
            Hand.TA : 100,
            Hand.TK : 40,
            Hand.ST : 10,
            Hand.FL : 5,
            Hand.PR : 1,
            Hand.HC : 0}

    # calculate returns
    for k, v in prob.items():
        ret[k] = vals[k] * v
        tot_ret += ret[k]

    return perm_freq, comb_freq, prob, ret, tot_ret


# Print a dict in a nice way
def printdict(dict):
    print("--------------------------------")
    for k, v in dict.items():
        print(k, " : ", v)
    print("--------------------------------\n")


def main():

    perm_freq, comb_freq, prob, ret, tot_ret = total_return()
    print("\nPermutation Frequencies:")
    printdict(perm_freq)
    print("Combination Frequencies:")
    printdict(comb_freq)
    print("Probabilities:")
    printdict(prob)
    print("Return values:")
    printdict(ret)
    print("Total Return: ", tot_ret, "\n")
    


if __name__ == "__main__":
    sys.exit(main())