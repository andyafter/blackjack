import argparse
import os
import csv

from blackjack import *
import math
from datetime import datetime
from copy import deepcopy

from logger import Logger

LOGGER = Logger('ConsoleLogger', log_target='console').get_logger()
OUTPUT_FOLDER = "output_data/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
if not os.path.exists(OUTPUT_FOLDER+"output/"):
    os.makedirs(OUTPUT_FOLDER+"output/")
if not os.path.exists(OUTPUT_FOLDER+"stats/"):
    os.makedirs(OUTPUT_FOLDER+"stats/")


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Metric Engine")
    parser.add_argument("--rounds", help="how many rounds per simulation thread",
                        type=int, nargs="?", required=True, default=1000)
    parser.add_argument("--seq", type=int, required=False, default=1)

    return parser


if __name__ == "__main__":
    args = get_argparser().parse_args()
    ROUNDS = args.rounds

    basic_strategy = {}
    for i in range(-2,5):
        HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY, KNIGHT_STRATEGY = StrategyImporter('./strategies/BasicStrategy_'+str(i)+'.csv').import_player_strategy()
        basic_strategy[str(i)]=deepcopy([HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY, KNIGHT_STRATEGY])
    
    count_list = []
    TC_list=[]
    nb_hands = 0
    round_list = []
    original_bet_list=[]
    bet_list = []
    pnl_list = []
    original_bet_list_per1000 = []
    pnl_list_per1000 = []
    pnl_per_original_bet_list=[]
    cards_dealt_number_list=[]
    total_bet = 0
    total_pnl = 0
    total_original_bet = 0

    TC_rolling_strategy=[{"max":4,"weight":{1:1,2:1,3:1,4:1},"remaining_decks":5}, #0
                         {"max":4,"weight":{1:1,2:1,3:0.5,4:0.5},"remaining_decks":5}, #1
                         {"max":4,"weight":{1:1,2:0.5,3:0.5,4:0.5},"remaining_decks":5}, #2
                         {"max":4,"weight":{1:1,2:1,3:1,4:1},"remaining_decks":4.5}, #3
                         {"max":4,"weight":{1:1,2:1,3:1,4:0.5},"remaining_decks":5}, #4
                         {"max":4,"weight":{1:0.76,2:0.44,3:0.33,4:0.24},"remaining_decks":5},#5
                         {"max":4,"weight":{1:0.75,2:0.5,3:0.33,4:0.25},"remaining_decks":5}, #6
                         {"max":4,"weight":{1:0.72,2:0.42,3:0.30,4:0.20},"remaining_decks":5.5}, #7
                         {"max":8,"weight":{1:0.95,2:0.68,3:0.49,4:0.44,5:0.40,6:0.35,7:0.32,8:0.27},"remaining_decks":5}, #8 for 1 hand per round 
                         {"max":4,"weight":{1:0.90,2:0.51,3:0.43,4:0.38},"remaining_decks":5}]  #9 for 2 hands per round

    def roundbet(TC):
        if TC<=0:
            return 25
        elif TC<=0.25:
            return 25
        elif TC<=2:
            return 2500*TC
        else:
            return 2500*2
    
    player_number=5
    min_bet=25
    rolling_strategy_code=6

    sh = Shuffler(6, TC_rolling_strategy[rolling_strategy_code])
    start_time = datetime.now()
    LOGGER.info("Start Time ={data_time}".format(data_time=datetime.now().strftime("%H:%M:%S")))

    for r in range(ROUNDS):
        TC_list.append(sh._trueCount)
        if math.floor(2*sh._trueCount)/2 < -2:
            strategy_code=-2
        elif math.floor(2*sh._trueCount)/2 > 4:
            strategy_code=4
        else:
            strategy_code=math.floor(sh._trueCount)

        round = Round(roundbet(math.floor(4*sh._trueCount)/4), sh, basic_strategy[str(strategy_code)],player_number=player_number,min_bet=min_bet)  
        round.play_round()
        for i in range(round.player_number):
            for hand in round.players[i].hands:
                nb_hands += 1
                win, bet = round.get_hand_winnings(hand)
                round.players[i].bet += bet
                round.players[i].win += win
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
        cards_dealt_number_list.append(sh.shuffle_back())
        if r % 1000 == 999:
            original_bet_list_per1000.append(total_original_bet)
            pnl_list_per1000.append(total_pnl)


    EV_distribution_ag_TC = {}

    for i in range(len(TC_list)):
        if not (math.floor(TC_list[i]*4)/4 in EV_distribution_ag_TC):
            EV_distribution_ag_TC[math.floor(TC_list[i]*4)/4] = {"frequency":1, "accumulated_EV":pnl_per_original_bet_list[i], "average EV":0}
        else:
            EV_distribution_ag_TC[math.floor(TC_list[i]*4)/4]["frequency"] += 1
            EV_distribution_ag_TC[math.floor(TC_list[i]*4)/4]["accumulated_EV"] += pnl_per_original_bet_list[i]

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
    
    LOGGER.info("Total Rounds = {rounds}".format(rounds=ROUNDS))
    LOGGER.info("Hands per Rounds = {player_number}".format(player_number=player_number))
    LOGGER.info("Total Hands = {total_hands}".format(total_hands=ROUNDS * player_number))
    LOGGER.info("Average cards dealt per round = {average}".format(average=sum(cards_dealt_number_list)/len(cards_dealt_number_list)))
    LOGGER.info("strategy:{strategy}".format(strategy=str(TC_rolling_strategy[rolling_strategy_code])))
    LOGGER.info("Total Original Bet = {total}".format(total=total_original_bet))
    LOGGER.info("Total Bet = {total_bet}".format(total_bet=total_bet))
    LOGGER.info("Total PnL = {total_pnl}".format(total_pnl=total_pnl))
    LOGGER.info("Total PnL / Total Original Bet = {total}".format(total = total_pnl / total_original_bet))
    LOGGER.info("EV distribution ag TC = {ev}".format(ev=EV_distribution_ag_TC))
    #LOGGER.info("Original Bet List per 1000 rounds = ", original_bet_list_per1000)
    #LOGGER.info("PnL List per 1000 rounds = ", pnl_list_per1000)
    LOGGER.info("End Time = {end_time}".format(end_time=datetime.now().strftime("%H:%M:%S")))

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    LOGGER.info("Total Time = {time_spent}".format(time_spent = elapsed_time.total_seconds()))

    with open('{dest}output_{seq}.txt'.format(dest=OUTPUT_FOLDER+"output/", seq=args.seq),'a') as f:
        f.write("bet list per 1000 rounds\n")
        for i in range(len(original_bet_list_per1000)):
            f.write(str(original_bet_list_per1000[i]))
            f.write("\n")
        f.write("pnl list per 1000 rounds\n")
        for i in range(len(pnl_list_per1000)):
            f.write(str(pnl_list_per1000[i]))
            f.write("\n")
        f.close()

    data = {"total_rounds": ROUNDS,
            "player_number": player_number,
            "total_hands": ROUNDS * player_number,
            "average_cards_dealt_per_round": sum(cards_dealt_number_list)/len(cards_dealt_number_list),
            "strategy": str(TC_rolling_strategy[rolling_strategy_code]),
            "total_original_bet": total_original_bet,
            "total_bet": total_bet,
            "total_pnl": total_pnl,
            "ev_distribution_ag_TC": str(EV_distribution_ag_TC),
            }
    with open(OUTPUT_FOLDER+"stats/statistics_{seq}.csv".format(seq=args.seq), 'w') as csv_file:
        # write data into csv as a single row csv
        writer = csv.DictWriter(csv_file, fieldnames = data.keys())
        writer.writeheader()
        writer.writerow(data)


    