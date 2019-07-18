from parse import sequences


def proteins_with_functions(valid_proteins, path="../data/uniprot_sprot_exp.txt"):
    # Funkcija za svaki protein odredjuje koje funkcije vrsi
    file = open(path, "r")
    all_lines = file.readlines()
    proteins = {}

    for line in all_lines:
        tokens = line.split(" ")

        if tokens[2] == "F\n":
            protein = tokens[0]
            function = tokens[1]

            # Preskacemo proteine koji sadrze nestandardne aminokiseline
            if protein not in valid_proteins:
                continue

            if protein in proteins:
                proteins[protein].append(function)
            else:
                proteins[protein] = []

    file.close()
    return proteins


def functions_with_proteins(path="../data/uniprot_sprot_exp.txt"):
    # Funkcija za svaku funkciju odredjuje koji proteini je vrse
    # Ima ih 5966, vecina su listovi ontologije, ali ima i unutrasnjih cvorova (1310)
    file = open(path, "r")
    all_lines = file.readlines()
    functions = {}

    for line in all_lines:
        tokens = line.split(" ")

        if tokens[2] == "F\n":
            protein = tokens[0]
            function = tokens[1]

            if function in functions:
                functions[function].append(protein)
            else:
                functions[function] = []

    file.close()
    return functions


def main():
    valid_proteins = sequences.protein_sequences().keys()
    proteins = proteins_with_functions(valid_proteins)
    functions = functions_with_proteins()
    print(len(proteins))
    print(len(functions))


if __name__ == '__main__':
    main()
