import numpy as np
import sys
sys.path.append(".")
import weights_quantization as wqtz
from math import ceil
import time

''
def quant_compress(name, data, nbit):
    weights_vec = data.flatten().astype(np.float32)
    vec_length = weights_vec.size
    nelem = int(32 / nbit)
    newlabel = np.empty(int((vec_length + nelem - 1) / nelem), dtype=np.int32)
    codebook = np.empty((2 ** nbit), dtype=np.float32)
    wqtz.compress_layer_weights(newlabel, codebook, weights_vec, vec_length, nbit)
    with open(name, "wb") as f:
        codebook.tofile(f)
        newlabel.tofile(f)
    return newlabel, codebook

def quant_decompress(name, nbit, row, col):
    codebook_size = 2**nbit
    vec_length = row*col
    labels = None
    codebook = None
    with open(name, 'rb') as f:
        #labels
        bytes = f.read(codebook_size*4)
        codebook = np.frombuffer(bytes, dtype=np.float32).copy()
        codebook.reshape([-1])

        # codebook weights
        f.seek(codebook_size*4)
        bytes = f.read(vec_length)
        labels = np.frombuffer(bytes, dtype=np.uint8).copy()
    data_vec = np.empty(vec_length, dtype=np.float32)
    wqtz.decompress_layer_weights(data_vec, labels, codebook, vec_length, nbit)
    data = data_vec.reshape([row, col])
    return data
