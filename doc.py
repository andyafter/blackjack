from shuffler import Shuffler

SHOE_SIZE = 6
BOARD_CARD_NUMBER = 20

# create a shuffler with 6 decks(SHOE_SIZE)
sh = Shuffler(SHOE_SIZE)

def deal_board(sh, board_size):
    # deal a board with card number of board_size
    sh.shuffle_back()
    for i in range(board_size):
        #print(sh.deal())
        sh.deal()
    return sh.cards_dealt

# if after running this there's no "incomplete deck" error, things are good!
# deal_board(sh, BOARD_CARD_NUMBER)


