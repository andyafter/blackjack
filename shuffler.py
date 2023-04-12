from random import shuffle, randint

class Shuffler:

    _trueCount=0
    cardNameMap={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"T",11:"J",12:"Q",0:"K"}

    def __init__(self, SHOE_SIZE):
        self.buckets = []
        for i in range(38):
            self.buckets.append([])
        self.deck = list(range(SHOE_SIZE * 52))
        self.shoe_size = SHOE_SIZE
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
        
        self.cards_dealt.append(self.cards_buffer[0]) #a bucket of cards will be dealt from index 0

        if ifCovertToCardname:
            return self.convertToCardname(self.cards_buffer.pop(0))
        else:
            return self.cards_buffer.pop(0)

    def insert_into_bucket(self, card):
        # insert card into certain bucket in a randomly order
        # TODO: check if it's actually randomly inserted, if not, change the rules
        bucket = self.get_bucket_for_insert()
        self.buckets[bucket].append(card) #suppose shuffled-back card will be put at very end of a bucket
        #shuffle(self.buckets[bucket]) 

    def shuffle_back(self):
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
        self._trueCount=0
        return self._trueCount
    
'''   
if __name__ == "__main__":
    shuffler = Shuffler(6)
    for i in range(50):
        print("deal: %s " % shuffler.deal(False))
        print("card buffer: %s " % shuffler.cards_buffer)
        print("dealt cards %s " % shuffler.cards_dealt)
        if i%15==0:
            shuffler.shuffle_back()
'''