from shuffler import Shuffler
from strategy_importer import StrategyImporter
from blackjack import Hand, Round, Player


ROUNDS = 10000
HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = StrategyImporter('./strategies/BasicStrategy.csv').import_player_strategy()
sh=Shuffler(6,{"max":4,"weight":{1:1,2:1,3:1,4:1}})

def player_start_hand_translator(hand):
    result_hand = 0
    if hand[0] == hand[1]:
        if hand[0] in set({'T', 'J', 'Q', 'K'}):
            return "T,T"
        return str(hand[0]) + ',' + str(hand[1])
    if hand[0] == 'A' or hand[1] == 'A':
        return 'A' + str(hand[0]) if hand[1] == 'A' else str(hand[1])
    result_hand += 10 if hand[0] in set({'T','J','Q','K'}) else int(hand[0])
    result_hand += 10 if hand[1] in set({'T','J','Q','K'}) else int(hand[1])
    return str(result_hand)

basic_strategy = [HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY]
countings = []
nb_hands = 0
round_list = []
bet_list = []
pnl_list = []
total_bet = 0
total_pnl = 0
sh = Shuffler(6, {"max": 4, "weight": {1: 1, 2: 1, 3: 1, 4: 1}})

# Hashmap for ev to hand 
start_hand_map = {}
start_hands = [str(i) for i in range(5,22)] + ["A"+str(i) for i in range(2,10)] + [str(i) + "," + str(i) for i in range(2,11)] + ["A,A"]

for r in range(ROUNDS):
    round = Round(1, sh, basic_strategy)  # TODO: vary bet size according to True Count
    player_init_hands, dealer_init_hand = round.play_round()
    for i in range(round.player_number):
        player_win = 0
        for hand in round.players[i].hands:
            nb_hands += 1
            win, bet = round.get_hand_winnings(hand)
            round.total_bet += bet
            round.total_win += win
            player_win += win
            # add to heatmap
        hand_string = player_start_hand_translator(player_init_hands[i])
        if hand_string not in start_hand_map:
            start_hand_map[hand_string] = {}
        if dealer_init_hand[0] not in start_hand_map[hand_string]:
            start_hand_map[hand_string][dealer_init_hand[0]] = 0
        start_hand_map[hand_string][dealer_init_hand[0]] += player_win


    round_list.append(round)
    bet_list.append(round.total_bet)
    pnl_list.append(round.total_win)
    total_bet += round.total_bet
    total_pnl += round.total_win
    sh.shuffle_back()

print(start_hand_map)