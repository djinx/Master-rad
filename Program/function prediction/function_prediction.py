import pickle
import numpy as np
from parse import read_files
from predictors import train_test_data
from sklearn import metrics

models_path = "../data/models/"


def save_model(function, model, directory):
    pickle.dump(model, open(models_path+directory+function, 'wb'))


def read_model(function, directory):
    return pickle.load(open(models_path+directory+function, 'rb'))


def prediction(protein_sequence, function, directory):
    classifier = read_model(function, directory)
    return classifier.predict([protein_sequence])[0]


def all_predictions(protein, directory, true_functions):
    predicted_functions = []
    functions = read_files.read_molecular_functions(add="_n_100.txt")

    n = len(functions)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    y_true = np.zeros(n)
    y_predicted = np.zeros(n)
    i = 0

    for function in functions:
        if function == "GO:0003674":
            predicted_functions.append(function)
            y_true[i] = 1
            y_predicted[i] = 1
            continue

        sequence = train_test_data.make_array(protein, 3)
        predicted = prediction(sequence, function.replace(":", "_"), directory)
        
        if function in true_functions:
            y_true[i] = 1

        if predicted == 1:
            y_predicted[i] = 1
            predicted_functions.append(function)
            if function in true_functions:
                tp += 1
            else:
                fp += 1

        else:
            if function in true_functions:
                fn += 1
            else:
                tn += 1

        i += 1

    acc = metrics.accuracy_score(y_true, y_predicted)
    pre = metrics.precision_score(y_true, y_predicted)
    rec = metrics.recall_score(y_true, y_predicted)
    f1 = metrics.f1_score(y_true, y_predicted)

    # print("\t", acc, pre, rec, f1)

    return predicted_functions, round(f1, 3)


def main():
    test_protein_sequences = read_files.read_array_sequences(add="_test_n_100.txt")
    test_proteins_with_functions = read_files.read_map_file("proteins_with_functions_test_n_100.txt")
    f1_scores = {}
    avg = 0.0
    for protein in test_protein_sequences:
        # print(protein)
        predicted_functions, f1 = all_predictions(test_protein_sequences[protein], "LR_models/", test_proteins_with_functions[protein])

        avg += f1
        if f1 in f1_scores:
            f1_scores[f1].append(protein)
        else:
            f1_scores[f1] = [protein]

    for f1 in f1_scores:
        print(f1, ":", len(f1_scores[f1]))

    print("Prosek:", avg/100)


if __name__ == '__main__':
    main()
