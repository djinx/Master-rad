from parse import read_files
import random
import numpy as np
from sklearn import metrics
from datetime import datetime

functions_with_freqs = {}


def make_freq_graph():
    proteins = read_files.read_proteins(add="_n_100.txt")
    functions = read_files.read_map_file("functions_with_proteins_n_100.txt")
    ontology = read_files.read_map_file("ontology.txt")

    num_of_proteins = len(proteins)

    for function in ontology:
        if function in functions:
            functions_with_freqs[function] = len(functions[function]) / num_of_proteins


def prediction(function):
    rand = random.uniform(0, 1)

    if rand <= functions_with_freqs[function]:
        return 1.0

    else:
        return 0.0


def all_predictions(true_functions):
    start = datetime.now()
    predicted_functions = []
    functions = read_files.read_molecular_functions(add="_n_100.txt")

    n = len(functions)
    y_true = np.zeros(n)
    y_predicted = np.zeros(n)
    i = 0

    for function in functions:
        predicted = prediction(function)

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

    return predicted_functions, round(f1, 3)


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
    test_proteins_with_functions = read_files.read_map_file("proteins_with_functions_test_org_n_100.txt")
    make_freq_graph()
    print(functions_with_freqs['GO:0003674'])

    i = 0
    nums = [0, 0, 0, 0, 0]
    avgs = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_f1 = 0.0
    for protein in test_proteins_with_functions:
        i += 1
        print(protein, i, "/ 100")
        predicted_functions, f1 = all_predictions(test_proteins_with_functions[protein])

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
