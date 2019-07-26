from datetime import datetime
import subprocess
import numpy as np


def main():
    # putanje
    svm_classify = "../svm_light/svm_classify "
    test = " ../data/svm/test.txt "

    # funckija za koju se pravi klasifikator
    function = "GO:0003700"

    cs = [10 ** i for i in range(-1, 2)]
    gammas = np.logspace(-4, 2, 7)

    for gamma in gammas:
        print("Pocelo testiranje za gamma: ", gamma, datetime.now().time())
        for c in cs:
            print("\t", c, datetime.now().time())
            model = " ../data/models/smaller_set/" + function[3:] + "_g" + str(gamma) + "_c" + str(c)
            output = " ../data/output/test_smaller_set/" + function[3:] + "_g" + str(gamma) + "_c" + str(c)
            output_terminal = "../data/terminal/test_smaller_set/test_ " + function[3:] + "_g" + str(gamma) + "_c" + str(c) + ".txt"

            with open(output_terminal, "w") as file:
                file.write("Pocelo testiranje: " + str(datetime.now().time()) + "\n")
                subprocess.run(svm_classify + test + model + output, stdout=file)
                file.write("Zavrseno testiranje: " + str(datetime.now().time()) + "\n")


if __name__ == '__main__':
    main()
