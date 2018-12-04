import random
from itertools import chain
import numpy as np
from scipy.special import psi

class Pybtm(object):
    def __init__(self, path_to_b2w: str, path_to_i2w: str):
        self.b2w = {}
        self.biterms = {}
        self.biterm_length = None
        self.phi = None
        self.theta = None
        self.topics = None
        self.num_topic = None
        self.alpha = None
        self.beta = None
        self.rho = 1.
        self.minibatch_size = None
        self.iteration = None
        self.inner_iteration = None
        self.hyperparam_opt_interval = None

        with open(path_to_b2w, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            words = line.split(',')
            self.b2w[i] = (int(words[0]), int(words[1][:-1]))

        with open(path_to_i2w, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        self.i2w = {i:line[:-1] for i, line in enumerate(lines)}
        self.num_vocab = len(self.i2w)

    def fit(self, path: str, num_topic=10, minibatch_size=10, iteration=100, inner_iteration=20, hyperparam_opt_interval=10, seed=0):
        # initialize random seed
        np.random.seed(seed)
        random.seed(seed)

        # setting hyper parameter
        self.alpha = np.full(num_topic, num_topic/50)
        self.beta = 1/self.num_vocab
        self.num_topic = num_topic
        self.minibatch_size = minibatch_size
        self.iteration = iteration
        self.inner_iteration = inner_iteration
        self.hyperparam_opt_interval = hyperparam_opt_interval

        self.__input_biterms(path)
        self.__train_btm()

    def __nu(self, t, tau=1000, kappa=0.8):
        return np.power(t + tau, -kappa)

    def __resamling(self, batch, minibatch_size):
        array_length = len(batch)
        random.shuffle(batch)
        for j in range(int(array_length / minibatch_size)+1):
            minibatch = batch[minibatch_size*j : minibatch_size*(j+1)]
            if len(minibatch) > 0:
                yield minibatch

    def __train_btm(self):
        # intialize parameter
        beta_sum = self.beta * self.num_vocab
        nkv = np.random.rand(self.num_topic, self.num_vocab)
        nk = np.random.rand(self.num_topic)

        b_index = list(self.biterms.keys())

        t = 0
        for i in range(self.iteration):
            for minibatch in self.__resamling(b_index, self.minibatch_size):
                t += 1
                biterm_freq = np.array([self.biterms[b] for b in minibatch])
                minibatchsize = biterm_freq.sum()

                self.rho *= (1-self.__nu(t))
                weight = (self.__nu(t)*self.biterm_length) / (minibatchsize*self.rho)

                tmp = (self.rho*nk + self.alpha) / ((2*self.rho*nk + beta_sum)*(2*self.rho*nk + beta_sum + 1))

                i1_indecies, i2_indecies = [], []

                for b in minibatch:
                    i1, i2 = self.b2w[b]
                    i1_indecies.append(i1)
                    i2_indecies.append(i2)

                p = (((self.rho*nkv[:, i1_indecies] + self.beta) * (self.rho*nkv[:, i2_indecies] + self.beta)).T * tmp).T
                p /= p.sum(axis=0)
                p *= weight * biterm_freq

                nk += p.sum(axis=1)

                for b, (i1, i2) in enumerate(zip(i1_indecies, i2_indecies)):
                    nkv[:, i1] += p[:, b]
                    nkv[:, i2] += p[:, b]

            if (i+1) % self.hyperparam_opt_interval == 0:
                nk *= self.rho
                nkv *= self.rho
                self.rho = 1.0

                for _ in range(self.inner_iteration):
                    M = psi(nk.sum()+self.alpha.sum())  - psi(self.alpha.sum())
                    Mk = psi(nk+self.alpha) - psi(self.alpha)
                    self.alpha *= Mk / M

            print("\rTraining progress{:>4}%".format(i*int(100/self.iteration)+1), end="")

        print('\n')
        nk *= self.rho
        nkv *= self.rho

        self.phi = ((nkv+self.beta).T / (nkv+self.beta).sum(axis=1)).T
        self.theta = (nk + self.alpha) / (nk + self.alpha).sum()

    def __input_biterms(self, path: str):
        with open(path, 'r', encoding="utf-8") as f:
            self.biterms = {b:int(line[:-1]) for b, line in enumerate(f.readlines())}

        self.biterm_length = len(self.biterms)

    def get_topics(self):
        indices = list(set(chain.from_iterable(np.argpartition(-self.phi, 8, axis=1)[:, :8].tolist())))

        self.topics = {}

        for k in range(self.theta.shape[0]):
            phi_dic = []

            for idx in indices:
                phi_dic.append((self.i2w[idx], float(np.around(self.phi[k, idx], 3))))

            self.topics[k] = ((float(np.around(self.theta[k], 3)), sorted(phi_dic, key=lambda x: -x[1])))
