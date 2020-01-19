import pickle
import numpy as np
from sklearn import model_selection

file_path = "data/parsed_data/"
score_path = "data/"
models_path = "data/models/"


def read_model(function, directory):
    return pickle.load(open(models_path + directory + function.replace(":", "_"), 'rb'))


def save_model(function, model, directory):
    pickle.dump(model, open(models_path + directory + function.replace(":", "_"), 'wb'))


def save_function_score(function, acc, pre, rec, f1, auc, num, num_precent, file_name):
    file = open(score_path + file_name, "a")
    file.write(function + "->" + str(f1) + " " + str(acc) + " " + str(pre) + " " + str(rec) + " ")
    file.write(str(auc) + " " + str(num) + " " + str(num_precent) + "\n")
    file.close()


def pos_neg_data(all_sequences, function, f_path="functions_with_proteins_n_100.txt", p_path="molecular_proteins_n_100.txt", k=3):
    #     print("Pocetak pripreme pozitivnih i negativnih instanci: ", datetime.now().time())
    positive_proteins = read_map_file(f_path)[function]
    negative_proteins = read_proteins(p_path, positive_proteins)
    size = len(all_sequences)

    x = np.zeros((size, 20 ** k))
    y = np.zeros(size, dtype=int)
    i = 0

    for protein in all_sequences:
        if protein in positive_proteins:
            x[i] = make_array(all_sequences[protein], k)
            y[i] = 1
        if protein in negative_proteins:
            x[i] = make_array(all_sequences[protein], k)
            y[i] = -1

        i += 1

    return x, y, len(positive_proteins)


def make_array(sequence, k=3):
    array = np.zeros(20 ** k)
    values = sequence.replace("\n", "").split(" ")

    for value in values:
        if value == '':
            continue
        tokens = value.split(":")
        i = int(tokens[0]) - 1
        num = float(tokens[1])

        array[i] = num

    return array


def train_val_test(x, y, function):
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.25, random_state=7)
    pca = read_model(function, "PCA_models/")
    x_train = pca.transform(x_train)
    x_test = pca.transform(x_test)
    return x_train, y_train, x_test, y_test


def read_functions(file):
    file = open(file_path + file, "r")
    lines = file.readlines()
    functions = []

    for line in lines:
        functions.append(line.replace("\n", ""))

    return functions


def read_map_file(file):
    # Cita datoteke zapisane u obliku kljuc -> vrednosti
    file = open(file_path + file, "r")
    lines = file.readlines()
    data = {}

    for line in lines:
        tokens = line.replace("\n", "").split("->")
        key = tokens[0]
        values = tokens[1].split(" ")

        data[key] = []

        for value in values:
            if value != "":
                data[key].append(value)

    return data


def read_proteins(file, positive_proteins=None):
    # Citanje spiska proteina koji ce se koristiti prilikom treniranja i testiranja
    file = open(file_path + file, "r")
    lines = file.readlines()
    proteins = []

    if positive_proteins is None:
        for line in lines:
            proteins.append(line.replace("\n", ""))

    else:
        for line in lines:
            protein = line.replace("\n", "")
            if protein not in positive_proteins:
                proteins.append(protein)

    file.close()
    return proteins


def read_array_sequences(file):
    # Citanje proteina sa sekvencama u formatu za datoteke
    file = open(file_path + file, "r")
    lines = file.readlines()
    array_sequences = {}

    for line in lines:
        tokens = line.split(" ")
        array_sequences[tokens[0]] = " ".join(tokens[1:-1])

    file.close()
    return array_sequences


