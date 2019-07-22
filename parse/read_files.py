def read_alt_ids(path="../data/parsed_data/alt_ids.txt"):
    file = open(path, "r")
    lines = file.readlines()
    alt_ids = {}

    for line in lines:
        functions = line.replace("\n", "").split(" ")
        alt_ids[functions[0]] = functions[1]

    file.close()
    return alt_ids


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
