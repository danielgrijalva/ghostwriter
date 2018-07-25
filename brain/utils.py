from keras.models import Model
from keras.preprocessing import sequence
from keras import backend as K
import numpy as np
import re


def textgenrnn_sample(preds, temperature, interactive=False, top_n=3):
    '''
    Samples predicted probabilities of the next character to allow
    for the network to show "creativity."
    '''

    preds = np.asarray(preds).astype('float64')

    if temperature is None or temperature == 0.0:
        return np.argmax(preds)

    preds = np.log(preds + K.epsilon()) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    
    if not interactive:
        index = np.argmax(probas)

        # prevent function from being able to choose 0 (placeholder)
        # choose 2nd best index from preds
        if index == 0:
            index = np.argsort(preds)[-2]        
    else:
        # return list of top N chars/words
        # descending order, based on probability
        index = (-preds).argsort()[:top_n]

    return index


def textgenrnn_generate(model, vocab,
                        indices_char, prefix=None, temperature=0.5,
                        maxlen=40, meta_token='<s>',
                        word_level=False,
                        single_text=False,
                        max_gen_length=300,
                        interactive=False,
                        top_n=3):
    '''
    Generates and returns a single text.
    '''

    collapse_char = ' ' if word_level else ''

    if single_text:
        text = list(prefix) if prefix else ['']
        max_gen_length += maxlen
    else:
        text = [meta_token] + list(prefix) if prefix else [meta_token]
    next_char = ''

    if not isinstance(temperature, list):
        temperature = [temperature]

    if model_input_count(model) > 1:
        model = Model(inputs=model.input[0], outputs=model.output[1])

    while next_char != meta_token and len(text) < max_gen_length:
        encoded_text = textgenrnn_encode_sequence(text[-maxlen:],
                                                vocab, maxlen)
        next_temperature = temperature[(len(text) - 1) % len(temperature)]

        if not interactive:
            # auto-generate text without user intervention
            next_index = textgenrnn_sample(
                model.predict(encoded_text, batch_size=1)[0],
                next_temperature)
            next_char = indices_char[next_index]
            text += [next_char]                    
        else:
            # ask user what the next char/word should be
            options_index = textgenrnn_sample(
                model.predict(encoded_text, batch_size=1)[0],
                next_temperature,
                interactive=interactive,
                top_n=top_n
            )
            options = [indices_char[idx] for idx in options_index]
            print('Controls:\n\ts: stop.\tx: backspace.\to: write your own.')
            print('\nOptions:')

            for i, option in enumerate(options, 1):
                print('\t{}: {}'.format(i, option))

            print('\nProgress: {}'.format(collapse_char.join(text)[3:]))
            print('\nYour choice?')
            user_input = input('> ')

            try:
                user_input = int(user_input)
                next_char = options[user_input-1]
                text += [next_char]
            except ValueError:
                if user_input == 's':
                    next_char = '<s>'
                    text += [next_char]
                elif user_input == 'o':
                    other = input('> ')
                    text += [other]                    
                elif user_input == 'x':
                    try:
                        del text[-1]
                    except IndexError:
                        pass
                else:
                    print('That\'s not an option!')

    # if single text, ignore sequences generated w/ padding
    # if not single text, strip the <s> meta_tokens
    if single_text:
        text = text[maxlen:]
    else:
        text = text[1:-1]

    text_joined = collapse_char.join(text)

    # If word level, remove spaces around punctuation for cleanliness.
    if word_level:
        punct = '\\n\\t'
        text_joined = re.sub(" ([{}]) ".format(punct), r'\1', text_joined)

    return text_joined


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
