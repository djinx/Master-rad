def read_molecular_functions(path="../data/parsed_data/molecular_functions.txt"):
    file = open(path, "r")
    lines = file.readlines()
    molecular_functions = []

    for line in lines:
        molecular_functions.append(line.replace("\n", ""))

    file.close()
    return molecular_functions


def read_obsoletes(path="../data/parsed_data/obsolete_functions.txt"):
    file = open(path, "r")
    lines = file.readlines()
    obsoletes = []

    for line in lines:
        obsoletes.append(line.replace("\n", ""))

    file.close()
    return obsoletes


def read_alt_ids(path="../data/parsed_data/alt_ids.txt"):
    file = open(path, "r")
    lines = file.readlines()
    alt_ids = {}

    for line in lines:
        functions = line.replace("\n", "").split(" ")
        alt_ids[functions[0]] = functions[1]

    file.close()
    return alt_ids


def read_ontology_tree(path="../data/parsed_data/ontology.txt"):
    file = open(path, "r")
    lines = file.readlines()
    ontology_tree = {}

    for line in lines:
        tokens = line.split(" -> ")
        function = tokens[0]
        children = tokens[1].split(" ")
        ontology_tree[function] = []

        for child in children:
            ontology_tree[function].append(child)

    return ontology_tree


def read_proteins_with_functions(path="../data/parsed_data/proteins_with_functions.txt"):
    file = open(path, "r")
    lines = file.readlines()
    proteins_with_functions = {}

    for line in lines:
        tokens = line.split("->")
        protein = tokens[0]
        functions = tokens[1].split(" ")
        proteins_with_functions[protein] = []

        for function in functions:
            proteins_with_functions[protein].append(function)

    return proteins_with_functions


def read_functions_with_proteins(path="../data/parsed_data/functions_with_proteins_leaves.txt"):
    file = open(path, "r")
    lines = file.readlines()
    functions_with_proteins = {}

    for line in lines:
        tokens = line.replace("\n", "").split("->")
        function = tokens[0]
        proteins = tokens[1].split(" ")
        functions_with_proteins[function] = []

        for protein in proteins:
            functions_with_proteins[function].append(protein)

    return functions_with_proteins


def read_proteins_with_sequences(path="../data/parsed_data/proteins_with_sequences.txt"):
    file = open(path, "r")
    lines = file.readlines()
    proteins_with_sequences = {}

    for line in lines:
        tokens = line.split("->")
        protein = tokens[0]
        sequence = tokens[1]
        proteins_with_sequences[protein] = sequence

    file.close()
    return proteins_with_sequences


def read_array_sequences(path="../data/parsed_data/all_array_sequences.txt"):
    file = open(path, "r")
    lines = file.readlines()
    array_sequences = {}

    for line in lines:
        tokens = line.split(" ")
        array_sequences[tokens[0]] = " ".join(tokens[1:-1])

    file.close()
    return array_sequences


def read_proteins(positive_proteins=None, path="../data/parsed_data/molecular_proteins.txt"):
    file = open(path, "r")
    lines = file.readlines()
    proteins = []

    if positive_proteins is None:
        for line in lines:
            proteins.append(line.replace("\n", ""))

    else:
        print(len(positive_proteins))
        for line in lines:
            protein = line.replace("\n", "")
            if protein not in positive_proteins:
                proteins.append(protein)

    file.close()
    print(len(proteins))
    return proteins
