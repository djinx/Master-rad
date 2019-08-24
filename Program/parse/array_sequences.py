from parse import read_files
import numpy as np

amino_acids_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
number_of_aa = len(amino_acids_list)


def array_sequences_file(protein_sequences, k=4, path="../data/parsed_data/array_sequences", add=".txt"):
    file = open(path+add, "w")

    for protein in protein_sequences:
        sequence = protein_sequences[protein]
        array = form_array(sequence, k)

        file.write(protein + " ")

        for i in range(0, len(array)):
            if array[i] > 0:
                # obelezavanje svsojstva krece od 1
                file.write(str(i+1) + ":" + str(array[i]) + " ")

        file.write("\n")

    file.close()


def form_array(protein, k=4):
    # Funkcija formira niz za zadatu sekvencu aminokiselina proteina.
    n = len(protein)
    array = np.zeros(number_of_aa ** k)

    for i in range(0, n - k):
        kmer = protein[i:i + k]
        position = kmer_to_number(kmer, k)
        array[position] += 1

    return array


def kmer_to_number(kmer, k=4):
    # Funkcija pretvara k-gram u broj. Broj se koristi kao indeks u nizu.
    if k == 1:
        return amino_to_number(kmer)

    return kmer_to_number(kmer[:-1], k - 1) * number_of_aa + amino_to_number(kmer[-1])


def amino_to_number(aa):
    # Funkcija dodeljuje broj aminokiselini
    amino_acids = {}

    for i in range(0, number_of_aa):
        amino_acids[amino_acids_list[i]] = i

    return amino_acids[aa]


def number_to_kmer(n, k=4):
    # Funkcija pretvara broj u k-gram.
    if k == 1:
        return number_to_amino(n)

    div = n // number_of_aa
    mod = n % number_of_aa

    return number_to_kmer(div, k - 1) + number_to_amino(mod)


def number_to_amino(n):
    # Funkcija pretvara broj u aminokiselinu.
    amino_acids = {}

    for i in range(0, number_of_aa):
        amino_acids[i] = amino_acids_list[i]

    return amino_acids[n]


def main():
    protein_sequences = read_files.read_proteins_with_sequences()
    all_array_sequences_file(protein_sequences, 3, "../data/parsed_data/all_array_sequences_20_3.txt")


if __name__ == '__main__':
    main()
