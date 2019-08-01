def proteins_with_functions_molecular(alt_ids, valid_proteins, obsoletes, path="../data/original_data/uniprot_sprot_exp.txt"):
    # Funkcija za svaki protein odredjuje koje funkcije vrsi
    file = open(path, "r")
    all_lines = file.readlines()
    proteins_molecular = {}

    for line in all_lines:
        tokens = line.split(" ")

        if tokens[2] == "F\n":
            protein = tokens[0]
            function = tokens[1]

            # Preskacemo proteine koji sadrze nestandardne aminokiseline
            if protein not in valid_proteins:
                continue

            # Preskacu se zastarele funkcije
            if function in obsoletes:
                continue

            if function in alt_ids:
                function = alt_ids[function]

            if protein in proteins_molecular:
                if function not in proteins_molecular[protein]:
                    proteins_molecular[protein].append(function)
            else:
                proteins_molecular[protein] = [function]

    file.close()
    return proteins_molecular


def proteins_with_functions_other(proteins_molecular, path="../data/original_data/uniprot_sprot_exp.txt"):
    file = open(path, "r")
    all_lines = file.readlines()
    proteins_other = set()

    for line in all_lines:
        tokens = line.split(" ")
        protein = tokens[0]

        if tokens[2] != "F\n" and protein not in proteins_molecular:
            proteins_other.add(protein)

    file.close()
    return proteins_other


def functions_with_proteins(alt_ids, valid_proteins, obsoletes, path="../data/original_data/uniprot_sprot_exp.txt"):
    # Funkcija za svaku funkciju odredjuje koji proteini je vrse
    # Ima ih 5966, vecina su listovi ontologije, ali ima i unutrasnjih cvorova (1310)
    # Zastarelih je 516, neke se ponavljaju za vise proteina, pa je ukupan broj funkcija 5916
    file = open(path, "r")
    all_lines = file.readlines()
    functions = {}

    for line in all_lines:
        tokens = line.split(" ")

        if tokens[2] == "F\n":
            protein = tokens[0]
            function = tokens[1]

            # Preskacemo proteine koji sadrze nestandardne aminokiseline
            if protein not in valid_proteins:
                continue

            # Preskacu se zastarele funkcije
            if function in obsoletes:
                continue

            if function in alt_ids:
                function = alt_ids[function]

            if function in functions:
                functions[function].append(protein)
            else:
                functions[function] = [protein]

    file.close()
    return functions


def all_functions_with_proteins(function, functions, ontology_tree):

    children = ontology_tree[function]

    if function in functions:
        proteins = functions[function]
    else:
        proteins = []

    for child in children:
        all_functions_with_proteins(child, functions, ontology_tree)

        if child in functions:
            proteins.extend(functions[child])

    if function in functions:
        set_current = set(functions[function])
    else:
        set_current = set([])
    set_proteins = set(proteins)
    functions[function] = list(set_current) + list(set_proteins - set_current)


def proteins_with_function_file(proteins):
    file = open("../data/parsed_data/proteins_with_functions.txt", "w")

    for protein in proteins:
        functions = proteins[protein]
        file.write(protein + "->" + " ".join(functions) + "\n")

    file.close()


def functions_with_proteins_file(functions):
    file = open("../data/parsed_data/functions_with_proteins.txt", "w")

    for function in functions:
        proteins = functions[function]
        file.write(function + "->" + " ".join(proteins) + "\n")

    file.close()


def proteins_file(proteins, path):
    file = open(path, "w")

    for protein in proteins:
        file.write(protein + "\n")

    file.close()
