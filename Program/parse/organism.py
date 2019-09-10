from parse import read_files

organisms_file_path = "../data/original_data/uniprot-proteome_"
all_file_path = "../data/parsed_data/organisms.txt"
proteins_with_organisms_path = "../data/parsed_data/proteins_with_organisms.txt"
molecular_proteins_path = "../data/parsed_data/molecular_proteins_organisms"


def parse_file(file_name):
    organisms_file = open(organisms_file_path + file_name + ".fasta", "r")
    all_file = open(all_file_path, "a")
    proteins_file = open(proteins_with_organisms_path, "a")
    proteins = []

    all_lines = organisms_file.read()
    lines = all_lines.split("\n")

    for line in lines:
        if line.startswith(">"):
            data = line.split("|")
            proteins.append(data[1])
            proteins_file.write(data[1] + "->" + file_name + "\n")

    all_file.write(file_name + "->" + " ".join(proteins) + "\n")
    print(file_name, len(proteins))

    organisms_file.close()
    all_file.close()
    proteins_file.close()


def add_to_file(protein, organism, file_name=".txt"):
    file = open(molecular_proteins_path + file_name, "a")

    file.write(protein + "->" + organism + "\n")

    file.close()


def main():
    organisms = ['human', 'mouse', 'rat', 'ecoli', 'arath']
    # organisms = ['pig', 'drome', 'danre', 'orysj', '9rhiz']
    for organism in organisms:
        parse_file(organism)

    proteins_with_organisms = read_files.read_map_file("proteins_with_organisms.txt")
    proteins = read_files.read_proteins(add="_n_100.txt")
    unknown_organism_proteins = []

    for protein in proteins:
        if protein in proteins_with_organisms:
            add_to_file(protein, proteins_with_organisms[protein][0], "_n_100.txt")
        else:
            unknown_organism_proteins.append(protein)

    print(len(unknown_organism_proteins))


if __name__ == '__main__':
    main()
