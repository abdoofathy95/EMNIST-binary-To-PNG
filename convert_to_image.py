#!/usr/bin/env python
# CONVERTS EMNIST BINARY TO PNG IMAGES
import os
import struct
import sys

from array import array
from os import path

import png

def read(dataset = "training", path = "."):
    if dataset is "training":
        fname_img = os.path.join(path, 'emnist-balanced-train-images-idx3-ubyte/data')
        fname_lbl = os.path.join(path, 'emnist-balanced-train-labels-idx1-ubyte/data')
    elif dataset is "testing":
        fname_img = os.path.join(path, 'emnist-balanced-test-images-idx3-ubyte/data')
        fname_lbl = os.path.join(path, 'emnist-balanced-test-labels-idx1-ubyte/data')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = array("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = array("B", fimg.read())
    fimg.close()

    return lbl, img, size, rows, cols

def write_dataset(labels, data, size, rows, cols, output_dir):
    # create output directories
    output_dirs = [
        path.join(output_dir, str(i))
        for i in range(47)
    ]
    for dir in output_dirs:
        if not path.exists(dir):
            os.makedirs(dir)

    print(rows, cols)
    # write data
    for (i, label) in enumerate(labels):
        output_filename = path.join(output_dirs[label], str(i) + ".png")
        print("writing " + output_filename)
        base = i*rows*cols;
        with open(output_filename, "wb") as h:
            w = png.Writer(cols, rows, greyscale=True)
            data_i = [
                data[ (base + j*cols) : (base + (j+1)*cols) ]
                for j in range(cols)
            ]
            data_i = list(map(list, zip(*data_i)))
            w.write(h, data_i)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: {0} <input_path> <output_path>".format(sys.argv[0]))
        sys.exit()

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    for dataset in ["training", "testing"]:
        labels, data, size, rows, cols = read(dataset, input_path)
        write_dataset(labels, data, size, rows, cols,
                      path.join(output_path, dataset))
