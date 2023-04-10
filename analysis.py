from random import randint
from doc import deal_board
from shuffler import Shuffler
import math


SHOE_SIZE = 6
BOARD_CARD_NUMBER = 20

cardNameMap={1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"T",11:"J",12:"Q",0:"K"}

def convertToCardname(serial):
    return cardNameMap[serial%13]

def calcTrueCount(board):
    TC=0
    for card in board:
        if card in ["2","3","4","5","6"]:
            TC +=1
        elif card in ["T","J","Q","K","A"]:
            TC -=1
    return TC

def calcBigCard(board):
    BC=0
    for card in board:
        if card in ["T","J","Q","K","A"]:
            BC +=1
    return BC

def calcSmallCard(board):
    SC=0
    for card in board:
        if card in ["2","3","4","5","6"]:
            SC +=1
    return SC

TCRollingStrategy=[{"max":4,"weight":{1:1,2:1,3:1,4:1}},{"max":8,"weight":{1:1,2:1,3:1,4:1,5:0.5,6:0.5,7:0.5,8:0.5}},
                   {"max":6,"weight":{1:1,2:1,3:1,4:1,5:0.5,6:0.5}},{"max":8,"weight":{1:1,2:0.9,3:0.8,4:0.7,5:0.6,6:0.5,7:0.4,8:0.3}}]

sh=Shuffler(SHOE_SIZE)

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
        








