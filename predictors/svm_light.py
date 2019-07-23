from parse import read_files
from predictors.train_test_data import train_test
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
    all_sequences = read_files.read_array_sequences()
    print(len(all_sequences))

    # funckija za koju se pravi klasifikator
    function = "GO:0004653"

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    train_test(all_sequences, function)

    cs = [10**i for i in range(-3, 1)]
    gammas = np.logspace(-5, 0, 6)

    for gamma in gammas:
        for c in cs:
            print(c, gamma)
            model = " ../data/models/" + function[3:] + "_" + str(c) + "_" + str(gamma)
            output = " ../data/output/" + function[3:] + "_" + str(c) + "_" + str(gamma)
            model_terminal = "../data/terminal/train_" + function[3:] + "_" + str(c) + "_" + str(gamma) + ".txt"
            output_terminal = "../data/terminal/test_ " + function[3:] + "_" + str(c) + "_" + str(gamma) + ".txt"

            parameters = "-c " + str(c) + " -t 3 -r " + str(gamma)

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
