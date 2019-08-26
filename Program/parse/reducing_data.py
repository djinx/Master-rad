from parse import read_files, array_sequences


def reduced_data_file(data, path):
    file = open(path, "w")

    for d in data:
        file.write(d + "\n")

    file.close()


def reduced_functions_with_proteins_file(functions, proteins, path="../data/parsed_data/functions_with_proteins_n_", add=".txt"):
    file = open(path+add, "w")
    functions_with_proteins_all = read_files.read_map_file("functions_with_proteins.txt")

    for function in functions:
        proteins_all = functions_with_proteins_all[function]
        proteins_reduced = []
        for protein in proteins_all:
            if protein in proteins:
                proteins_reduced.append(protein)

        file.write(function + "->" + " ".join(proteins_reduced) + "\n")

    file.close()


def reduced_proteins_with_functions_file(functions, proteins, path="../data/parsed_data/proteins_with_functions_n_", add=".txt"):
    file = open(path+add, "w")
    proteins_with_functions_all = read_files.read_map_file("proteins_with_functions.txt")

    for protein in proteins:
        functions_all = proteins_with_functions_all[protein]
        functions_reduced = []
        for function in functions_all:
            if function in functions:
                functions_reduced.append(function)

        file.write(protein + "->" + " ".join(functions_reduced) + "\n")

    file.close()


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

    # Upis proteina i sekvenci u novu datoteku
    array_sequences.array_sequences_file(final_proteins, k=3, add="_n_" + str(limit) + ".txt")

    # Upis smanjenog skupa u datoteke
    reduced_data_file(final_proteins, "../data/parsed_data/molecular_proteins_n_ " + str(limit) + ".txt")
    reduced_data_file(accepted_functions, "../data/parsed_data/molecular_functions_n_ " + str(limit) + ".txt")

    reduced_functions_with_proteins_file(accepted_functions, final_proteins, add=str(limit) + ".txt")
    reduced_proteins_with_functions_file(accepted_functions, final_proteins, add=str(limit) + ".txt")


if __name__ == '__main__':
    main()
