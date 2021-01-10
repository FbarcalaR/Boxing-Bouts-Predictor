import csv
import boxingWebScrapper as scrapperService
import boxingSelenium as seleniumSraperService
import predictor as boxingPredictor
from numpy import loadtxt
import traceback
from urllib.error import HTTPError
import time
import random


allExistingIds = []

def getDataSelenium(boxerId, username, password):
    boxingScrapper = seleniumSraperService.BoxingSelenium(rootLink='https://boxrec.com')

    loginLink='https://boxrec.com/en/login'
    boxingScrapper.login(loginLink, username, password)
    boxingScrapper.tryCloseCookiesAdvice()

    boxerId = '7035'
    allBoutLinks = boxingScrapper.getAllBoutLinks('https://boxrec.com/en/proboxer/'+boxerId, boxerId)

    boxingDataCsv = open('boxing_prediction_project\\boxing_prediction_project\\data\\boxing-bouts-data.csv', 'a')
    boxingDataCsv.close()
    try:
        for i, boutLink in enumerate(allBoutLinks):
            id = float(boxingScrapper.getIdFromLink(boutLink))
            if(id in allExistingIds):
                continue
            boxingDataCsv = open('boxing_prediction_project\\boxing_prediction_project\\data\\boxing-bouts-data.csv', 'a')
            wr = csv.writer(boxingDataCsv)
            searchWasPerformed = boxingScrapper.randomSearch()
            if(searchWasPerformed):
                boxingScrapper.goBackToBoxer(boxerId)
            bout = boxingScrapper.getBoutData(boutLink, 'https://boxrec.com/en/proboxer/'+boxerId, boxerId)
            wr.writerow(bout.toString().split(','))
            allExistingIds.append(id)
            print(bout.toString())
            boxingDataCsv.close()
    finally:
        if(boxingDataCsv.closed != True):
            boxingDataCsv.close()

def getDataFromBoxerLink(link):
    allBoutLinks = boxingScrapper.getAllBoutLinks(link)
    allBouts = []

    boxingDataCsv = open('boxing_prediction_project\\boxing_prediction_project\\data\\boxing-bouts-data.csv', 'a')
    boxingDataCsv.close()
    try:
        for i, boutLink in enumerate(allBoutLinks):
            id = float(boxingScrapper.getIdFromLink(boutLink))
            if(id in allExistingIds):
                continue
            boxingDataCsv = open('boxing_prediction_project\\boxing_prediction_project\\data\\boxing-bouts-data.csv', 'a')
            wr = csv.writer(boxingDataCsv)
            time.sleep(random.choice(range(3, 9)))
            bout = boxingScrapper.getBoutData(boutLink)
            wr.writerow(bout.toString().split(','))
            allExistingIds.append(id)
            print("\t"+bout.toString())
            boxingDataCsv.close()
    finally:
        if(boxingDataCsv.closed != True):
            boxingDataCsv.close()

def scrapeData(username, password):
    loginLink='https://boxrec.com/en/login'
    boxingScrapper = scrapperService.BoxingWebScrapper(rootLink='https://boxrec.com', username = username, password = password, loginLink=loginLink)
    boxingScrapper.login()
    allExistingIds = loadtxt('boxing_prediction_project\\boxing_prediction_project\\data\\boxing-bouts-data.csv', delimiter=',', usecols=[0]).tolist()

    for boxerId in range(11, 1000000):
        link = 'https://boxrec.com/en/proboxer/' + str(boxerId)
        print("searching in link: " + link)
        getDataFromBoxerLink(link)

# username = input('BoxRec username: ')
# password = input('BoxRec password: ')
# scrapeData(username, password)
boxingPredictor.BoxingPredictor().predict()












