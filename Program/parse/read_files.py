def read_molecular_functions(path="../data/parsed_data/molecular_functions", add=".txt"):
    # Citanje molekularnih funkcija
    file = open(path+add, "r")
    lines = file.readlines()
    molecular_functions = []

    for line in lines:
        molecular_functions.append(line.replace("\n", ""))

    file.close()
    return molecular_functions


def read_obsoletes(path="../data/parsed_data/obsolete_functions.txt"):
    # Citanje zastarelih funkcija
    file = open(path, "r")
    lines = file.readlines()
    obsoletes = []

    for line in lines:
        obsoletes.append(line.replace("\n", ""))

    file.close()
    return obsoletes


def read_alt_ids(path="../data/parsed_data/alt_ids.txt"):
    # Citanje alternativnih idetifikatora funkcija
    file = open(path, "r")
    lines = file.readlines()
    alt_ids = {}

    for line in lines:
        functions = line.replace("\n", "").split(" ")
        alt_ids[functions[0]] = functions[1]

    file.close()
    return alt_ids


def read_map_file(file, path="../data/parsed_data/"):
    # Cita datoteke zapisane u obliku kljuc -> vrednosti
    file = open(path+file, "r")
    lines = file.readlines()
    data = {}

    for line in lines:
        tokens = line.replace("\n", "").split("->")
        key = tokens[0]
        values = tokens[1].split(" ")

        data[key] = []

        for value in values:
            if value != "":
                data[key].append(value)

    return data


def read_proteins_with_sequences(path="../data/parsed_data/proteins_with_sequences", add=".txt"):
    # Citanje proteina sa sekvencama
    file = open(path+add, "r")
    lines = file.readlines()
    proteins_with_sequences = {}

    for line in lines:
        tokens = line.split("->")
        protein = tokens[0]
        sequence = tokens[1]
        proteins_with_sequences[protein] = sequence

    file.close()
    return proteins_with_sequences


def read_array_sequences(path="../data/parsed_data/array_sequences", add=".txt"):
    # Citanje proteina sa sekvencama u formatu za datoteke
    file = open(path+add, "r")
    lines = file.readlines()
    array_sequences = {}

    for line in lines:
        tokens = line.split(" ")
        array_sequences[tokens[0]] = " ".join(tokens[1:-1])

    file.close()
    return array_sequences


def read_proteins(positive_proteins=None, path="../data/parsed_data/molecular_proteins", add=".txt"):
    # Citanje spiska proteina koji ce se koristiti prilikom treniranja i testiranja
    file = open(path+add, "r")
    lines = file.readlines()
    proteins = []

    if positive_proteins is None:
        for line in lines:
            proteins.append(line.replace("\n", ""))

    else:
        for line in lines:
            protein = line.replace("\n", "")
            if protein not in positive_proteins:
                proteins.append(protein)

    file.close()
    return proteins


def read_test_functions(path="../data/parsed_data/", file="testing_functions.txt"):
    file = open(path + file, "r")
    lines = file.readlines()
    functions = []

    for line in lines:
        functions.append(line.replace("\n", ""))

    return functions
