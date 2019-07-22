from parse import array_sequences, ontology, proteins_and_functions, sequences
from datetime import datetime
import subprocess


def main():
    # nekoliko proteina za testiranje klasifikatora
    # prva 3 izvrsavaju zadatu funkciju, preostali ne
    test_proteins = ['Q53GS7', 'P16892', 'O14368', 'J7FCF0', 'A2A9A2', 'V5JFY4']

    all_sequences = array_sequences.read_sequences()

    # funckija za koju se pravi klasifikator
    function = "GO:0042802"
    fs, obsoletes = ontology.functions()

    # sve sekvence
    protein_sequences = sequences.protein_sequences()
    test_proteins_arrays = [array_sequences.form_array(protein_sequences[p]) for p in test_proteins]
    # proteini koji vrse tu funkciju
    proteins = proteins_and_functions.functions_with_proteins(protein_sequences.keys(), obsoletes)[function]

    # izbaceni test proteini
    for protein in test_proteins:
        del protein_sequences[protein]

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())

    make_train_file(function[3:], proteins, all_sequences)
    make_test_file(function[3:], test_proteins, all_sequences)

    print("Pocelo trenuranje: ", datetime.now().time())
    subprocess.run("../svm_light/svm_learn -t 3 -s 0.00000625 -r 1 -m 100 -# 1000 ../data/input/0042802.txt ../data/models/0042802")
    print("Zavrseno treniranje: ", datetime.now().time())

    print("Pocelo testiranje: ", datetime.now().time())
    subprocess.run("../svm_light/svm_classify ../data/test/0042802.txt ../data/models/0042802 ../data/output/0042802")
    print("Zavrseno testiranje: ", datetime.now().time())


def make_train_file(function, positive, all_sequences):

    path = "../data/input/" + function + ".txt"
    file = open(path, "a")
    file.truncate(0)

    for protein in all_sequences:
        if protein in positive:
            file.write("1 ")
            file.write(all_sequences[protein])
            file.write("\n")

    for protein in all_sequences:
        if protein not in positive:
            file.write("-1 ")
            file.write(all_sequences[protein])
            file.write("\n")

    file.close()


def make_test_file(function, test, all_sequences, n=3):

    path = "../data/test/" + function + ".txt"
    file = open(path, "a")
    file.truncate(0)
    positive = test[:n]
    negative = test[n:]

    for protein in all_sequences:
        if protein in positive:
            file.write("1 ")
            file.write(all_sequences[protein])
            file.write("\n")

    for protein in all_sequences:
        if protein in negative:
            file.write("-1 ")
            file.write(all_sequences[protein])
            file.write("\n")

    file.close()


if __name__ == '__main__':
    main()
