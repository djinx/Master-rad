from parse import read_files
import numpy as np

sequences_path = "../data/parsed_data/array_sequences_test_org_n_100.txt"
pf_path = "../data/parsed_data/proteins_with_functions_test_org_n_100.txt"


def save_functions(proteins, path):
    file = open(path, "w")

    for protein in proteins:
        file.write(protein + "->" + " ".join(proteins[protein]) + "\n")

    file.close()


def save_sequences(proteins, path):
    file = open(path, "w")

    for protein in proteins:
        file.write(protein + " " + proteins[protein] + "\n")

    file.close()


def main():
    # 	- instanca se mora naci u molecular_proteins.txt (obican)
    # 	- instanca ne sme da bude u trening skupu molecular_proteins_n_100.txt (map)
    # 	- instanca treba da iz jednog od organizama proteins_with_organisms.txt (map)
    # 	- instancama formirati podrgaf koji cini njihovu funkciju molecular_functions_n_100.txt (obican)
    all_proteins = read_files.read_array_sequences(add="_20_3.txt")
    train_proteins = read_files.read_proteins(add="_n_100.txt")
    proteins_with_organisms = read_files.read_map_file("proteins_with_organisms.txt")
    molecular_functions = read_files.read_molecular_functions(add="_n_100.txt")
    proteins_with_functions = read_files.read_map_file("proteins_with_functions_parents.txt")

    rest_proteins = []
    print(len(train_proteins))

    for protein in all_proteins:
        if protein not in train_proteins and protein in proteins_with_organisms:
            rest_proteins.append(protein)

    print(len(rest_proteins))

    indices = np.random.choice(len(rest_proteins), 100, replace=False)
    rest_proteins = np.array(rest_proteins)[indices]
    test_proteins_functions = {}
    test_proteins_sequences = {}

    for protein in rest_proteins:
        test_proteins_sequences[protein] = all_proteins[protein]

        functions = proteins_with_functions[protein]
        for function in functions:
            if function in molecular_functions:
                if protein in test_proteins_functions:
                    test_proteins_functions[protein].append(function)
                else:
                    test_proteins_functions[protein] = [function]

    save_functions(test_proteins_functions, pf_path)
    save_sequences(test_proteins_sequences, sequences_path)


if __name__ == '__main__':
    main()
