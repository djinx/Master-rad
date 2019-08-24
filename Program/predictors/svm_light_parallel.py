from parse import read_files
from predictors.train_test_data import train_test_svm_light
from predictors.models_parallel import all_models
from datetime import datetime


def main():
    # nekoliko proteina za testiranje klasifikatora
    all_sequences = read_files.read_array_sequences(add="_20_3.txt")
    print(len(all_sequences))

    # funckija za koju se pravi klasifikator
    function = "GO:0003824"

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    train_test_svm_light(all_sequences, function, k=3)

    print("Pocinje paralelno izracunavanje modela: ", datetime.now().time())
    all_models(function)


if __name__ == '__main__':
    main()
