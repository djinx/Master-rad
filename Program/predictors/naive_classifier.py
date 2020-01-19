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
    acc = metrics.accuracy_score(y_true, y_predicted)
    pre = metrics.precision_score(y_true, y_predicted)
    rec = metrics.recall_score(y_true, y_predicted)
    auc = metrics.roc_auc_score(y_true, y_predicted)

    print("\t", f1)
    end = datetime.now()
    print("\t", end - start)

    return predicted_functions, f1, acc, pre, rec, auc


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
    proteins_with_organisms = read_files.read_map_file("test_proteins_with_organisms.txt")
    test_proteins_with_functions = read_files.read_map_file("test_proteins_with_functions.txt")
    make_freq_graph()
    print(functions_with_freqs['GO:0003674'])
    i = 0
    num_of_proteins = len(test_proteins_with_functions)
    nums = [0, 0, 0, 0, 0]
    avgs_f1 = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_f1 = 0.0
    avgs_acc = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_acc = 0.0
    avgs_pre = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_pre = 0.0
    avgs_rec = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_rec = 0.0
    avgs_auc = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_auc = 0.0
    for protein in test_proteins_with_functions:
        i += 1
        print(protein, i, "/", num_of_proteins)
        predicted_functions, f1, acc, pre, rec, auc = all_predictions(test_proteins_with_functions[protein])

        if protein in proteins_with_organisms:
            p = organism_num(proteins_with_organisms[protein][0])

            if p != 5:
                avgs_f1[p] += f1
                avgs_acc[p] += acc
                avgs_pre[p] += pre
                avgs_rec[p] += rec
                avgs_auc[p] += auc
                nums[p] += 1

        avg_f1 += f1
        avg_acc += acc
        avg_pre += pre
        avg_rec += rec
        avg_auc += auc

    avg_f1s = [0.0 for i in range(0, len(avgs_f1))]
    avg_accs = [0.0 for i in range(0, len(avgs_acc))]
    avg_pres = [0.0 for i in range(0, len(avgs_pre))]
    avg_recs = [0.0 for i in range(0, len(avgs_rec))]
    avg_aucs = [0.0 for i in range(0, len(avgs_auc))]
    for i in range(0, len(avgs_f1)):
        if nums[i] != 0:
            avg_f1s[i] = avgs_f1[i] / nums[i]
            avg_accs[i] = avgs_acc[i] / nums[i]
            avg_pres[i] = avgs_pre[i] / nums[i]
            avg_recs[i] = avgs_rec[i] / nums[i]
            avg_aucs[i] = avgs_auc[i] / nums[i]

    avg_f1s.append(avg_f1 / num_of_proteins)
    avg_accs.append(avg_acc / num_of_proteins)
    avg_pres.append(avg_pre / num_of_proteins)
    avg_recs.append(avg_rec / num_of_proteins)
    avg_aucs.append(avg_auc / num_of_proteins)
    print("F1:", avg_f1s)
    print("Acc:", avg_accs)
    print("Pre:", avg_pres)
    print("Rec:", avg_recs)
    print("AUC:", avg_aucs)


if __name__ == '__main__':
    main()
