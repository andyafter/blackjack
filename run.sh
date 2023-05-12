for i in {0..9}
do
   python run_hands.py $i &
done

# wait for all background processes to finish
wait