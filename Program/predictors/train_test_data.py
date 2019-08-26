from sklearn import model_selection
from parse import read_files
import numpy as np
# from sklearn.decomposition import PCA
from datetime import datetime


def train_test_svm_light(all_sequences, function, n=1, size=-1, k=4):
    positive_proteins = read_files.read_map_file("functions_with_proteins_n_10.txt")[function]
    negative_proteins = read_files.read_proteins(positive_proteins, add="_n_100.txt")

    if size == -1:
        chosen_positives = positive_proteins
        chosen_negatives = negative_proteins
        size = len(all_sequences)
    else:
        chosen_positives, chosen_negatives = smaller_set(positive_proteins, negative_proteins, len(all_sequences), size)
        num_of_positives = len(chosen_positives)
        n = round((size / 2 - num_of_positives) / num_of_positives)

    print("n =", n)
    x = np.zeros((size, 20 ** k))
    y = np.ones(size)
    i = 0

    print("\tPriprema x i y pocetak: ", datetime.now().time())
    for protein in all_sequences:
        if protein in chosen_positives:
            x[i] = make_array(all_sequences[protein], k)
            i += 1
        if protein in chosen_negatives:
            y[i] = -1
            x[i] = make_array(all_sequences[protein], k)
            i += 1
    print("\tPriprema x i y kraj: ", datetime.now().time())

    print("\tTrain val test pocetak: ", datetime.now().time())
    x_train_val, x_test, y_train_val, y_test = model_selection.train_test_split(x, y, test_size=0.25)

    # print("\tPCA pocetak: ", datetime.now().time())
    # num_components = 1000
    # pca = PCA(n_components=num_components)
    # pca.fit(x_train_val)
    # x_train_val_pca = pca.transform(x_train_val)
    # x_test_pca = pca.transform(x_test)
    # print("\tPCA kraj: ", datetime.now().time())

    print("\tTrain val pocetak: ", datetime.now().time())
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x_train_val, y_train_val,
                                                                                    test_size=0.25)

    make_file(x_train, y_train, "../data/svm/train.txt", True, n)
    make_file(x_validation, y_validation, "../data/svm/validation.txt")
    make_file(x_test, y_test, "../data/svm/test.txt")


def make_file(x, y, path, train=False, n=1):
    print("\tFile " + path + " pocetak: ", datetime.now().time())
    file = open(path, "w")

    for i in range(0, len(x)):
        sequence = make_sequence(x[i])
        k = 0

        if train and y[i] == 1:
            while k < n:
                file.write(str(y[i]) + " " + sequence + "\n")
                k += 1

        else:
            file.write(str(y[i]) + " " + sequence + "\n")

    file.close()
    print("\tFile " + path + " kraj: ", datetime.now().time())


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
