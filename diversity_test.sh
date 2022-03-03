python diversity_multiplexer_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_multiplexer_0.csv &
python diversity_parity_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_parity_0.csv &
python diversity_regression_test.py --no_fit_share -g 100 -s 50 -e 4 --cpu 10 --fit_partition 1000 -p 512 -n 100 --csv results2/diversity_regression_0.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_multiplexer_1.csv &
python diversity_parity_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_parity_1.csv &
python diversity_regression_test.py --no_fit_share -g 100 -s 50 -e 4 --cpu 10 --fit_partition 1000 -p 512 -n 100 --csv results2/diversity_regression_1.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_multiplexer_3.csv &
python diversity_parity_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_parity_3.csv &
python diversity_regression_test.py --no_fit_share -g 100 -s 50 -e 4 --cpu 10 --fit_partition 1000 -p 512 -n 100 --csv results2/diversity_regression_3.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_multiplexer_4.csv &
python diversity_parity_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_parity_4.csv &
python diversity_regression_test.py --no_fit_share -g 100 -s 50 -e 4 --cpu 10 --fit_partition 1000 -p 512 -n 100 --csv results2/diversity_regression_4.csv &

wait

python diversity_multiplexer_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_multiplexer_5.csv &
python diversity_parity_test.py --no_fit_share -g 256 -s 50 -e 4 --cpu 10 --fit_partition 0.001 -p 256 -n 100 --csv results2/diversity_parity_5.csv &
python diversity_regression_test.py --no_fit_share -g 100 -s 50 -e 4 --cpu 10 --fit_partition 1000 -p 512 -n 100 --csv results2/diversity_regression_5.csv &

wait
