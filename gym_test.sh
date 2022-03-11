python diversity_gym_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/no_share/diversity_gym_1.pkl --csv results/no_share/diversity_gym_1.csv --seed 1 &
python diversity_gym_test.py -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/share/diversity_gym_1.pkl --csv results/share/diversity_gym_1.csv --seed 1 &
wait

python diversity_gym_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/no_share/diversity_gym_2.pkl --csv results/no_share/diversity_gym_2.csv --seed 2 &
python diversity_gym_test.py -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/share/diversity_gym_2.pkl --csv results/share/diversity_gym_2.csv --seed 2 &
wait

python diversity_gym_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/no_share/diversity_gym_3.pkl --csv results/no_share/diversity_gym_3.csv --seed 3 &
python diversity_gym_test.py -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/share/diversity_gym_3.pkl --csv results/share/diversity_gym_3.csv --seed 3 &
wait

python diversity_gym_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/no_share/diversity_gym_4.pkl --csv results/no_share/diversity_gym_4.csv --seed 4 &
python diversity_gym_test.py -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/share/diversity_gym_4.pkl --csv results/share/diversity_gym_4.csv --seed 4 &
wait

python diversity_gym_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/no_share/diversity_gym_5.pkl --csv results/no_share/diversity_gym_5.csv --seed 5 &
python diversity_gym_test.py -g 1000 -s 1000 -e 4 --cpu 15 --fit_partition 1 -p 450 -t 8 -n 100 -f results/share/diversity_gym_5.pkl --csv results/share/diversity_gym_5.csv --seed 5 &
wait
