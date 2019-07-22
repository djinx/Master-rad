from parse import sequences, proteins_and_functions, ontology
import numpy as np

amino_acids_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

# amino_acids_list = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'
# , 'B', 'Z']
number_of_aa = len(amino_acids_list)


def all_array_sequences(protein_sequences, k=4, path="../data/all_array_sequences.txt", n=10):
    file = open(path, "a")
    array_sequences = {}

    for protein in protein_sequences:
        n -= 1
        sequence = protein_sequences[protein]
        array = form_array(sequence, k)
        array_sequences[protein] = array

        file.write(protein + " ")

        for i in range(0, len(array)):
            if array[i] > 0:
                file.write(str(i+1) + ":" + str(array[i]) + " ")

        file.write("\n")

        if n < 0:
            break

    file.close()
    return array_sequences


def n_array_sequences(protein_sequences, positive_proteins, n=5000, k=4):
    # Funkcija odredjuje sekvence za n proteina
    # protein_sequences sadrze proteine i niske aminokiselina
    # positive_proteins sadrzi listu proteina koji izvrsavaju odredjenu funkciju

    # Ukupan broj proteina koji vse molekulske funckije
    num_of_proteins = len(protein_sequences)

    # Ukupan broj pozitivnih i negativnih instanci
    total_num_of_positive = len(positive_proteins)
    total_num_of_negative = num_of_proteins - total_num_of_positive

    # Broj pozitivnih i negativnih instanci za uzorak
    num_of_positive = round(len(positive_proteins) / num_of_proteins * n)
    num_of_negative = n - num_of_positive

    # Indeksi odabranih instanci
    positive_indices = np.random.choice(total_num_of_positive, num_of_positive, replace=False)
    negative_indices = np.random.choice(total_num_of_negative, num_of_negative, replace=False)

    # Lista negativnih instanci
    negative_proteins = []
    for protein in protein_sequences:
        if protein not in positive_proteins:
            negative_proteins.append(protein)

    # Odabir instanci
    chosen_positive = np.array(positive_proteins)[positive_indices]
    chosen_negative = np.array(negative_proteins)[negative_indices]

    # Formiranje recnika pozitivnih i negativnih instanci sa sekvencama
    positive = {}
    negative = {}

    for protein in chosen_positive:
        positive[protein] = form_array(protein_sequences[protein], k)

    for protein in chosen_negative:
        negative[protein] = form_array(protein_sequences[protein], k)

    return positive, negative


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


def read_sequences(path="../data/parsed_data/all_array_sequences.txt"):
    file = open(path, "r")
    lines = file.readlines()
    array_sequences = {}

    for line in lines:
        tokens = line.split(" ")
        array_sequences[tokens[0]] = " ".join(tokens[1:-1])

    file.close()
    return array_sequences


def main():
    array = read_sequences()
    print(len(array))


if __name__ == '__main__':
    main()
