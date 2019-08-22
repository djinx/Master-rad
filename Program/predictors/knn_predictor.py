from parse import read_files
from predictors import train_test_data
from datetime import datetime
from sklearn import model_selection
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import numpy as np


def main():

    # nekoliko proteina za testiranje klasifikatora
    all_sequences = read_files.read_array_sequences(add="_n_10.txt")
    print(len(all_sequences))

    function = "GO:0060589"
    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    x, y = train_test_data.train_test_knn_nn(all_sequences, function, k=3)

    x_train_val, x_test, y_train_val, y_test = model_selection.train_test_split(x, y, test_size=0.25)

    num_components = 1000
    pca = PCA(n_components=num_components)
    pca.fit(x_train_val)
    x_train_val_prepared_pca = pca.transform(x_train_val)
    x_test_prepared_pca = pca.transform(x_test)

    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x_train_val_prepared_pca,
                                                                                    y_train_val, test_size=0.25)

    print("Explained variance: {}".format(np.sum(pca.explained_variance_ratio_)))

    print(x_train_val_prepared_pca.shape, x_test_prepared_pca.shape)

    ks = [5*i for i in range(1, 5)]
    classifiers = []

    for k in ks:
        print("Treniranje za k=", k, datetime.now().time())
        classifier = KNeighborsClassifier(n_neighbors=k)
        classifier.fit(x_train, y_train)

        print("Predvidjanje: ", datetime.now().time())
        y_predicted = classifier.predict(x_validation)

        print("Metrike:", datetime.now().time())
        print(metrics.confusion_matrix(y_validation, y_predicted))
        print(metrics.classification_report(y_validation, y_predicted))
        acc = metrics.accuracy_score(y_validation, y_predicted)
        pre = metrics.precision_score(y_validation, y_predicted)
        rec = metrics.recall_score(y_validation, y_predicted)
        f1 = metrics.f1_score(y_validation, y_predicted)
        classifiers.append([classifier, acc, pre, rec, f1, k])

    best_classifier = None
    best_f1 = 0
    best_k = 0

    for classifier in classifiers:
        if classifier[4] > best_f1:
            best_f1 = classifier[4]
            best_classifier = classifier[0]
            best_k = classifier[5]

    print("Predvidjanje sa k=", best_k, datetime.now().time())
    y_predicted = best_classifier.predict(x_validation)

    print("Metrike:", datetime.now().time())
    print(metrics.confusion_matrix(y_validation, y_predicted))
    print(metrics.classification_report(y_validation, y_predicted))


if __name__ == '__main__':
    main()
