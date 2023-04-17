from blackjack import *


if __name__ == "__main__":

    ROUNDS = 1
    HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = StrategyImporter('./strategies/BasicStrategy.csv').import_player_strategy()
    basic_strategy = [HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY]
    countings = []
    nb_hands = 0
    round_list = []
    bet_list = []
    pnl_list = []
    total_bet = 0
    total_pnl = 0
    sh = Shuffler(6, {"max": 4, "weight": {1: 1, 2: 1, 3: 1, 4: 1}})

    for r in range(ROUNDS):
        round = Round(1, sh, basic_strategy)  # TODO: vary bet size according to True Count
        round.play_round()
        for i in range(round.player_number):
            for hand in round.players[i].hands:
                nb_hands += 1
                win, bet = round.get_hand_winnings(hand)
                round.total_bet += bet
                round.total_win += win
        round_list.append(round)
        bet_list.append(round.total_bet)
        pnl_list.append(round.total_win)
        total_bet += round.total_bet
        total_pnl += round.total_win
        sh.shuffle_back()

    print("Bet List", bet_list)
    print("pnl List", pnl_list)
    print("Total Bet = ", total_bet)
    print("Total PnL = ", total_pnl)
        
        #countings += game.shoe.count_history

        #print("WIN for Game no. %d: %s (%s bet)" % (g + 1, "{0:.2f}".format(game.get_money()), "{0:.2f}".format(game.get_bet())))

    #sume = 0.0
    #total_bet = 0.0
    #for value in moneys:
    #    sume += value
    #for value in bets:
    #    total_bet += value