for i in {0..1}
do
   python3 run_hands.py $i &
done

# wait for all background processes to finish
wait