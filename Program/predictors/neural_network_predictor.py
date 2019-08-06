import pandas as pd
from matplotlib import pyplot as plt

from sklearn import model_selection

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.losses import binary_crossentropy

from parse import read_files
from predictors import train_test_data
from datetime import datetime


def main():
    all_sequences = read_files.read_array_sequences("../data/parsed_data/all_array_sequences_20_3.txt")
    print(len(all_sequences))

    function = "GO:0003824"

    print("Priprema pozitivnih i negativnih instanci: ", datetime.now().time())
    x, y = train_test_data.train_test_knn_nn(all_sequences, function, k=3)

    x_train_val, x_test, y_train_val, y_test = model_selection.train_test_split(x, y, test_size=0.25)
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x_train_val, y_train_val,
                                                                                    test_size=0.25)

    # broj neurona za ulazni sloj
    number_of_features = x_train.shape[1]

    # broj neurona za izlazni sloj
    number_of_outputs = 1

    # broj neurona za skriveni sloj
    number_of_neurons = [100, 200, 500, 1000]
    rates = [i/10 for i in range(1, 6)]

    for neurons in number_of_neurons:
        for r in rates:
            # pravljenje modela sa jednim skrivenim slojem
            print("Priprema modela: ", datetime.now().time())
            model_time = datetime.now()
            model = Sequential()
            model.add(Dense(units=neurons, input_dim=number_of_features, activation='relu'))
            model.add(Dropout(rate=r))
            model.add(Dense(units=number_of_outputs, activation='sigmoid'))
            model.compile(optimizer='adam', loss=binary_crossentropy, metrics=['accuracy'])
            model.summary()
            model_time = datetime.now() - model_time

            # obucavanje modela na 30 epoha
            train_time = datetime.now()
            print("Obucavanje modela: ", datetime.now().time())
            history = model.fit(x_train, y_train, epochs=30,
                                batch_size=16, validation_split=0.3, verbose=0)
            train_time = datetime.now() - train_time

            # prikaz grafika tacnosti
            graph_time = datetime.now()
            epochs = history.epoch
            train_loss = history.history['loss']
            val_loss = history.history['val_loss']
            plt.xlabel('Epochs')
            plt.ylabel('Loss function')
            plt.plot(epochs, train_loss, color='red', label='Train loss')
            plt.plot(epochs, val_loss, color='orange', label='Val loss')
            plt.legend(loc='best')

            print("Prikaz grafika: ", datetime.now().time())
            train_acc = history.history['acc']
            val_acc = history.history['val_acc']
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.plot(epochs, train_acc, color='green', label='Train accuracy')
            plt.plot(epochs, val_acc, color='blue', label='Val accuracy')
            plt.legend(loc='best')
            plt.savefig("../data/nn/imgs/neurons_" + str(neurons) + "_rate_" + str(r) + ".png")
            plt.clf()

            graph_time = datetime.now() - graph_time

            # evaluacija konstruisane mreze
            print("Evaluacija mreze: ", datetime.now().time())
            eval_time = datetime.now()
            test_scores = model.evaluate(x_test, y_test)
            test_scores = pd.Series(test_scores, index=model.metrics_names)
            eval_time = datetime.now() - eval_time

            with open("../data/nn/results/neurons" + str(neurons) + "_rate_" + str(r), "w") as file:
                file.write("Vreme za model: " + str(model_time.total_seconds()) + "\n")
                file.write("Vreme za treniranje: " + str(train_time.total_seconds()) + "\n")
                file.write("Vreme za sliku: " + str(graph_time.total_seconds()) + "\n")
                file.write("Vreme za evaluaciju: " + str(eval_time.total_seconds()) + "\n")
                file.write("Test: " + test_scores.to_string())


if __name__ == '__main__':
    main()
