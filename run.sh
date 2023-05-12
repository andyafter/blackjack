
# for c6a.48xlarge, the optimal number of processes is 95
for ((i=0; i<=$1; i++))
do
   python3 run_hands.py --rounds $2 --seq $i &
done

# wait for all background processes to finish
wait