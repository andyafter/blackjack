from blackjack import *
import math


if __name__ == "__main__":

    ROUNDS = 20000000
    HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = StrategyImporter('./strategies/BasicStrategy.csv').import_player_strategy()
    basic_strategy = [HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY]
    count_list = []
    TC_list=[]
    nb_hands = 0
    round_list = []
    original_bet_list=[]
    bet_list = []
    pnl_list = []
    pnl_per_original_bet_list=[]
    total_bet = 0
    total_pnl = 0
    total_original_bet = 0

    sh = Shuffler(6, {"max": 4, "weight": {1: 1, 2: 1, 3: 1, 4: 1},"remaining_decks":5})

    for r in range(ROUNDS):
        TC_list.append(sh._trueCount)
        roundbet=2**math.trunc(sh._trueCount)
        round = Round(roundbet, sh, basic_strategy,player_number=5)  
        round.play_round()
        for i in range(round.player_number):
            for hand in round.players[i].hands:
                nb_hands += 1
                win, bet = round.get_hand_winnings(hand)
                round.players[i].bet += bet
                round.players[i].win += win
            if round.dealer.hand.blackjack() and round.players[i].win<-round.bet:
                round.players[i].win = -round.bet # split/doubled hands lose only original bet if dealer has blackjack
        for i in range(round.player_number):
            round.total_bet += round.players[i].bet
            round.total_win += round.players[i].win
        #round_list.append(round)
        original_bet_list.append(round.bet * round.player_number)
        #bet_list.append(round.total_bet)
        pnl_list.append(round.total_win)
        pnl_per_original_bet_list.append(round.total_win/(round.bet*round.player_number))
        total_original_bet += round.bet * round.player_number
        total_bet += round.total_bet
        total_pnl += round.total_win
        sh.shuffle_back()

    EV_distribution_ag_TC = {}

    for i in range(len(TC_list)):
        if not (math.trunc(TC_list[i]) in EV_distribution_ag_TC):
            EV_distribution_ag_TC[math.trunc(TC_list[i])] = {"frequency":1, "accumulated_EV":pnl_per_original_bet_list[i], "average EV":0}
        else:
            EV_distribution_ag_TC[math.trunc(TC_list[i])]["frequency"] += 1
            EV_distribution_ag_TC[math.trunc(TC_list[i])]["accumulated_EV"] += pnl_per_original_bet_list[i]

    for key in EV_distribution_ag_TC:
        EV_distribution_ag_TC[key]["average EV"] = EV_distribution_ag_TC[key]["accumulated_EV"]/EV_distribution_ag_TC[key]["frequency"]

    keys=list(EV_distribution_ag_TC.keys())
    keys.sort()
    sorted_EV_distribution_ag_TC = {i:EV_distribution_ag_TC[i] for i in keys}
    EV_distribution_ag_TC = sorted_EV_distribution_ag_TC

    #print("TC List                  ", TC_list)
    #print("Original Bet List        ", original_bet_list)
    #print("Bet List", bet_list)
    #print("pnl List                 ", pnl_list)
    #print("pnl per original bet List", pnl_per_original_bet_list)
    print("Total Original Bet = ", total_original_bet)
    print("Total Bet = ", total_bet)
    print("Total PnL = ", total_pnl)
    print("Total PnL / Total Original Bet = ", total_pnl / total_original_bet)
    print("EV distribution ag TC = ", EV_distribution_ag_TC)