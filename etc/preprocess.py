'''
requirement : janome, pandas
'''

import re
from janome.tokenizer import Tokenizer
import unicodedata
from html import unescape
import pandas as pd

class Pretweet(object):
    def __init__(self):
        self.tokenizer = Tokenizer()
        
    def cleaning(self, text):
        text = ' ' + unescape(text) + ' '

        stopwords = []
        
        if text[1:3] == 'RT':
            stopwords.append('RT')

        stopwords += re.findall(r'\s@[a-zA-Z1-9]+\s', text)
        stopwords += re.findall(r'\s#\w+\s', text)
        stopwords += [g[0] for g in re.findall(r'((https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+))', text)]
        
        return re.sub('(' + '|'.join(stopwords) + ')', '', text)[1:-1]
        
    def annotation(self, text):
        return [(token.base_form,  token.part_of_speech.split(',')) for token in self.tokenizer.tokenize(text)]
    
    def normalization(self, text):
        return unicodedata.normalize("NFKC", text)
        
    def is_not_my_stopword(self, word, attr):
        if attr[0] == '名詞' and attr[1] in ['固有名詞', '一般',  'サ変接続']:
            if (re.match(u'[一-龥ぁ-んァ-ンa-zA-Zａ-ｚＡ-Ｚ1-9１-９]', word) and len(word) >= 2) or (re.match(u'[一-龥]', word) and len(word) == 1):
                return True
        
        return False
                
    def segmentation(self, text, cleaning=True, cleaning_pos=True, normalization=True):
        text = self.cleaning(text) if cleaning else text
        
        segment = []
        for word, attr in self.annotation(text):
            
            word = self.normalization(word) if normalization else word
            
            if cleaning_pos and self.is_not_my_stopword(word, attr):
                segment.append(self.normalization(word))
                
        return ' '.join(segment)
    
if __name__ == "__main__":
    pretweet = Pretweet()
    
    lines = pd.read_csv('sample-data/tweet.csv', encoding = 'utf-8').text.tolist()
    
    with open('sample-data/processed.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write('{}\n'.format(pretweet.segmentation(line)))
