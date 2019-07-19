from predictors import one_function
from parse import array_sequences, ontology, proteins_and_functions, sequences


def main():
    # nekoliko proteina za testiranje klasifikatora
    # prva 3 izvrsavaju zadatu funkciju, preostali ne
    test_proteins = ['Q53GS7', 'P16892', 'O14368', 'J7FCF0', 'A2A9A2', 'V5JFY4']

    # funckija za koju se pravi klasifikator
    function = "GO:0042802"
    fs, obsoletes = ontology.functions()

    # proteini koji vrse tu funkciju
    proteins = proteins_and_functions.functions_with_proteins(obsoletes)[function]

    # sve sekvence
    protein_sequences = sequences.protein_sequences()

    # izbaceni test proteini
    for protein in test_proteins:
        del protein_sequences[protein]

    all_sequences = array_sequences.all_array_sequences(protein_sequences)

    classificator = one_function.one_function_predictor(all_sequences, proteins)

    prediction = classificator.predict(test_proteins)
    print(prediction)


if __name__ == '__main__':
    main()
