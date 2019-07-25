from sklearn import model_selection
from parse import read_files


def train_test(all_sequences, function):
    positive_proteins = read_files.read_functions_with_proteins()[function]

    # povecanje broja pozitivnih instanci
    # dodaju se iste instance vise puta
    total = len(all_sequences)
    positive = len(positive_proteins)
    n = (total - 2*positive) / positive

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
