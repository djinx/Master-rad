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
    test_protein_sequences = read_files.read_array_sequences(add="_test.txt")
    test_proteins_with_functions = read_files.read_map_file("test_proteins_with_functions.txt")
    read_models("LR_models/")
    pca = False
    i = 0
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

    num_of_test_proteins = len(test_protein_sequences)

    for protein in test_protein_sequences:
        i += 1
        print(protein, i, "/", num_of_test_proteins)
        predicted_functions, f1, acc, pre, rec, auc = all_predictions(test_protein_sequences[protein], test_proteins_with_functions[protein], pca)

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

    avg_f1s.append(avg_f1 / num_of_test_proteins)
    avg_accs.append(avg_acc / num_of_test_proteins)
    avg_pres.append(avg_pre / num_of_test_proteins)
    avg_recs.append(avg_rec / num_of_test_proteins)
    avg_aucs.append(avg_auc / num_of_test_proteins)
    print("F1:", avg_f1s)
    print("Acc:", avg_accs)
    print("Pre:", avg_pres)
    print("Rec:", avg_recs)
    print("AUC:", avg_aucs)

    file = open("../test_scoresss_lr.txt", "w")
    file.write("F1:" + " ".join(str(a) for a in avg_f1s) + "\n")
    file.write("Acc:" + " ".join(str(a) for a in avg_accs) + "\n")
    file.write("Pre:" + " ".join(str(a) for a in avg_pres) + "\n")
    file.write("Rec:" + " ".join(str(a) for a in avg_recs) + "\n")
    file.write("AUC:" + " ".join(str(a) for a in avg_aucs) + "\n")

    file.close()

    print(datetime.now())


if __name__ == '__main__':
    main()
