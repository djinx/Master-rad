from sklearn import model_selection
from parse import utility
import numpy as np
# from sklearn.decomposition import PCA
from datetime import datetime


def make_sequence(x):
    sequence = ""

    for i in range(0, len(x)):
        if x[i] > 0:
            sequence += str(i+1) + ":" + str(x[i]) + " "

    return sequence


def smaller_set(positives, negatives, num_of_proteins, n):
    # Ukupan broj pozitivnih i negativnih instanci
    total_num_of_positive = len(positives)
    total_num_of_negative = num_of_proteins - total_num_of_positive

    # Broj pozitivnih i negativnih instanci za uzorak
    num_of_positive = round(len(positives) / num_of_proteins * n)
    num_of_negative = n - num_of_positive

    # Indeksi odabranih instanci
    positive_indices = np.random.choice(total_num_of_positive, num_of_positive, replace=False)
    negative_indices = np.random.choice(total_num_of_negative, num_of_negative, replace=False)

    # Odabir instanci
    chosen_positive = np.array(positives)[positive_indices]
    chosen_negative = np.array(negatives)[negative_indices]

    return chosen_positive, chosen_negative


def train_test_knn_nn(all_sequences, function, size=-1, k=4):
    positive_proteins = read_files.read_map_file("functions_with_proteins_n_100.txt")[function]
    negative_proteins = read_files.read_proteins(positive_proteins, "_n_100.txt")

    if size == -1:
        chosen_positives = positive_proteins
        chosen_negatives = negative_proteins
        n = 1
        size = len(all_sequences)
    else:
        chosen_positives, chosen_negatives = smaller_set(positive_proteins, negative_proteins, len(all_sequences), size)
        num_of_positives = len(chosen_positives)
        n = round((size / 2 - num_of_positives) / num_of_positives)

    x = np.zeros((size, 20**k))
    y = np.zeros(size)
    i = 0

    print("\tn =", n)
    for protein in all_sequences:
        if protein in chosen_positives:
            y[i] = 1
            x[i] = make_array(all_sequences[protein], k)
            i += 1
        if protein in chosen_negatives:
            x[i] = make_array(all_sequences[protein], k)
            i += 1

    print("\tX i Y:", x.shape, y.shape)
    return x, y


def make_array(sequences, k=4):
    array = np.zeros(20**k)
    values = sequences.replace("\n", "").split(" ")

    for value in values:
        if value == '':
            continue
        tokens = value.split(":")
        i = int(tokens[0]) - 1
        num = float(tokens[1])

        array[i] = num

    return array
