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


def read_functions_with_proteins(path="../data/parsed_data/functions_with_proteins.txt"):
    file = open(path, "r")
    lines = file.readlines()
    functions_with_proteins = {}

    for line in lines:
        tokens = line.split("->")
        function = tokens[0]
        proteins = tokens[1].split(" ")
        functions_with_proteins[function] = []

        for protein in proteins:
            functions_with_proteins[function].append(protein)

    return functions_with_proteins


def main():
    print(len(read_proteins_with_functions()))
    print(len(read_alt_ids()))
    print(len(read_functions_with_proteins()))
    print(len(read_molecular_functions()))
    print(len(read_obsoletes()))


if __name__ == '__main__':
    main()
