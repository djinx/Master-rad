from parse import read_files
from predictors.train_test_data import train_test_svm_light
from datetime import datetime
import subprocess
import numpy as np


def main():
    # putanje
    svm_learn = "../svm_light/svm_learn "
    svm_classify = "../svm_light/svm_classify "
    train = " ../data/svm/train.txt "
    validation = " ../data/svm/validation.txt "
    test = " ../data/svm/test.txt "

    # nekoliko proteina za testiranje klasifikatora
    all_sequences = read_files.read_array_sequences(add="_n_100.txt")
    print(len(all_sequences))

    # funckija za koju se pravi klasifikator
    function = "GO:0060589"

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    train_test_svm_light(all_sequences, function, k=3)

    cs = [10**i for i in range(-2, 2)]
    gammas = np.logspace(-3, 1, 5)

    for gamma in gammas:
        print("Pocelo trenuranje za gamma: ", gamma, datetime.now().time())
        for c in cs:
            print("\t", c, datetime.now().time())
            model = " ../data/models/reduced_rbf/" + function[3:] + "_g" + str(gamma) + "_c" + str(c)
            output = " ../data/output/reduced_rbf/" + function[3:] + "_g" + str(gamma) + "_c" + str(c)
            model_terminal = "../data/terminal/reduced_rbf/train_" + function[3:] + "_g" + str(gamma) + "_c" + str(c) + ".txt"
            output_terminal = "../data/terminal/reduced_rbf/val_ " + function[3:] + "_g" + str(gamma) + "_c" + str(c) + ".txt"

            parameters = "-c " + str(c) + " -t 2 -g " + str(gamma)

            with open(model_terminal, "w") as file:
                file.write("Pocelo trenuranje za c: " + str(c) + " " + str(datetime.now().time()) + "\n")
                subprocess.run(svm_learn + parameters + train + model, stdout=file)
                file.write("Zavrseno treniranje: " + str(datetime.now().time()) + "\n")

            with open(output_terminal, "w") as file:
                file.write("Pocelo testiranje: " + str(datetime.now().time()) + "\n")
                subprocess.run(svm_classify + validation + model + output, stdout=file)
                file.write("Zavrseno testiranje: " + str(datetime.now().time()) + "\n")


if __name__ == '__main__':
    main()
