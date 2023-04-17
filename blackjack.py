from shuffler import Shuffler
from strategy_importer import StrategyImporter

class Hand:
    """
    Represents a hand, either from the dealer or from the player
    """
    _value = 0
    _aces = []
    _aces_soft = 0
    _is_soft=False
    splithand = False
    surrender = False
    doubled = False
    pnl=0
    card_values={"A":1,"K":10,"Q":10,"J":10,"T":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2} # A is 1 by default

    def __init__(self, cards): # cards is a list of card, each card is a letter from A to K
        self.cards = cards
        self._value=self.value 

    def __str__(self):
        h = ""
        for c in self.cards:
            h += "%s " % c
        return h
    
    @property
    def contain_ace(self):
        self._contain_ace=False
        for c in self.cards:
            if c == "A":
                self._contain_ace=True
                return self._contain_ace
        return self._contain_ace

    @property
    def value(self):
        """
        Returns: The current value of the hand (aces are either counted as 1 or 11).
        """
        self._value = 0
        for c in self.cards:
            self._value += self.card_values[c] # A is 1 by default
        if self._value<=11 and self.contain_ace:
            self._value+=10
            self._is_soft=True
        return self._value

    @property
    def aces(self):
        """
        Returns: The all aces in the current hand.
        """
        self._aces = []
        for c in self.cards:
            if c.name == "Ace":
                self._aces.append(c)
        return self._aces

    @property
    def aces_soft(self):
        """
        Returns: The number of aces valued as 11
        """
        self._aces_soft = 0
        for ace in self.aces:
            if ace.value == 11:
                self._aces_soft += 1
        return self._aces_soft

    def soft(self):
        """
        Determines whether the current hand is soft (soft means that it consists of aces valued at 11).
        """
        return self._is_soft

    def splitable(self):
        """
        Determines if the current hand can be splitted.
        """
        if self.length() == 2 and self.cards[0] == self.cards[1]:
            if self.cards[0] == "A" and self.splithand:
                return False
            else:
                return True
        else:
            return False

    def blackjack(self):
        """
        Check a hand for a blackjack
        """
        if not self.splithand and self.value == 21 and self.length() == 2:
            return True
        else:
            return False

    def busted(self):
        """
        Checks if the hand is busted.
        """
        if self.value > 21:
            return True
        else:
            return False

    def add_card(self, card):
        """
        Add a card to the current hand.
        """
        self.cards.append(card)
        self._value=self.value #whenever a new card is added, the value will be calculated again as well as whether it is soft

    def split(self):
        """
        Split the current hand.
        Returns: The new hand created from the split.
        """
        self.splithand = True
        c = self.cards.pop()
        new_hand = Hand([c])
        new_hand.splithand = True
        return new_hand

    def length(self):
        """
        Returns: The number of cards in the current hand.
        """
        return len(self.cards)
    
sh=Shuffler(6,{"max":4,"weight":{1:1,2:1,3:1,4:1}})

class Player:
    """
    Represent a player
    """
    def __init__(self, basic_strategy, hand=None, dealer_hand=None):
        self.hands = [hand]
        self.dealer_hand = dealer_hand
        self.basic_strategy = basic_strategy
        
    def set_hands(self, new_hand, new_dealer_hand):
        self.hands = [new_hand]
        self.dealer_hand = new_dealer_hand

    def play(self, shoe):
        for hand in self.hands:
            HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = self.playStrategy(sh)
            self.play_hand(hand, shoe, HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY)

    def play_hand(self, hand, shoe, HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY):
        
        while not hand.busted() and not hand.blackjack():
            if hand.length() < 2:
                if hand.cards[0]=="A":  #split Aces can only draw one card
                    self.hit(hand, shoe)
                    break
                else:
                    self.hit(hand, shoe)

            if hand.soft():
                flag = SOFT_STRATEGY[hand.value][self.dealer_hand.cards[0]]
            elif hand.splitable() and self.hand_numbers<=4:
                flag = PAIR_STRATEGY[hand.value][self.dealer_hand.cards[0]]
            else:
                flag = HARD_STRATEGY[hand.value][self.dealer_hand.cards[0]]

            if flag == 'DH' or flag == 'DS':
                if hand.length() == 2:
                    print ("Double Down")
                    hand.doubled = True
                    self.hit(hand, shoe)
                    print("value = %d" % hand.value)
                    break
                else:
                    flag = flag[1] # if cannot double, then stand (DS) or hit (DH)

            if flag == 'US' or flag == 'UH':
                if hand.length() == 2 and hand.splithand == False:
                    print ("Surrender")
                    hand.surrender = True
                    break
                else:
                    flag = flag[1] # if cannot double, then stand (US) or hit (UH)

            if flag == 'H':
                self.hit(hand, shoe)
                if hand.busted():
                    print ("Busted, value=%d" % hand.value)

            if flag == 'P':
                self.split(hand, shoe, HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY)
                break

            if flag == 'S':
                print ("Stand, value = %d" % hand.value)
                break

    def hit(self, hand, shoe):
        c = shoe.deal()
        hand.add_card(c)
        print ("Hitted: %s" % c)

    def split(self, hand, shoe, HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY):
        self.hands.append(hand.split())
        print ("Splitted %s" % hand)
        self.play_hand(hand, shoe, HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY)

    def playStrategy(self,sh): #adjust play strategy according to True Count
        HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY = self.basic_strategy
        return HARD_STRATEGY, SOFT_STRATEGY, PAIR_STRATEGY
    
    @property
    def hand_numbers(self):
        return len(self.hands) 

class Dealer:
    """
    Represent the dealer
    """
    def __init__(self, hand=None):
        self.hand = hand

    def set_hand(self, new_hand):
        self.hand = new_hand

    def play(self, shoe):
        while self.hand.value < 17: #deal stand on soft 17
            self.hit(shoe)
        print("Dealer's hand: %s, value = %d" % (self.hand, self.hand.value))

    def hit(self, shoe):
        c = shoe.deal()
        self.hand.add_card(c)
        print ("Dealer hitted: %s" %c)

    # Returns an array of 6 numbers representing the probability that the final score of the dealer is
    # [17, 18, 19, 20, 21, Busted] '''
    # TODO Differentiate 21 and BJ
    # TODO make an actual tree, this is false AF
    def get_probabilities(self) :
        start_value = self.hand.value
        # We'll draw 5 cards no matter what an count how often we got 17, 18, 19, 20, 21, Busted

class Round:
    "represents a round of blackjack"
    total_win=0
    total_bet=0

    def __init__(self, bet, sh, basic_strategy, player_number=5): #sh is a shuffler object
        self.bet = bet
        self.sh=sh
        self.basic_strategy=basic_strategy
        self.player_number=player_number
        self.players=[]
    
    def play_round(self):
        "play a round"
        print("round begins")
        player_initial_deal=[None] * self.player_number
        for i in range(self.player_number):
            self.players.append(Player(self.basic_strategy))
            player_initial_deal[i]=Hand([self.sh.deal()]) # deal a first card to each player
        self.dealer=Dealer(Hand([self.sh.deal()])) # deal a card to the dealer
        for i in range(self.player_number):
            player_initial_deal[i].add_card(self.sh.deal()) # deal a second card to each player
            self.players[i].set_hands(player_initial_deal[i],self.dealer.hand)
            print("player %d, hand %s" % (i, player_initial_deal[i]))
            print("dealer hand %s" % self.dealer.hand)

        for i in range(self.player_number):
            print("player %d plays" % i)
            self.players[i].play(self.sh)
        self.dealer.play(self.sh)

    
    def get_hand_winnings(self, hand): # must first play the round
        win = 0.0
        bet = self.bet
        if not hand.surrender:
            if hand.busted():
                status = "LOST"
            else:
                if hand.blackjack():
                    if self.dealer.hand.blackjack():
                        status = "PUSH"
                    else:
                        status = "WON 3:2"
                elif self.dealer.hand.busted():
                    status = "WON"
                elif self.dealer.hand.value < hand.value:
                    status = "WON"
                elif self.dealer.hand.value > hand.value:
                    status = "LOST"
                elif self.dealer.hand.value == hand.value:
                    if self.dealer.hand.blackjack():
                        status = "LOST"  # player's 21 vs dealers blackjack
                    else:
                        status = "PUSH"
        else:
            status = "SURRENDER"

        if status == "LOST":
            win += -1
        elif status == "WON":
            win += 1
        elif status == "WON 3:2":
            win += 1.5
        elif status == "SURRENDER":
            win += -0.5
        if hand.doubled:
            #win *= 2  this line should be deleted
            bet *= 2

        win *= bet

        return win, bet
    
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