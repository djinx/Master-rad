from parse import read_files
import numpy as np

amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
number_of_aa = len(amino_acids)


def array_sequences_file(protein_sequences, k=3, path="../data/parsed_data/array_sequences", add=".txt"):
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


def form_array(protein, k=3):
    # Funkcija formira niz za zadatu sekvencu aminokiselina proteina.
    n = len(protein)
    array = np.zeros(number_of_aa ** k)

    for i in range(0, n - k):
        kmer = protein[i:i + k]
        position = kmer_to_number(kmer, k)
        array[position] += 1

    return array


def kmer_to_number(kmer, k=3):
    # Funkcija pretvara k-gram u broj. Broj se koristi kao indeks u nizu.
    if k == 1:
        return amino_to_number(kmer)

    return kmer_to_number(kmer[:-1], k - 1) * number_of_aa + amino_to_number(kmer[-1])


def amino_to_number(aa):
    # Funkcija dodeljuje broj aminokiselini
    return amino_acids.index(aa)


def main():
    protein_sequences = read_files.read_proteins_with_sequences()
    array_sequences_file(protein_sequences, add="_20_3.txt")


if __name__ == '__main__':
    main()
