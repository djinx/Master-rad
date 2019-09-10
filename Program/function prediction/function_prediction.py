import pickle
import numpy as np
from parse import read_files
from predictors import train_test_data
from sklearn import metrics
from datetime import datetime

models_path = "../data/models/"
models = {}


def save_model(function, model, directory):
    pickle.dump(model, open(models_path+directory+function, 'wb'))


def read_model(function, directory):
    return pickle.load(open(models_path+directory+function, 'rb'))


# def read_pca_models():
#     start = datetime.now()
#     directory = "PCA_models/"
#     functions = read_files.read_molecular_functions(add="_n_100.txt")
#
#     for function in functions:
#         if function != "GO:0003674":
#             pca_models[function] = read_model(function.replace(":", "_"), directory)
#
#     end = datetime.now()
#     print("Citanje PCA modela:", end - start)


def read_models(directory):
    start = datetime.now()
    functions = read_files.read_molecular_functions(add="_n_100.txt")

    for function in functions:
        if function != "GO:0003674":
            models[function] = read_model(function.replace(":", "_"), directory)

    end = datetime.now()
    print("Citanje modela:", end - start)


def prediction(protein_sequence, function):
    classifier = models[function]
    return classifier.predict(protein_sequence)[0]


def all_predictions(protein, true_functions, pca):
    start = datetime.now()
    predicted_functions = []
    functions = read_files.read_molecular_functions(add="_n_100.txt")

    n = len(functions)
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

        if pca:
            pca_model = read_model(function.replace(":", "_"), "PCA_models/")
            sequences = pca_model.transform([sequence])
            predicted = prediction(sequences, function)
        else:
            predicted = prediction([sequence], function)

        if function in true_functions:
            y_true[i] = 1

        if predicted == 1:
            y_predicted[i] = 1
            predicted_functions.append(function)

        i += 1

    f1 = metrics.f1_score(y_true, y_predicted)

    print("\t", f1)
    end = datetime.now()
    print("\t", end - start)

    return predicted_functions, f1


def organism_num(organism):
    if organism == 'human':
        return 0
    elif organism == 'mouse':
        return 1
    elif organism == 'rat':
        return 2
    elif organism == 'ecoli':
        return 3
    elif organism == 'arath':
        return 4
    else:
        return 5


def main():
    proteins_with_organisms = read_files.read_map_file("proteins_with_organisms.txt")
    test_protein_sequences = read_files.read_array_sequences(add="_test_org_n_100.txt")
    test_proteins_with_functions = read_files.read_map_file("proteins_with_functions_test_org_n_100.txt")
    read_models("SVM_models/")
    pca = True
    i = 0
    nums = [0, 0, 0, 0, 0]
    avgs = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_f1 = 0.0

    for protein in test_protein_sequences:
        i += 1
        print(protein, i, "/ 100")
        predicted_functions, f1 = all_predictions(test_protein_sequences[protein], test_proteins_with_functions[protein], pca)

        if protein in proteins_with_organisms:
            p = organism_num(proteins_with_organisms[protein][0])
            avgs[p] += f1
            nums[p] += 1

        avg_f1 += f1

    avg_f1s = [0.0 for i in range(0, len(avgs))]
    for i in range(0, len(avgs)):
        if nums[i] != 0:
            avg_f1s[i] = avgs[i] / nums[i]

    print("Proseci:", avg_f1s)
    print("Ukupna f1:", avg_f1 / 100)


if __name__ == '__main__':
    main()
