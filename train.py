import sys, os
from src.model.pybtm import Pybtm

if __name__ == "__main__":

    if len(sys.argv) < 7:
        print('Usage: python %s <b2w_dir> <i2w_dir> <biterms_dir> <num_topic> <minibatchsize> <iteration>' % sys.argv[0])
        exit(1)

    b2w_dir = sys.argv[1]
    i2w_dir = sys.argv[2]
    biterms_dir = sys.argv[3]
    num_topic = int(sys.argv[4])
    minibatch_size = int(sys.argv[5])
    iteration = int(sys.argv[6])
    
    pybtm = Pybtm(path_to_b2w='output/w2b.txt', path_to_i2w='output/i2w.txt')
    pybtm.fit('output/biterms.txt', num_topic=num_topic, minibatch_size=minibatch_size, iteration=iteration)
    pybtm.get_topics()

    for topic in sorted(pybtm.topics.items(), key=lambda x: -x[1][0]):
        print(topic[1][0], topic[1][1][:5], '\n')

