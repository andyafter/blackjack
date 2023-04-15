from random import shuffle, randint

class Shuffler:

    _trueCount=0
    _count=0
    _roundCount=0
    pastCountList=[]
    cardNameMap={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"T",11:"J",12:"Q",0:"K"}

    def __init__(self, SHOE_SIZE, TCStrategy):
        self.buckets = []
        for i in range(38):
            self.buckets.append([])
        self.deck = list(range(SHOE_SIZE * 52))
        self.shoe_size = SHOE_SIZE
        self.TCStrategy=TCStrategy
        self.cards_map = {}
        self.cards_buffer = []
        self.cards_dealt = [] #cards dealt but yet to be shuffled back
        for card in self.deck:
            # incase if we need to mark the status of each card
            self.cards_map[card] = 1
            self.insert_into_bucket(card)
        self.check_total()
    
    def convertToCardname(self, serial):
        return self.cardNameMap[serial%13]

    def get_bucket_for_insert(self):
        """
            generate a bucket number randomly for inserting one card
        """
        target = randint(0, len(self.buckets) - 1)
        while len(self.buckets[target]) >= 10:   #by alex: should be >=10
            target = randint(0, len(self.buckets) - 1)
        return target

    def get_bucket_for_dealing(self):
        """
            generate a bucket number randomly for dealing, 
            WARNING:
            The assumption here is that the machine will always 
            deal card buckets that have cards between 7 to 10 cards.
        """
        target = randint(0, len(self.buckets) - 1)
        while len(self.buckets[target]) < 7:
            target = randint(0, len(self.buckets) - 1)
        return target
    
    def deal(self, ifCovertToCardname=True):
        if len(self.cards_buffer) == 0:
            bucket = self.get_bucket_for_dealing()
            self.cards_buffer = self.cards_buffer + self.buckets[bucket]
            # clean up the bucket
            self.buckets[bucket] = []
        
        c=self.cards_buffer.pop(0) #a bucket of cards will be dealt from index 0
        self.cards_dealt.append(c)
        self._count+=self.calcCardCount(self.convertToCardname(c))
        self._roundCount+=self.calcCardCount(self.convertToCardname(c))

        if ifCovertToCardname:
            return self.convertToCardname(c)
        else:
            return c

    def insert_into_bucket(self, card):
        # insert card into certain bucket in a randomly order
        # TODO: check if it's actually randomly inserted, if not, change the rules
        bucket = self.get_bucket_for_insert()
        self.buckets[bucket].append(card) #suppose shuffled-back card will be put at very end of a bucket
        #shuffle(self.buckets[bucket]) 

    def shuffle_back(self):
        self.pastCountList.append(self._roundCount) #record round count
        self._roundCount=0 # clear round count
        if len(self.pastCountList)>self.TCStrategy["max"]:
            self.pastCountList.pop(0)
        self._count=0 # reset accumulative count
        for i in range (min(len(self.pastCountList),self.TCStrategy["max"])):
            self._count += self.pastCountList[-1-i] * self.TCStrategy["weight"][i+1]
        
        shuffle(self.cards_dealt) #TODO: improve accuracy
        for card in self.cards_dealt:
            self.insert_into_bucket(card)
        self.cards_dealt=[] #clear dealt cards 
        self.check_total()

    def check_total(self):
        deck_size = len(self.cards_buffer)
        for bucket in self.buckets:
            deck_size += len(bucket)
        if deck_size != self.shoe_size * 52:
            print("deck size error, incomplete deck!")

    @property
    def trueCount(self):
        self._trueCount=+1
        return self._trueCount
    
    def calcBoardCount(self,board):
        TC=0
        for card in board:
            TC+=self.calcCardCount(card)
        return TC
    
    def calcCardCount(self,card):
        if card in ["2","3","4","5","6"]:
            return 1
        elif card in ["T","J","Q","K","A"]:
            return -1
        else:
            return 0
    

if __name__ == "__main__":
    sh = Shuffler(6,{"max":4,"weight":{1:1,2:1,3:1,4:1}})
    
    for i in range(50):
        print("deal: %s " % sh.deal(True))
        print("count",sh._count)
        #print("card buffer: %s " % sh.cards_buffer)
        #print("dealt cards %s " % sh.cards_dealt)
        if i%15==0:
            sh.shuffle_back()

