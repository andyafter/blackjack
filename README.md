# Blackjack

### Running

    python blackjack.py strategies/BasicStrategy.csv

### Definition of Terms

The simulator involves several concepts related to Blackjack game play:

- A _Hand_ is a single hand of Blackjack, consisting of two or more cards
- A _Round_ is single round of Blackjack, in which one or more players play their hands against the dealer's hand
- A _Shoe_ consists of multiple card decks consisting of SHOE_SIZE times 52 cards
- A _Game_ is a sequence of Rounds that starts with a fresh _Shoe_ and ends when the _Shoe_ gets reshuffled
