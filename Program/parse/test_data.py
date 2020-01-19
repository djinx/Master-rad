from parse import array_sequences, sequences, read_files, proteins_and_functions


def parse_file(test_proteins):
    organisms_file = open("../data/original_data/cafa.fasta", "r")
    proteins_file = open("../data/original_data/test_proteins_with_organisms.txt", "a")
    proteins = []

    all_lines = organisms_file.read()
    lines = all_lines.split("\n")

    for line in lines:
        if line.startswith(">"):
            data = line.split(" ")
            protein = data[0].replace(">", "")
            organism = data[1].replace("\n", "")
            if "_" in organism:
                organism = organism.split("_")[1]

            if protein in test_proteins:
                proteins.append(protein)
                proteins_file.write(protein + "->" + organism.lower() + "\n")

    print(len(proteins))

    organisms_file.close()
    proteins_file.close()


def main():
    test_proteins = read_files.read_proteins(path="../data/original_data/mfo_all_type1")
    print(len(test_proteins))
    test_sequences = sequences.molecular_proteins_sequences(test_proteins, "../data/original_data/cafa.fasta")
    array_sequences.array_sequences_file(test_sequences, add="_test.txt")

    functions_with_models = read_files.read_functions("molecular_functions_n_100.txt")
    alt_ids = read_files.read_alt_ids()
    obsoletes = read_files.read_obsoletes()
    leaves = proteins_and_functions.proteins_with_functions_molecular(alt_ids, test_proteins, obsoletes, "../data/original_data/leafonly_MFO.txt")
    parents = read_files.read_map_file("parents.txt")
    proteins_with_all_functions = {}

    for p in leaves:
        all_functions = []

        for f in leaves[p]:
            all_functions.extend(parents[f])
            all_functions.append(f)

        proteins_with_all_functions[p] = []
        for function in all_functions:
            if function in functions_with_models and function not in proteins_with_all_functions[p]:
                proteins_with_all_functions[p].append(function)

        # proteins_and_functions.proteins_with_function_file(proteins_with_all_functions,  path="../data/parsed_data/test_proteins_with_functions.txt")

    for protein in test_proteins:
        if protein not in proteins_with_all_functions:
            print(protein)

    print(len(leaves))


if __name__ == '__main__':
    main()
