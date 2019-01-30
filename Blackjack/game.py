import random
from pip._vendor.distlib.compat import raw_input


def face_card(card):
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    return card

#def ready_deck(deck):

def deal_hand(deck):
    hand = []
    for i in range(2):
        card = deck.pop()
        card = face_card(card)
        hand.append(card)
    return hand

def twist(hand, deck):
    card = deck.pop()
    card = face_card(card)
    hand.append(card)
    return hand

def card_total(hand):
    total = 0
    if "A" in hand:
        old_index = hand.index("A")
        hand.insert(len(hand), hand.pop(old_index))
    for card in range(len(hand)):
        if hand[card] == "J": total = total + 10
        elif hand[card] == "Q": total = total + 10
        elif hand[card] == "K": total = total + 10
        elif hand[card] == "A":
            if total > 10:
                total = total + 1
            else:
                total = total + 11
        else:
            total = total + hand[card]
    return total


def play_game(hand, deck):
    choice = False
    while choice == False:
        print("Your hand contains " + str(hand))
        hand_total = card_total(hand)
        print("Your hand total is " + str(hand_total))
        if hand_total > 21:
            print("BUST, end of game")
            choice = True  # stops an infinite loop
        else:
            another_card = raw_input('(s)tick or (t)wist: ')
            if another_card == "s":
                choice = True
                print ("stick, your hand total: " + str(hand_total))
            elif another_card == "t":
                choice = False
                print("twist")
                hand = twist(hand, deck)
            else:
                print("\nPoor Input.\n")
    return hand


def dealers_game(hand, deck):
    total = card_total(hand)
    print("Dealers starting hand is " + str(hand))
    print("Dealers starting total is " + str(total))
    while int(total) < 17:
        print("Dealer twists")
        hand = twist(hand, deck)
        total = card_total(hand)
        print("Dealer twists and has new of total: " + str(total))
    else:
        print("Dealer has finishing hand of " + str(hand))
        print("Dealer sticks with total of " + str(total))
    return hand


def score(dealer_hand, player_hand):
    player_total = card_total(player_hand)
    dealer_total = card_total(dealer_hand)

    if player_total == 21:
        print("Congratulations! You got a Blackjack!\n")
    elif dealer_total == 21:
        print("Sorry, you lose. The dealer got a blackjack.\n")
    elif player_total > dealer_total and player_total < 22:
        print("Player wins")
    elif player_total < dealer_total and dealer_total < 22:
        print("Dealer wins")
    elif player_total > 21:
        print("Player bust, dealer wins")
    elif dealer_total > 21:
        print("dealer bust, player wins")


deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
random.shuffle(deck)
player_hand = deal_hand(deck)
dealer_hand = deal_hand(deck)
player_hand = play_game(player_hand, deck)
dealer_hand = dealers_game(dealer_hand, deck)
score(dealer_hand, player_hand)








# print "Intial total of cards " + str(card_total(hand))
# print "The cards remaining in the deck are " + str(deck)
# print "Remaining deck size " + str(len(deck))
#
# #twist and add new total
# hand = twist(hand, deck)
# print "New total of cards " + str(card_total(hand))
# print "The cards remaining in the deck are " + str(deck)
# print "Remaining deck size " + str(len(deck))
# #print "Total of cards " + str(card_total(hand))