from sklearn import model_selection
from parse import read_files
import numpy as np


def train_test(all_sequences, function, size=20000):
    positive_proteins = read_files.read_functions_with_proteins()[function]
    negative_proteins = read_files.read_proteins(positive_proteins)

    chosen_positives, chosen_negatives = smaller_set(positive_proteins, negative_proteins, len(all_sequences), size)
    num_of_positives = len(chosen_positives)
    n = (size / 2 - num_of_positives) / num_of_positives

    x = []
    y = []

    for protein in all_sequences:
        i = 0
        if protein in positive_proteins:
            while i < n:
                y.append(1)
                x.append(protein)
                i += 1
        else:
            y.append(-1)
            x.append(protein)

    x_train_val, x_test, y_train_val, y_test = model_selection.train_test_split(x, y, test_size=0.25)
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x_train_val, y_train_val,
                                                                                    test_size=0.25)

    make_file(x_train, y_train, all_sequences, "../data/svm/train.txt")
    make_file(x_validation, y_validation, all_sequences, "../data/svm/validation.txt")
    make_file(x_test, y_test, all_sequences, "../data/svm/test.txt")


def make_file(x, y, all_sequences, path):
    file = open(path, "w")

    for i in range(0, len(x)):
        protein = x[i]
        file.write(str(y[i]) + " " + all_sequences[protein] + "\n")

    file.close()


def smaller_set(positives, negatives, num_of_proteins, n):
    # Ukupan broj pozitivnih i negativnih instanci
    total_num_of_positive = len(positives)
    total_num_of_negative = num_of_proteins - total_num_of_positive

    # Broj pozitivnih i negativnih instanci za uzorak
    num_of_positive = round(len(positives) / num_of_proteins * n)
    num_of_negative = n // 2

    # Indeksi odabranih instanci
    positive_indices = np.random.choice(total_num_of_positive, num_of_positive, replace=False)
    negative_indices = np.random.choice(total_num_of_negative, num_of_negative, replace=False)

    # Odabir instanci
    chosen_positive = np.array(positives)[positive_indices]
    chosen_negative = np.array(negatives)[negative_indices]

    return chosen_positive, chosen_negative
