from datetime import datetime
from time import sleep
import multiprocessing
import subprocess
import numpy as np

# putanje
svm_learn = "../svm_light/svm_learn "
svm_classify = "../svm_light/svm_classify "
train = " ../data/svm/train.txt "
validation = " ../data/svm/validation.txt "


def all_models(function):
    cs = [10**i for i in range(-1, 2)]
    gammas = np.logspace(-4, -1, 4)

    with multiprocessing.Pool(processes=4) as pool:
        # pool.starmap(calculate_one_model, [(gamma, c, function) for gamma in gammas for c in cs])
        pool.starmap(calculate_one_model, [(c, function) for c in cs])


# def calculate_one_model(gamma, c, function):
def calculate_one_model(c, function):
    print("Pocelo trenuranje za C=", c, datetime.now().time())
    model = " ../data/models/" + function[3:] + "_c" + str(c)
    output = " ../data/output/" + function[3:] + "_c" + str(c)
    model_terminal = "../data/terminal/train_" + function[3:] + "_c" + str(c) + ".txt"
    output_terminal = "../data/terminal/val_ " + function[3:] + "_c" + str(c) + ".txt"

    parameters = "-c " + str(c)

    with open(model_terminal, "w") as file:
        file.write("Pocelo trenuranje za c: " + str(c) + " " + str(datetime.now().time()) + "\n")
        subprocess.run(svm_learn + parameters + train + model, stdout=file)
        file.write("Zavrseno treniranje: " + str(datetime.now().time()) + "\n")

    sleep(0.1)

    with open(output_terminal, "w") as file:
        file.write("Pocelo testiranje: " + str(datetime.now().time()) + "\n")
        subprocess.run(svm_classify + validation + model + output, stdout=file)
        file.write("Zavrseno testiranje: " + str(datetime.now().time()) + "\n")
