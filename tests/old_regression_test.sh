python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/diversity_older_regression_1.csv --seed 1 &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/diversity_older_regression_2.csv --seed 2 &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/diversity_older_regression_3.csv --seed 3 &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/diversity_older_regression_4.csv --seed 4 &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/diversity_older_regression_5.csv --seed 5 &

wait

python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/diversity_older_regression_1.csv --seed 1 &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/diversity_older_regression_2.csv --seed 2 &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/diversity_older_regression_3.csv --seed 3 &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/diversity_older_regression_4.csv --seed 4 &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/diversity_older_regression_5.csv --seed 5 &

wait 