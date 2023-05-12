from shuffler import Shuffler
import csv

sh = Shuffler(6)
BOARD_CARD_NUMBER = 20

def deal_board_then_shuffle_back(board_card_number):
    dealt_cards = []
    for i in range(board_card_number):
        dealt_cards.append(sh.get_card())
    sh.shuffle_back(dealt_cards)
    return dealt_cards

temp = {}
temp_count = 0
repeated_cards = []
for r in range(10000):
    dealt_cards = deal_board_then_shuffle_back(BOARD_CARD_NUMBER)
    print("======== new hand ==========")
    rc = []
    for card in dealt_cards:
        if card in temp:
            rc.append(card)
            print("card from last table appeared again, the card is: ", card)
    if len(rc) > 0:
        repeated_cards.append(rc)
    temp = {}
    for card in dealt_cards:
        temp[card] = 1

one_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 1])
two_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 2])
three_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 3])
four_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 4])
five_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 5])
six_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 6])
seven_cards_used_count = len([sublist for sublist in repeated_cards if len(sublist) == 7])
print(len(repeated_cards), one_cards_used_count, two_cards_used_count, three_cards_used_count, four_cards_used_count, five_cards_used_count, six_cards_used_count, seven_cards_used_count)