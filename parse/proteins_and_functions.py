def proteins_with_functions(valid_proteins, obsoletes, path="../data/original_data/uniprot_sprot_exp.txt"):
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

            # Preskacu se zastarele funkcije
            if function in obsoletes:
                continue

            if protein in proteins:
                proteins[protein].append(function)
            else:
                proteins[protein] = [function]

    file.close()
    return proteins


def functions_with_proteins(valid_proteins, obsoletes, path="../data/original_data/uniprot_sprot_exp.txt"):
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

            if function in functions:
                functions[function].append(protein)
            else:
                functions[function] = [protein]

    file.close()
    return functions


def proteins_with_function_file(proteins, alt_ids):
    file = open("../data/parsed_data/proteins_with_functions.txt", "w")

    for protein in proteins:
        functions = proteins[protein]
        file.write(protein + "->")
        for function in functions:
            if function in alt_ids:
                file.write(alt_ids[function] + " ")
            else:
                file.write(function + " ")
        file.write("\n")

    file.close()


def function_with_proteins_file(functions, alt_ids):
    file = open("../data/parsed_data/functions_with_proteins.txt", "w")

    for function in functions:
        proteins = functions[function]
        if function in alt_ids:
            file.write(alt_ids[function] + "->")
        else:
            file.write(function + "->")

        file.write(" ".join(proteins) + "\n")

    file.close()
