# run an toy example for BTM
mkdir -p ./output
input_dir=sample-data/yahoonews.txt
output_dir=./output/

b2w_dir=./output/b2w.txt
i2w_dir=./output/i2w.txt
biterms_dir=./output/biterms.txt
num_topic=10
minibatchsize=10
iteration=100

echo "================= Index Docs ==============="
python indexDocs.py $input_dir $output_dir
wc -l ./output/*

echo "=============== Topic Learning ============="
python train.py $b2w_dir $i2w_dir $biterms_dir $num_topic $minibatchsize $iteration