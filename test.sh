python3 generic_regression_test.py --cpu 4 -f cache/fit_share_75.pkl --species_threshold .75 | tee results/fit_share_75.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_75.pkl --no_fit_share --species_threshold .75 > results/no_fit_share_75.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_8.pkl --species_threshold .8 | tee results/fit_share_8.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_8.pkl --no_fit_share --species_threshold .8 > results/no_fit_share_8.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_85.pkl --species_threshold .85 | tee results/fit_share_85.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_85.pkl --no_fit_share --species_threshold .85 > results/no_fit_share_85.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_9.pkl --species_threshold .9 | tee results/fit_share_9.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_9.pkl --no_fit_share > results/no_fit_share_9.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_75_2.pkl --species_threshold .75 | tee results/fit_share_75_2.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_75_2.pkl --no_fit_share --species_threshold .75 > results/no_fit_share_75_2.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_8_2.pkl --species_threshold .8 | tee results/fit_share_8_2.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_8_2.pkl --no_fit_share --species_threshold .8 > results/no_fit_share_8_2.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_85_2.pkl --species_threshold .85 | tee results/fit_share_85_2.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_85_2.pkl --no_fit_share --species_threshold .85 > results/no_fit_share_85_2.txt &

wait

python3 generic_regression_test.py --cpu 4 -f cache/fit_share_9_2.pkl --species_threshold .9 | tee results/fit_share_9_2.txt &
python3 generic_regression_test.py --cpu 4 -f cache/no_fit_share_9_2.pkl --no_fit_share > results/no_fit_share_9_2.txt &


