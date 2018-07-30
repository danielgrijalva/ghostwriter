from keras.preprocessing.text import Tokenizer
import numpy as np
import json
from pkg_resources import resource_filename
from brain.utils import *
from brain.model import textgenrnn_model
import re


class textgenrnn:
    META_TOKEN = '<s>'
    config = {}

    def __init__(self, weights_path=None,
                 vocab_path=None,
                 config_path=None):

        if weights_path is None:
            weights_path = resource_filename(__name__,
                                             'data/weights.hdf5')

        if vocab_path is None:
            vocab_path = resource_filename(__name__,
                                           'data/vocab.json')

        if config_path is None:
            config_path = resource_filename(__name__,
                                           'data/config.json')

        with open(vocab_path, 'r',
                  encoding='utf8', errors='ignore') as json_file:
            self.vocab = json.load(json_file)

        with open(config_path, 'r',
                    encoding='utf8', errors='ignore') as json_file:
            self.config = json.load(json_file)

        self.indices_char = dict((self.vocab[c], c) for c in self.vocab)
        self.tokenizer = Tokenizer(filters='', char_level=False)
        self.tokenizer.word_index = self.vocab
        self.num_classes = len(self.vocab) + 1
        self.model = textgenrnn_model(self.num_classes,
                                      cfg=self.config,
                                      weights_path=weights_path)


    def generate(self, temperature, max_gen_length, top_n):
        gen_text = textgenrnn_generate(self.model,
                                        self.vocab,
                                        self.indices_char,
                                        temperature,
                                        self.config['max_length'],
                                        self.META_TOKEN,
                                        max_gen_length,
                                        top_n)

        return gen_text
