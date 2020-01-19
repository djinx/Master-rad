from parse import utility
from datetime import datetime
from sklearn import metrics as met

models = "../data/models/"


def main():
    all_sequences = utility.read_array_sequences("array_sequences_n_100.txt")
    functions = utility.read_functions("ordered_molecular_functions.txt")
    smote_functions = utility.read_functions("rf_smote")
    print(len(all_sequences), len(functions), len(smote_functions))

    i = 0
    j = 0
    k = 400
    for function in functions:
        i += 1

        if i < j:
            continue

        if i >= k:
            break

        if function == "GO:0003674":
            utility.save_function_score(function, 1.0, 1.0, 1.0, 1.0, 1.0, 20860, 100, "RF_scores.txt")
            continue

        start_time = datetime.now()
        best_clf = utility.read_model(function, "RF_models/")
        print("Funkcija:", function, i, "/", len(functions), start_time.time())
        x, y, num = utility.pos_neg_data(all_sequences, function)
        x_train, y_train, x_test, y_test = utility.train_val_test(x, y, function)

        y_predicted = best_clf.predict(x_test)
        f1 = met.f1_score(y_test, y_predicted)
        acc = met.accuracy_score(y_test, y_predicted)
        pre = met.precision_score(y_test, y_predicted)
        rec = met.recall_score(y_test, y_predicted)
        auc = met.roc_auc_score(y_test, y_predicted)

        if function in smote_functions:
            total = 20860 - num
            num = 0.5*(total * 0.75 * 0.75 - num)
            total += num

        num_precent = round((100 * num / len(all_sequences)), 1)

        print("\tPisanje...", datetime.now())
        utility.save_function_score(function, acc, pre, rec, f1, auc, num, num_precent, "RF_scores.txt")


if __name__ == '__main__':
    main()
