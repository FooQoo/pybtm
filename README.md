# pybtm

ツイートなど短文書に特化したトピックモデルの一種である Biterm topic model の実装です．  
この実装では Stochastic Collapsed Variational Bayes Zero と呼ばれる推論アルゴリズムをミニバッチ学習に対応させており，従来の Gibbs sampling と比較して効率的にトピックを学習できます．

## QuickStart

- run pybtm

```
sh etc/run.sh
```

## Requirement

- numpy
- scipy

## Useful tool

- [pretweet.py](https://gist.github.com/FooQoo/c028e522d99b3209f58d035a89c802ee)
  - ツイートテキストに前処理を行うスクリプト

## Reference

- [Stochastic collapsed variational bayesian inference for biterm
  topic model](https://ieeexplore.ieee.org/document/7727629) - IJCNN - Awaya et al.
