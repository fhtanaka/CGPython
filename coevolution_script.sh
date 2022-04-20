python coevolution_test.py --no_fit_share -g 100 -s 20 -e 1 --cpu 4 --fit_partition 1 -p 64 --controller_pop 18 -t 2 -n 100 --csv results/separated_genome_1.csv -f results/separate_genome_1.pkl --seed 1 -r 1 &
python coevolution_test.py --no_fit_share -g 100 -s 20 -e 1 --cpu 4 --fit_partition 1 -p 64 --controller_pop 18 -t 2 -n 100 --csv results/separated_genome_2.csv -f results/separate_genome_2.pkl --seed 2 -r 1 > results/saida2_2.txt &
python coevolution_test.py --no_fit_share -g 100 -s 20 -e 1 --cpu 3 --fit_partition 1 -p 64 --controller_pop 18 -t 2 -n 100 --csv results/separated_genome_3.csv -f results/separate_genome_3.pkl --seed 3 -r 1 > results/saida3_2.txt &

wait

python coevolution_test.py --no_fit_share -g 100 -s 20 -e 1 --cpu 6 --fit_partition 1 -p 64 --controller_pop 18 -t 2 -n 100 --csv results/separated_genome_4.csv -f results/separate_genome_4.pkl --seed 4 -r 1 &
python coevolution_test.py --no_fit_share -g 100 -s 20 -e 1 --cpu 5 --fit_partition 1 -p 64 --controller_pop 18 -t 2 -n 100 --csv results/separated_genome_5.csv -f results/separate_genome_5.pkl --seed 5 -r 1 > results/saida5_2.txt &
