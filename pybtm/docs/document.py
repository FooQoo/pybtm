from collections import defaultdict
from itertools import combinations

class Document(object):
    def __init__(self):
        self.w2i = defaultdict(lambda: len(self.w2i))
        self.w2b = defaultdict(lambda: len(self.w2b))
        self.biterms = defaultdict(int)

    def transform_docs_to_biterm(self, path: str):

        with open(path, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            words = line.split()
            biterms = [self.w2b[tuple(sorted([self.w2i[b[0]], self.w2i[b[1]]]))] for b in combinations(words, 2) if b[0] != b[1]]

            for b in biterms:
                self.biterms[b] += 1

    def export_to_txt(self, path: str):

        with open(path + '/i2w.txt', 'w', encoding="utf-8") as f:
            for w2i in sorted(self.w2i.items(), key=lambda w2i: w2i[1]):
                f.write('{}\n'.format(w2i[0]))

        with open(path + '/b2w.txt', 'w', encoding="utf-8") as f:
            for w2b in sorted(self.w2b.items(), key=lambda w2b: w2b[1]):
                f.write('{0},{1}\n'.format(w2b[0][0], w2b[0][1]))

        with open(path + '/biterms.txt', 'w', encoding="utf-8") as f:
            for biterms in sorted(self.biterms.items(), key=lambda biterms: biterms[0]):
                f.write('{}\n'.format(biterms[1]))
