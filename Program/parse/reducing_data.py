from parse import read_files, array_sequences
import numpy as np


def reduced_data_file(data, path):
    file = open(path, "w")

    for d in data:
        file.write(d + "\n")

    file.close()


def reduced_functions_with_proteins_file(functions, proteins, test_proteins, path="../data/parsed_data/functions_with_proteins_n_", add=".txt"):
    file = open(path+add, "w")
    functions_with_proteins_all = read_files.read_map_file("functions_with_proteins.txt")

    for function in functions:
        proteins_all = functions_with_proteins_all[function]
        proteins_reduced = []
        for protein in proteins_all:
            if protein in proteins and protein not in test_proteins:
                proteins_reduced.append(protein)

        file.write(function + "->" + " ".join(proteins_reduced) + "\n")

    file.close()


def reduced_proteins_with_functions_file(functions, proteins, test_proteins, path="../data/parsed_data/proteins_with_functions_n_", add=".txt"):
    file = open(path+add, "w")
    proteins_with_functions_all = read_files.read_map_file("proteins_with_functions.txt")

    for protein in proteins:
        if protein in test_proteins:
            continue

        functions_all = proteins_with_functions_all[protein]
        functions_reduced = []
        for function in functions_all:
            if function in functions:
                functions_reduced.append(function)

        file.write(protein + "->" + " ".join(functions_reduced) + "\n")

    file.close()


def test_proteins_with_functions_file():
    test_protein_sequences = read_files.read_array_sequences(add="_test_n_100.txt")
    test_proteins_with_functions = {}

    proteins_with_functions = read_files.read_map_file("proteins_with_functions.txt")
    parent_functions = read_files.read_map_file("parents.txt")

    file = open("../data/parsed_data/proteins_with_functions_test_n_100.txt", "w")

    for protein in test_protein_sequences:
        functions = proteins_with_functions[protein]
        test_proteins_with_functions[protein] = set(functions)

        for function in functions:
            parents = parent_functions[function]
            for parent in parents:
                test_proteins_with_functions[protein].add(parent)

    for protein in test_proteins_with_functions:
        file.write(protein + "->" + " ".join(test_proteins_with_functions[protein]) + "\n")


def main():

    functions_with_proteins = read_files.read_map_file("functions_with_proteins.txt")
    function_number = {}
    accepted_functions = []
    limit = 100
    zero = 0
    less_10 = 0
    less_100 = 0
    less_500 = 0
    rest = 0

    # Odredjivanje broja pojavljivanja svake funkcije u trening skupu
    for function in functions_with_proteins:
        n = len(functions_with_proteins[function])
        function_number[function] = n

        if n == 0:
            zero += 1
        elif n < 10:
            less_10 += 1
        elif n < 100:
            less_100 += 1
        elif n < 500:
            less_500 += 1
        else:
            rest += 1

        # Izdvajanje funkcija koje se pojavljuju bar 100 puta
        if n >= limit:
            accepted_functions.append(function)

    file = open("../data/parsed_data/test_functions.txt", "w")
    for f in function_number:
        if f in accepted_functions:
            file.write(f + " " + str(function_number[f]) + "\n")
    file.close()

    num_func = {}
    for f in function_number:
        if f in accepted_functions:
            num = function_number[f]

            if num not in num_func:
                num_func[num] = [f]
            else:
                num_func[num].append(f)

    file = open("../data/parsed_data/num_functions.txt", "w")
    niz = [i for i in range(1, 36000)]
    for n in niz:
        if n in num_func:
            file.write(str(n) + " " + " ".join(num_func[n]) + "\n")
    file.close()

    # Izdvajanje proteina sa funkcijama koje se pojavljuju bar 100 puta
    proteins_with_functions = read_files.read_map_file("proteins_with_functions.txt")
    protein_sequences = read_files.read_proteins_with_sequences()
    proteins_with_accepted_functions = set()
    final_proteins = {}

    for protein in proteins_with_functions:
        functions = proteins_with_functions[protein]

        for function in functions:
            if function in accepted_functions:
                proteins_with_accepted_functions.add(protein)

    for protein in proteins_with_accepted_functions:
        final_proteins[protein] = protein_sequences[protein]

    indices = np.random.choice(20960, 100, replace=False)
    proteins = [key for key in final_proteins]
    chosen_proteins = np.array(proteins)[indices]
    chosen_proteins_map = {}

    for i in range(0, len(chosen_proteins)):
        protein = str(chosen_proteins[i])
        chosen_proteins_map[protein] = protein_sequences[protein]

    for protein in chosen_proteins:
        del final_proteins[protein]

    # Upis proteina i sekvenci u novu datoteku
    array_sequences.array_sequences_file(final_proteins, k=3, add="_n_" + str(limit) + ".txt")
    array_sequences.array_sequences_file(chosen_proteins_map, k=3, add="_test_n_" + str(limit) + ".txt")

    # Upis smanjenog skupa u datoteke
    reduced_data_file(final_proteins, "../data/parsed_data/molecular_proteins_n_" + str(limit) + ".txt")
    reduced_data_file(accepted_functions, "../data/parsed_data/molecular_functions_n_" + str(limit) + ".txt")

    reduced_functions_with_proteins_file(accepted_functions, final_proteins, chosen_proteins_map, add=str(limit) + ".txt")
    reduced_proteins_with_functions_file(accepted_functions, final_proteins, chosen_proteins_map, add=str(limit) + ".txt")
    test_proteins_with_functions_file()


if __name__ == '__main__':
    main()
