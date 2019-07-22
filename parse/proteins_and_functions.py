from parse import sequences, ontology


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


def main():
    valid_proteins = sequences.protein_sequences().keys()
    fs, obsoletes = ontology.functions()
    proteins = proteins_with_functions(valid_proteins, obsoletes)
    functions = functions_with_proteins(valid_proteins, obsoletes)
    print(len(proteins))
    print(len(functions))

if __name__ == '__main__':
    main()
