from blackjack import *
import math
from datetime import datetime




if __name__ == "__main__":

    ROUNDS = 10000000
    player_number=4
    basic_strategy = {}
    for i in range(-2,5):
        HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = StrategyImporter('./strategies/BasicStrategy_'+str(i)+'.csv').import_player_strategy()
        basic_strategy[i]=[HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY]
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

    TC_rolling_strategy=[{"max":4,"weight":{1:1,2:1,3:1,4:1},"remaining_decks":5}, #0
                         {"max":4,"weight":{1:1,2:1,3:0.5,4:0.5},"remaining_decks":5}, #1
                         {"max":4,"weight":{1:1,2:0.5,3:0.5,4:0.5},"remaining_decks":5}, #2
                         {"max":4,"weight":{1:1,2:1,3:1,4:1},"remaining_decks":4.5}] #3

    def roundbet(TC):
        if TC<=-1:
            return 0.1
        elif TC<=0:
            return 0.25
        elif TC<=4:
            return 2*(2**TC)
        else:
            return 2*(2**4)
    
    rolling_strategy_code=0

    sh = Shuffler(6, TC_rolling_strategy[rolling_strategy_code])
    print("Start Time =",datetime.now().strftime("%H:%M:%S"))

    for r in range(ROUNDS):
        TC_list.append(sh._trueCount)
        if math.floor(sh._trueCount) < -2:
            strategy_code=-2
        elif math.floor(sh._trueCount) > 4:
            strategy_code=4
        else:
            strategy_code=math.floor(sh._trueCount)
        round = Round(roundbet(math.floor(sh._trueCount)), sh, basic_strategy[strategy_code],player_number=player_number)  
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
        if not (math.floor(TC_list[i]) in EV_distribution_ag_TC):
            EV_distribution_ag_TC[math.floor(TC_list[i])] = {"frequency":1, "accumulated_EV":pnl_per_original_bet_list[i], "average EV":0}
        else:
            EV_distribution_ag_TC[math.floor(TC_list[i])]["frequency"] += 1
            EV_distribution_ag_TC[math.floor(TC_list[i])]["accumulated_EV"] += pnl_per_original_bet_list[i]

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
    print("Total Rounds = ", ROUNDS)
    print("Hands per Rounds = ", player_number)
    print("Total Hands = ", ROUNDS * player_number)
    print("strategy:" + str(TC_rolling_strategy[rolling_strategy_code]))
    print("Total Original Bet = ", total_original_bet)
    print("Total Bet = ", total_bet)
    print("Total PnL = ", total_pnl)
    print("Total PnL / Total Original Bet = ", total_pnl / total_original_bet)
    print("EV distribution ag TC = ", EV_distribution_ag_TC)
    print("End Time =",datetime.now().strftime("%H:%M:%S"))