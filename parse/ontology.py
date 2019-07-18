def functions(path="../data/go.obo"):
    # Funckija izdvaja sve molekulske funkcije u mapu
    file = open(path, "r")
    all_lines = file.read()
    all_functions = all_lines.split("[Term]")
    del all_functions[0]

    # mapa sa siframa molekulskih funkcija i podacima o njima
    # ime, definicija, roditeljske funkcije
    molecular_functions = {}

    for function in all_functions:
        # Izdvajaju se samo molekulske funkcije i to one koje nisu zastarele
        if function.find("namespace: molecular_function") != -1 and function.find("is_obsolete: true") == -1:
            function_info = function.split("\n")
            function_id = function_info[1][4:]
            name = function_info[2][6:]
            definition = ''
            parents = []

            for info in function_info:
                if info.startswith("def:"):
                    definition = info[6:]

                if info.startswith("is_a"):
                    parent = info.split(" ")
                    parents.append(parent[1])

            if len(parents) == 0:
                parents = "root"

            molecular_functions[function_id] = {
                "name": name,
                "definition": definition,
                "parents": parents
            }

    file.close()
    return molecular_functions


def ontology_tree(molecular_functions):
    # Funkcija formira ontologiju na osnovu mape funkcija
    tree = {}

    for function_id in molecular_functions:
        function_info = molecular_functions[function_id]
        parents = function_info["parents"]

        if function_id not in tree:
            tree[function_id] = []

        if parents == "root":
            continue

        for parent in parents:
            if parent in tree:
                tree[parent].append(function_id)

            else:
                tree[parent] = []

    return tree


def main():
    fs = functions()
    tree = ontology_tree(fs)
    print(len(fs))
    print(len(tree))


if __name__ == '__main__':
    main()
