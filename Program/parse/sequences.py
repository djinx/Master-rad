from parse import read_files


def molecular_proteins_sequences(molecular_proteins, path="../data/original_data/uniprot_sprot_exp_molecular.fasta"):
    # Funkcija izdvaja sekvence aminokiselina za svaki od proteina koji vrsi bar jednu molekulsku funckiju
    file = open(path, "r")
    all_lines = file.read()
    lines = all_lines.split("\n")

    # Mapa cuva podatke u obliku identifikator proteina -> sekvenca
    sequences = {}
    protein_id = ""
    sequence = ""

    for line in lines:
        if line.startswith(">"):
            if protein_id != "" and protein_id in molecular_proteins:
                sequences[protein_id] = sequence

            protein_id = line.replace(">", "").replace("\n", "")
            sequence = ""

        else:
            sequence += line.replace("\n", "")

    # Poslednji protein koji nije upisan jos uvek
    sequences[protein_id] = sequence

    file.close()
    return sequences


def other_proteins_sequences(other_proteins, path="../data/original_data/uniprot_sprot_exp.fasta"):
    # Funkcija izdvaja sekvence aminokiselina za svaki od proteina koji ne vrsi nijednu molekulsku funckiju
    file = open(path, "r")
    all_lines = file.read()
    lines = all_lines.split("\n")

    # Mapa cuva podatke u obliku identifikator proteina -> sekvenca
    sequences = {}
    protein_id = ""
    sequence = ""

    for line in lines:
        if line.startswith(">"):
            if protein_id != "" and protein_id in other_proteins:
                sequences[protein_id] = sequence

            protein_id = line.replace(">", "").replace("\n", "")
            sequence = ""

        else:
            sequence += line.replace("\n", "")

    # Poslednji protein koji nije upisan jos uvek
    sequences[protein_id] = sequence

    file.close()
    return sequences


def protein_sequences_file(proteins_with_sequences, path):
    file = open(path, "w")

    for protein in proteins_with_sequences:
        file.write(protein + "->" + proteins_with_sequences[protein] + "\n")

    file.close()
