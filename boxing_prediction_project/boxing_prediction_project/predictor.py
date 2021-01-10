# first neural network with keras tutorial (https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/)
from numpy import loadtxt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from enum import Enum

class BoxingPredictor:
    def __boxerAIsMatch(self, boxersRow, inputs):
        boxerA = boxersRow[range(Columns.age_A.value, Columns.kos_A.value+1, 2)]
        return self.__boxerIsMatch(boxerA, inputs)

    def __boxerBIsMatch(self, boxersRow, inputs):
        boxerB = boxersRow[range(Columns.age_B.value, Columns.kos_B.value+1, 2)]
        return self.__boxerIsMatch(boxerB, inputs)

    def __boxerIsMatch(self, boxer, inputs):
        boxerAge = boxer[Columns.age_A.value//2]
        if(boxerAge != -1 and not (boxerAge < inputs['inputAge'] + 4 and inputs['inputAge'] - 4 < boxerAge) ):
            return False
        boxerHeight = boxer[Columns.height_A.value//2]
        if(boxerHeight != -1 and not (boxerHeight < inputs['inputHeight'] + 10 and inputs['inputHeight'] - 10 < boxerHeight) ):
            return False
        boxerReach = boxer[Columns.reach_A.value//2]
        if(boxerReach != -1 and not (boxerReach < inputs['inputReach'] + 10 and inputs['inputReach'] - 10 < boxerReach) ):
            return False
        if(not boxer[Columns.stance_A.value//2] == inputs['inputStance'].value):
            return False
        boxerWeight = boxer[Columns.weight_A.value//2]
        if(boxerWeight != -1 and not (boxerWeight < inputs['inputWeight'] + 7 and inputs['inputWeight'] - 7 < boxerWeight) ):
            return False
        boxerWon = boxer[Columns.won_A.value//2]
        if(boxerWon != -1 and not (boxerWon < inputs['inputWon'] + 5 and inputs['inputWon'] - 5 < boxerWon) ):
            return False
        boxerLost = boxer[Columns.lost_A.value//2]
        if(boxerLost != -1 and not (boxerLost < inputs['inputLost'] + 4 and inputs['inputLost'] - 4 < boxerLost) ):
            return False
        boxerDrawn = boxer[Columns.drawn_A.value//2]
        if(boxerDrawn != -1 and not (boxerDrawn < inputs['inputDrawn'] + 5 and inputs['inputDrawn'] - 5 < boxerDrawn) ):
            return False
        boxerKos = boxer[Columns.kos_A.value//2]
        if(boxerKos != -1 and not (boxerKos < inputs['inputKos'] + 5 and inputs['inputKos'] - 5 < boxerKos) ):
            return False
        return True

    def predict(self):
        # load the dataset
        boxers = np.genfromtxt('boxing_prediction_project\\boxing_prediction_project\\data\\boxing_matches.csv', delimiter=',', usecols=(range(Columns.age_A.value, Columns.kos_B.value+1)), skip_header=1, missing_values='', filling_values=-1) 
        results = np.genfromtxt('boxing_prediction_project\\boxing_prediction_project\\data\\boxing_matches.csv', delimiter=',', usecols=(Columns.result.value), skip_header=1, missing_values='', filling_values=-1)

        #get input data
        inputAge = 31 #input("Boxer A Age: ")
        inputHeight = 198 #input("Boxer A Height: ")
        inputReach = 208 #input("Boxer A Reach: ")
        inputStance = Stances.orthodox #input("Boxer A Stance(orthodox = 0, southpaw = 1): ")
        inputWeight = 237 #input("Boxer A Weight(lbs): ")
        inputWon = 23 #input("Boxer A Won: ")
        inputLost = 1 #input("Boxer A Lost: ")
        inputDrawn = 0 #input("Boxer A Drawn: ")
        inputKos = 21 #input("Boxer A Kos: ")

        inputsA = {
            'inputAge': inputAge,
            'inputHeight': inputHeight,
            'inputReach': inputReach,
            'inputStance': inputStance,
            'inputWeight': inputWeight,
            'inputWon': inputWon,
            'inputLost': inputLost,
            'inputDrawn': inputDrawn,
            'inputKos': inputKos
        }
        # get x and y from filtered csv
        filter_arr = []
        for i in range(0, len(boxers)):
            filter_arr.append(self.__boxerAIsMatch(boxers[i], inputsA) or self.__boxerBIsMatch(boxers[i], inputsA))
        boxersLikeA = boxers[filter_arr]
        resultsForA = results[filter_arr]

        inputAge = 32 #input("Boxer B Age: ")
        inputHeight = 206 #input("Boxer B Height: ")
        inputReach = 216 #input("Boxer B Reach: ")
        inputStance = Stances.orthodox #input("Boxer B Stance(orthodox = 0, southpaw = 1): ")
        inputWeight = 273 #input("Boxer B Weight(lbs): ")
        inputWon = 30 #input("Boxer B Won: ")
        inputLost = 0 #input("Boxer B Lost: ")
        inputDrawn = 1 #input("Boxer B Drawn: ")
        inputKos = 21 #input("Boxer B Kos: ")

        inputsB = {
            'inputAge': inputAge,
            'inputHeight': inputHeight,
            'inputReach': inputReach,
            'inputStance': inputStance,
            'inputWeight': inputWeight,
            'inputWon': inputWon,
            'inputLost': inputLost,
            'inputDrawn': inputDrawn,
            'inputKos': inputKos
        }
        filter_arr = []
        for i in range(0, len(boxers)):
            filter_arr.append(self.__boxerAIsMatch(boxers[i], inputsB) or self.__boxerBIsMatch(boxers[i], inputsB))
        boxersLikeB = boxers[filter_arr]
        resultsForB = results[filter_arr]

        # define the keras model
        model = Sequential()
        model.add(Dense(27, input_dim=18, activation='relu'))
        model.add(Dense(14, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        # # compile the keras model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # # fit the keras model on the dataset
        allBouts = np.vstack((boxersLikeA, boxersLikeB))
        allResults = np.append(resultsForA, resultsForB)
        model.fit(allBouts, allResults, epochs=int(len(allBouts)/10)+1, batch_size=10)

        # # evaluate the keras model
        _, accuracy = model.evaluate(allBouts, allResults)
        print('Accuracy: %.2f' % (accuracy*100))
        
        bout = [[
            float(inputsA['inputAge']),
            float(inputsB['inputAge']),
            float(inputsA['inputHeight']),
            float(inputsB['inputHeight']),
            float(inputsA['inputReach']),
            float(inputsB['inputReach']),
            float(inputsA['inputStance'].value),
            float(inputsB['inputStance'].value),
            float(inputsA['inputWeight']),
            float(inputsB['inputWeight']),
            float(inputsA['inputWon']),
            float(inputsB['inputWon']),
            float(inputsA['inputLost']),
            float(inputsB['inputLost']),
            float(inputsA['inputDrawn']),
            float(inputsB['inputDrawn']),
            float(inputsA['inputKos']),
            float(inputsB['inputKos'])
        ]]

        boutPrediction = model.predict(np.array(bout))
        print('\n\n\n%s => %d' % (bout[0], boutPrediction))


class Columns(Enum):
    age_A = 0
    age_B = 1
    height_A = 2
    height_B = 3
    reach_A = 4
    reach_B = 5
    stance_A = 6
    stance_B = 7
    weight_A = 8
    weight_B = 9
    won_A = 10
    won_B = 11
    lost_A = 12
    lost_B = 13
    drawn_A = 14
    drawn_B = 15
    kos_A = 16
    kos_B = 17
    result = 18
    decision = 19
    judge1_A = 20
    judge1_B = 21
    judge2_A = 22
    judge2_B = 23
    judge3_A = 24
    judge3_B = 25

class Stances(Enum):
    orthodox = 0
    southpaw = 1

class Result(Enum):
    win_A = 0
    draw = 1
    win_B = 2