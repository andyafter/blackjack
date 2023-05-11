#!/bin/bash

python run_hands.py 0 &
python run_hands.py 1 &
python run_hands.py 2 &
python run_hands.py 3 &
python run_hands.py 4 &
python run_hands.py 5 &
python run_hands.py 6 &
python run_hands.py 7 &
python run_hands.py 8 &
python run_hands.py 9 &

# wait for all background processes to finish
wait
