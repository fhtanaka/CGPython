python single_genome_coevolution.py --no_fit_share -g 100 -s 20 -e 1 --cpu 4 --fit_partition 1 -p 1024 -t 2 -n 100 --csv results/single_genome_1.csv -f results/single_genome_1.pkl --seed 1 -r 1 &
python single_genome_coevolution.py --no_fit_share -g 100 -s 20 -e 1 --cpu 4 --fit_partition 1 -p 1024 -t 2 -n 100 --csv results/single_genome_2.csv -f results/single_genome_2.pkl --seed 2 -r 1 > results/saida2.txt &
python single_genome_coevolution.py --no_fit_share -g 100 -s 20 -e 1 --cpu 3 --fit_partition 1 -p 1024 -t 2 -n 100 --csv results/single_genome_3.csv -f results/single_genome_3.pkl --seed 3 -r 1 > results/saida3.txt &

wait

python single_genome_coevolution.py --no_fit_share -g 100 -s 20 -e 1 --cpu 6 --fit_partition 1 -p 1024 -t 2 -n 100 --csv results/single_genome_4.csv -f results/single_genome_4.pkl --seed 4 -r 1 &
python single_genome_coevolution.py --no_fit_share -g 100 -s 20 -e 1 --cpu 5 --fit_partition 1 -p 1024 -t 2 -n 100 --csv results/single_genome_5.csv -f results/single_genome_5.pkl --seed 5 -r 1 > results/saida5.txt &
