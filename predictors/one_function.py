from sklearn import model_selection, metrics, svm
from datetime import datetime


def one_function_predictor(array_sequences, proteins):
    # Funkcija odredjuje klasifikator za jednu funkciju
    # array_sequences je niz proteina i njihovih nizovnih sekvenci
    # proteins je niz proteina koji vrse zadatu funkciju

    x = []
    y = []

    for protein in array_sequences:
        x.append(array_sequences[protein])
        if protein in proteins:
            y.append(1)
        else:
            y.append(-1)

    x_train_val, x_test, y_train_val, y_test = model_selection.train_test_split(x, y, test_size=0.25)
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x_train_val, y_train_val,
                                                                                    test_size=0.25)

    print("Odabir modela: ", datetime.now().time())
    best_c = select_best_c(x_train, x_validation, y_train, y_validation)

    print("Treniranje odabranog modela: ", datetime.now().time())
    classificator = svm.SVC(gamma="scale", C=best_c)
    classificator.fit(x_train_val, y_train_val)

    print("Testiranje odabranog modela: ", datetime.now().time())
    y_predicted = classificator.predict(x_test)

    print("Ocena odabranog modela: ", datetime.now().time())
    accuracy = metrics.accuracy_score(y_test, y_predicted)
    precision = metrics.precision_score(y_test, y_predicted)
    f1 = metrics.f1_score(y_test, y_predicted)

    print("accuracy: ", accuracy)
    print("precision: ", precision)
    print("f1: ", f1)

    return classificator


def select_best_c(x_train, x_test, y_train, y_test):
    results = {}
    cs = [10**x for x in range(0, 3)]

    for c in cs:
        print("\nTreniranja modela za C =", c, " ", datetime.now().time())
        classificator = svm.SVC(gamma="scale", C=c)
        classificator.fit(x_train, y_train)

        print("Testiranje modela za C =", c, datetime.now().time())
        y_predicted = classificator.predict(x_test)

        print("Ocena modela za C =", c, datetime.now().time())
        accuracy = metrics.accuracy_score(y_test, y_predicted)
        precision = metrics.precision_score(y_test, y_predicted)
        f1 = metrics.f1_score(y_test, y_predicted)
        results[c] = {
            "acc": accuracy,
            "pre": precision,
            "f1": f1
        }

    return find_best_c(results)


def find_best_c(results, eps=10**-3):
    best_c_acc = 1
    best_c_pre = 1
    best_c_f1 = 1
    best_accuracy = 0
    best_precision = 0
    best_f1 = 0
    for c in results:
        accuracy = results[c]["acc"]
        precision = results[c]["pre"]
        f1 = results[c]["f1"]

        if accuracy > best_accuracy and abs(accuracy - best_accuracy) > eps:
            best_c_acc = c

        if precision > best_precision and abs(precision - best_precision) > eps:
            best_c_pre = c

        if f1 > best_f1 and abs(f1 - best_f1) > eps:
            best_c_f1 = c

    if best_c_acc == best_c_f1 or best_c_acc == best_c_pre:
        return best_c_acc

    elif best_c_f1 == best_c_pre:
        return best_c_pre

    else:
        return best_f1

