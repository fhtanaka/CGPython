python diversity_multiplexer_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/no_share/diversity_multiplexer_v2_1.csv &
python diversity_parity_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/no_share/diversity_parity_v2_1.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/no_share/diversity_regression_v2_1.csv &

python diversity_multiplexer_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/share/diversity_multiplexer_v2_1.csv &
python diversity_parity_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/share/diversity_parity_v2_1.csv &
python diversity_regression_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/share/diversity_regression_v2_1.csv &

wait
python diversity_multiplexer_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/no_share/diversity_multiplexer_v2_2.csv &
python diversity_parity_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/no_share/diversity_parity_v2_2.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/no_share/diversity_regression_v2_2.csv &

python diversity_multiplexer_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/share/diversity_multiplexer_v2_2.csv &
python diversity_parity_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/share/diversity_parity_v2_2.csv &
python diversity_regression_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/share/diversity_regression_v2_2.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/no_share/diversity_multiplexer_v2_3.csv &
python diversity_parity_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/no_share/diversity_parity_v2_3.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/no_share/diversity_regression_v2_3.csv &

python diversity_multiplexer_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/share/diversity_multiplexer_v2_3.csv &
python diversity_parity_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/share/diversity_parity_v2_3.csv &
python diversity_regression_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/share/diversity_regression_v2_3.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/no_share/diversity_multiplexer_v2_4.csv &
python diversity_parity_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/no_share/diversity_parity_v2_4.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/no_share/diversity_regression_v2_4.csv &

python diversity_multiplexer_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/share/diversity_multiplexer_v2_4.csv &
python diversity_parity_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/share/diversity_parity_v2_4.csv &
python diversity_regression_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/share/diversity_regression_v2_4.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/no_share/diversity_multiplexer_v2_5.csv &
python diversity_parity_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/no_share/diversity_parity_v2_5.csv &
python diversity_regression_test.py --no_fit_share -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/no_share/diversity_regression_v2_5.csv &

python diversity_multiplexer_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.001 -p 500 -t 2 -n 100 --csv results/share/diversity_multiplexer_v2_5.csv &
python diversity_parity_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 0.01 -p 500 -t 2 -n 100 --csv results/share/diversity_parity_v2_5.csv &
python diversity_regression_test.py -g 1000 -s 1000 -e 4 --cpu 5 --fit_partition 1000 -p 500 -t 2 -n 100 --csv results/share/diversity_regression_v2_5.csv &

wait
