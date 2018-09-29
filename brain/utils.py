from keras.models import Model
from keras.preprocessing import sequence
from keras import backend as K
import numpy as np
import re
from pprint import pprint

def textgenrnn_sample(preds, top_n=3, temperature=1):
    '''
    Samples predicted probabilities of the next word.
    '''

    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + K.epsilon()) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)

    index = (-preds).argsort()[:top_n]

    # avoid leaks by closing the session after making predictions
    # https://stackoverflow.com/a/50377181
    K.clear_session()
    
    return index

 
def textgenrnn_generate(model, vocab, indices_char, maxlen, 
                        meta_token, max_gen_length, top_n, story):
    '''
    Generates and returns a single text.
    '''

    if story:
        story = story.split()
    else:
        story = [meta_token, meta_token]

    if model_input_count(model) > 1:
        model = Model(inputs=model.input[0], outputs=model.output[1])

    while len(story) < max_gen_length:
        encoded_text = textgenrnn_encode_sequence(
            story[-maxlen:],
            vocab,
            maxlen
        )

        # get indexes of top n options
        options_index = textgenrnn_sample(
            model.predict(encoded_text, batch_size=1)[0],
            top_n=top_n,
        )

        # get top n options from vocab using indexes
        options = [indices_char[idx] for idx in options_index]

        return options


def textgenrnn_encode_sequence(text, vocab, maxlen):
    '''
    Encodes a text into the corresponding encoding for prediction with
    the model.
    '''

    encoded = np.array([vocab.get(x, 0) for x in text])
    return sequence.pad_sequences([encoded], maxlen=maxlen)


def model_input_count(model):
    if isinstance(model.input, list):
        return len(model.input)
    else:   # is a Tensor
        return model.input.shape[0]
