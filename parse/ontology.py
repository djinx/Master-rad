def functions(path="../data/original_data/go.obo"):
    # Funckija izdvaja sve molekulske funkcije u mapu
    file = open(path, "r")
    all_lines = file.read()
    all_functions = all_lines.split("[Term]")
    del all_functions[0]

    # mapa sa siframa molekulskih funkcija i podacima o njima
    # ime, definicija, roditeljske funkcije
    molecular_functions = {}
    obsoletes = []

    for function in all_functions:
        # Izdvajaju se samo molekulske funkcije i to one koje nisu zastarele
        if function.find("namespace: molecular_function") != -1:
            if function.find("is_obsolete: true") == -1:
                function_info = function.split("\n")
                function_id = function_info[1][4:]
                name = function_info[2][6:]
                definition = ""
                parents = []

                # Neke funkcije imaju alterantivne identifikatore
                alt_ids = []

                for info in function_info:
                    if info.startswith("def:"):
                        definition = info[6:]

                    if info.startswith("alt_id:"):
                        alt_ids.append(info[8:].replace("\n", ""))

                    if info.startswith("is_a"):
                        parent = info.split(" ")
                        parents.append(parent[1])

                if len(parents) == 0:
                    parents = "root"

                molecular_functions[function_id] = {
                    "name": name,
                    "definition": definition,
                    "parents": parents,
                    "alt_id": []
                }

                for alt_id in alt_ids:
                    molecular_functions[alt_id] = {
                        "name": name,
                        "definition": definition,
                        "parents": parents,
                        "alt_id": function_id
                    }

                    molecular_functions[function_id]["alt_id"] = alt_ids

            else:
                function_info = function.split("\n")
                function_id = function_info[1][4:]
                obsoletes.append(function_id)

    file.close()
    return molecular_functions, obsoletes


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
    fs, obsoletes = functions()
    tree = ontology_tree(fs)
    print(len(fs))
    print(len(tree))
    print(len(obsoletes))


if __name__ == '__main__':
    main()
