def protein_sequences(path="../data/uniprot_sprot_exp_molecular.fasta"):
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
            if protein_id != "":
                sequences[protein_id] = sequence

            protein_id = line.replace(">", "").replace("\n", "")
            sequence = ""

        else:
            sequence += line.replace("\n", "")

    # Poslednji protein koji nije upisan jos uvek
    sequences[protein_id] = sequence

    file.close()
    return sequences


def main():
    sequences = protein_sequences()
    print(len(sequences))


if __name__ == '__main__':
    main()
