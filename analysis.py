from random import randint
from shuffler import Shuffler
import matplotlib.pyplot as plt
import math


SHOE_SIZE = 6
BOARD_CARD_NUMBER = 9

cardNameMap={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"T",11:"J",12:"Q",0:"K"}

def calculate_true_count(board):
    TC=0
    for card in board:
        if card in ["2","3","4","5","6"]:
            TC +=1
        elif card in ["T","J","Q","K","A"]:
            TC -=1
    return TC

def calculate_big_card(board):
    BC=0
    for card in board:
        if card in ["T","J","Q","K","A"]:
            BC +=1
    return BC

def calculate_small_card(board):
    SC=0
    for card in board:
        if card in ["2","3","4","5","6"]:
            SC +=1
    return SC

TCRollingStrategy=[{"max":4,"weight":{1:1,2:1,3:1,4:1}},{"max":8,"weight":{1:1,2:1,3:1,4:1,5:0.5,6:0.5,7:0.5,8:0.5}},
                   {"max":6,"weight":{1:1,2:1,3:1,4:1,5:0.5,6:0.5}},{"max":8,"weight":{1:1,2:0.9,3:0.8,4:0.7,5:0.6,6:0.5,7:0.4,8:0.3}}]

def reappear_distribution(sh):
    SIZE=1000000
    cardSequence=[]
    board_size=0
    clearFrequency=10000
    dist={}
    for i in range(SIZE):
        newCard=sh.deal(False)
        board_size+=1
        cardSequence.append(newCard)
        j=1
        while j<len(cardSequence) and newCard!=cardSequence[-1-j]:
            j+=1
        if j<len(cardSequence):
            if int(j/BOARD_CARD_NUMBER) not in dist:
                dist[int(j/BOARD_CARD_NUMBER)]=1
            else:
                dist[int(j/BOARD_CARD_NUMBER)]+=1
            cardSequence[-1-j]=-1 #-1 means this card has reappeared
        if board_size==BOARD_CARD_NUMBER:
            board_size=0
            sh.shuffle_back()
        if i%clearFrequency==0:
            while cardSequence[0]==-1: #clear consecutive reappeared cards in the beginning of the sequence
                cardSequence.pop(0)
    #print(dist)
    plt.bar(dist.keys(),list(map(lambda x:x/SIZE, dist.values())))
    plt.show()

def delay_effect(sh):

    def common_cards(listA,listB):
        count=0
        for card in listA:
            if card in listB:
                count+=1
        return count

    SIZE=1000000
    cardSequence=[]
    boardSequence=[[]]
    cardCount=0
    boardCount=0
    dist={}
    times={}
    for i in range(SIZE):
        newCard=sh.deal(False)
        cardCount+=1
        if cardCount>=BOARD_CARD_NUMBER:
            cardCount=0
            boardCount+=1
            boardSequence.append([])
            sh.shuffle_back()
        boardSequence[boardCount].append(newCard)
    for i in range(len(boardSequence)):
        for j in range(i+1,min(i+30,len(boardSequence))):
            if j-i not in dist:
                dist[j-i]=common_cards(boardSequence[i],boardSequence[j])
                times[j-i]=1
            else:
                dist[j-i]+=common_cards(boardSequence[i],boardSequence[j])
                times[j-i]+=1
    for key in dist:
        if times[key]!=0:
            dist[key]=dist[key]/times[key]
    print(dist)
    plt.bar(dist.keys(),dist.values())
    plt.show()
            

sh=Shuffler(SHOE_SIZE,{"max":4,"weight":{1:1,2:1,3:1,4:1},"remaining_decks":5})
#reappearDistribution()
delay_effect(sh)


'''
TCList=[]
bigCardList=[]
smallCardList=[]
TCSequence=[]
HANDS=200000
TC_ROLLING_STRATEGY=0

for i in range(HANDS):
    BOARD_CARD_NUMBER=randint(15,15)
    thisBoard=list(map(convertToCardname,deal_board(sh,BOARD_CARD_NUMBER)))
    TCList.append(calcTrueCount(thisBoard))
    bigCardList.append(calcBigCard(thisBoard))
    smallCardList.append(calcSmallCard(thisBoard))

    #calculate rolling True Counts
    if i<TCRollingStrategy[TC_ROLLING_STRATEGY]["max"]:
        TCSequence.append(0)
    else:
        GC=0
        for j in range(i-TCRollingStrategy[TC_ROLLING_STRATEGY]["max"],i):
            GC+=TCList[j]*TCRollingStrategy[TC_ROLLING_STRATEGY]["weight"][i-j]
        TCSequence.append(GC/5) #TODO: auto-calculate remaining decks

#print(TCList)
#print(smallCardList)
#print(bigCardList)
#print(TCSequence)

TCFrequency={}
TCBigCard={}
TCSmallCard={}
TCBigMinusSmallCard={}

for i in range(-10,11):
    TCFrequency[i]=0
    TCBigCard[i]=0
    TCSmallCard[i]=0
    TCBigMinusSmallCard[i]=0

for i in range(TCRollingStrategy[TC_ROLLING_STRATEGY]["max"],HANDS):
    TCFrequency[math.trunc(TCSequence[i])]+=1
    TCBigCard[math.trunc(TCSequence[i])]+=bigCardList[i]
    TCSmallCard[math.trunc(TCSequence[i])]+=smallCardList[i]
    TCBigMinusSmallCard[math.trunc(TCSequence[i])]+=(bigCardList[i]-smallCardList[i])

for i in range(-10,11):
    if TCFrequency[i]!=0:
        TCBigCard[i]/=TCFrequency[i]
        TCSmallCard[i]/=TCFrequency[i]
        TCBigMinusSmallCard[i]/=TCFrequency[i]

print("TC Frequency", TCFrequency)
print("avg small card number", TCSmallCard)
print("avg big card number", TCBigCard)
print("avg big minus small card number", TCBigMinusSmallCard)
'''

