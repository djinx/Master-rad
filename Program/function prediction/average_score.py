from parse import read_files


def scores_organism(organism):
    organism_scores = read_files.read_map_file("test_svm_" + organism, "../")
    f1 = 0
    acc = 0
    pre = 0
    rec = 0
    auc = 0
    num_of_proteins = len(organism_scores)
    
    for protein in organism_scores:
        scores = organism_scores[protein]
        f1 += float(scores[0])
        acc += float(scores[1])
        pre += float(scores[2])
        rec += float(scores[3])
        auc += float(scores[4])

    return f1/num_of_proteins, acc/num_of_proteins, pre/num_of_proteins, rec/num_of_proteins, auc/num_of_proteins


def main():
    organisms = ['human', 'mouse', 'rat', 'ecoli', 'arath', 'all']

    avg_f1s = []
    avg_accs = []
    avg_pres = []
    avg_recs = []
    avg_aucs = []

    for organism in organisms:
        f1, acc, pre, rec, auc = scores_organism(organism)

        avg_f1s.append(f1)
        avg_accs.append(acc)
        avg_pres.append(pre)
        avg_recs.append(rec)
        avg_aucs.append(auc)

    print("F1:", avg_f1s)
    print("Acc:", avg_accs)
    print("Pre:", avg_pres)
    print("Rec:", avg_recs)
    print("AUC:", avg_aucs)

    file = open("../test_scores_svm.txt", "w")
    file.write("F1:" + " ".join(str(a) for a in avg_f1s) + "\n")
    file.write("Acc:" + " ".join(str(a) for a in avg_accs) + "\n")
    file.write("Pre:" + " ".join(str(a) for a in avg_pres) + "\n")
    file.write("Rec:" + " ".join(str(a) for a in avg_recs) + "\n")
    file.write("AUC:" + " ".join(str(a) for a in avg_aucs) + "\n")

    file.close()


if __name__ == '__main__':
    main()
