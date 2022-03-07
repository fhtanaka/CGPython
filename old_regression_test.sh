python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/old_regression_1.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/old_regression_2.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/old_regression_3.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/old_regression_4.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/no_share/old_regression_5.csv &

wait

python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/old_regression_1.csv &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/old_regression_2.csv &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/old_regression_3.csv &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/old_regression_4.csv &
python diversity_regression_test.py -g 1000 -s 30 -e 2 --cpu 6 --fit_partition 1000 -p 1000 -t 20 -n 100 -m 0.2 --species_threshold 0.8 --csv results/share/old_regression_5.csv &

wait 