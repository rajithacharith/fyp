import os
import re
import tempfile
import sys
import time
import argparse
import numpy as np
from collections import namedtuple

assert os.environ.get('LASER'), 'Please set the enviornment variable LASER'
LASER = os.environ['LASER']

sys.path.append(LASER + '/source/')
from lib.text_processing import Token, BPEfastApply
from embed import SentenceEncoder, EncodeFile

def createEmbeddings(txt_in_path, txt_out_path, lang):
    files = os.listdir(txt_in_path + "/")
    filepaths = []
    o_filepaths = []
    for filename in files:
        filepaths.append(txt_in_path + filename)
        o_filepaths.append(txt_out_path + filename.replace("txt", "raw"))
    print(filepaths)
    print(o_filepaths)
    encodeMultiple(LASER + "/models/bilstm.93langs.2018-12-26.pt", "en", LASER + "/models/93langs.fcodes", filepaths, o_filepaths)

def encodeMultiple(encoder, token_lang, bpe_codes, inputpaths, outputpaths):
    stable = True
    cpu = False
    buffer_size = 10000
    max_tokens = 12000
    max_sentences = "None"
    verbose = True

    if verbose:
        print(' - Encoder: loading {}'.format(encoder))
    encoder = SentenceEncoder(encoder,
                              max_sentences=max_sentences,
                              max_tokens=max_tokens,
                              sort_kind='mergesort' if stable else 'quicksort',
                              cpu=cpu)

    for i in range(len(inputpaths)):
        with tempfile.TemporaryDirectory() as tmpdir:
            ifname = ''  # stdin will be used
            if token_lang != '--':
                tok_fname = os.path.join(tmpdir, 'tok')
                Token(inputpaths[i],
                    tok_fname,
                    lang=token_lang,
                    romanize=True if token_lang == 'el' else False,
                    lower_case=True, gzip=False,
                    verbose=verbose, over_write=False)
                inputpaths[i] = tok_fname

            if bpe_codes:
                bpe_fname = os.path.join(tmpdir, 'bpe')
                BPEfastApply(inputpaths[i],
                            bpe_fname,
                            bpe_codes,
                            verbose=verbose, over_write=False)
                inputpaths[i] = bpe_fname

            EncodeFile(encoder,
                    inputpaths[i],
                    outputpaths[i],
                    verbose=verbose, over_write=False,
                    buffer_size=buffer_size)