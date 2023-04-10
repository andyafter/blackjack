from shuffler import Shuffler

class Hand(object):
    """
    Represents a hand, either from the dealer or from the player
    """
    _value = 0
    _aces = []
    _aces_soft = 0
    _isSoft=False
    splithand = False
    surrender = False
    doubled = False
    pnl=0
    _cardValues={"A":1,"K":10,"Q":10,"J":10,"T":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2} # A is 1 by default

    def __init__(self, cards): # cards is a list of card, each card is a letter from A to K
        self.cards = cards

    def __str__(self):
        h = ""
        for c in self.cards:
            h += "%s " % c
        return h
    
    @property
    def containAce(self):
        self._containAce=False
        for c in self.cards:
            if c == "A":
                self._containAce=True
                return self._containAce
        return self._containAce

    @property
    def value(self):
        """
        Returns: The current value of the hand (aces are either counted as 1 or 11).
        """
        self._value = 0
        for c in self.cards:
            self._value += self._cardValues[c] # A is 1 by default
        if self._value<=11 and self.containAce:
            self._value+=10
            self._isSoft=True
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
        if self.aces_soft > 0:
            return True
        else:
            return False

    def splitable(self):
        """
        Determines if the current hand can be splitted.
        """
        if self.length() == 2 and self.cards[0] == self.cards[1]:
            if self.cards[0].name == "Ace" and self.splithand:
                return False
            else:
                return True
        else:
            return False

    def blackjack(self):
        """
        Check a hand for a blackjack
        """
        if not self.splithand and self.value == 21:
            if self.length() == 2:
                return True
            else:
                return False
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
    
sh=Shuffler(6)

class Round:
    "represents a round of blackjack"
    def __init__(self, bet, sh, player=5): #sh is a shuffler object
        self.bet = bet
        self.player=player
        self.playerHands=[]
        for i in range(self.player):
            self.playerHands.append(Hand([sh.deal(),sh.deal()]))
        self.dealerHand=Hand([sh.deal()])
    
    def playHand(self, hand):
        "play a hand"






        if hand.blackjack():
            hand.pnl=self.bet*1.5
            return
        while True:
            if hand.value>=17:
                break
            hand.add_card(sh.deal())
            if hand.busted():
                hand.pnl=-self.bet
                return
        if hand.value>self.dealerHand.value:
            hand.pnl=self.bet
        elif hand.value==self.dealerHand.value:
            hand.pnl=0
        else:
            hand.pnl=-self.bet
        return