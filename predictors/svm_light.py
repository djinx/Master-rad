from parse import read_files
from predictors.train_test_data import train_test
from datetime import datetime
import subprocess


def main():
    # nekoliko proteina za testiranje klasifikatora
    all_sequences = read_files.read_array_sequences()

    # funckija za koju se pravi klasifikator
    function = "GO:0042802"

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    train_test(all_sequences, function)

    model = "../data/models/" + function[3:]
    output = "../data/output/" + function[3:]

    print("Pocelo trenuranje: ", datetime.now().time())
    subprocess.run("../svm_light/svm_learn -m 200 -# 1000 ../data/svm/train.txt " + model)
    print("Zavrseno treniranje: ", datetime.now().time())

    print("Pocelo testiranje: ", datetime.now().time())
    subprocess.run("../svm_light/svm_classify ../data/svm/validation.txt " + model + " " + output)
    print("Zavrseno testiranje: ", datetime.now().time())


if __name__ == '__main__':
    main()
