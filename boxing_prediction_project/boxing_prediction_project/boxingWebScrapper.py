import requests
import bout as BoutData
import recaptcha_v2_solver as recaptchaSolver
import proxiesGenerator
from bs4 import BeautifulSoup
import time
import math
import logging
import random
import string
from urllib.error import HTTPError
from termcolor import colored


class BoxingWebScrapper:
    
    def __init__(self, rootLink, username, password, loginLink, timeout=5):
        self.rootLink = rootLink
        self.session = requests.Session()
        self.timeout = timeout
        self.username = username
        self.password = password
        self.loginPayload = {'_username': username, '_password': password}
        self.loginLink = loginLink
        self.recaptchaSolver = recaptchaSolver.RecaptchaSolver(username, password, loginLink)
        proxy = proxiesGenerator.ProxiesGenerator().getRandomProxy()
        self.session.proxies.update(proxy)
        self.__setHeaders()

    def __setHeaders(self):
        self.session.headers.update({'Host': 'boxrec.com'})
        self.session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"})
        self.session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
        self.session.headers.update({'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'})
        self.session.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
        self.session.headers.update({'DNT': '1'})
        self.session.headers.update({'Connection': 'keep-alive'})
        self.session.headers.update({'Upgrade-Insecure-Requests': '1'})
        self.session.headers.update({'Pragma': 'no-cache'})
        self.session.headers.update({'Cache-Control': 'no-cache'})
    
    def login(self):
        self.session.post(self.loginLink, data=self.loginPayload)

    def getAllBoutLinks(self, allBoutsLink):
        soup = self.__makeSoup(allBoutsLink)
        boutLinks = []
        allActionCells = soup.findAll('td', attrs={'class': 'actionCell drawRowBorder'})

        for actionCell in allActionCells:
            anchorsInCell = actionCell.findAll('a')
            boutHref = anchorsInCell[1]['href']
            boutLinks.append(self.rootLink + boutHref)

        return boutLinks

    def getBoutData(self, boutLink: str, id=None):
        if(id==None):
            id = self.getIdFromLink(boutLink)

        soup = self.__makeSoup(boutLink)
        return self.__getBoutDataFromSoup(id, soup)

    def getIdFromLink(self, boutLink):
        splittedLink = boutLink.split('/')
        return splittedLink[-2] + splittedLink[-1]
    
    def __makeSoup(self, link: str):
        response = self.session.get(link, timeout=self.timeout)
        while(response.status_code == 429):
            print(colored("429 Error on last petition to: "+ colored(link, 'green'), 'yellow'))
            print("\tTrying to resolve recaptcha")
            self.recaptchaSolver.solveRecaptcha()
            response = self.session.get(link, timeout=self.timeout)
    
        return BeautifulSoup(response.text, 'html.parser')

    def __getBoutDataFromSoup(self, id, soup):
        bout = BoutData.Bout(id=id)

        bout.country = self.__getBoutContryFromSoup(soup)
        
        tableBout = soup.find('table', attrs={'class': 'responseLessDataTable'})
        for row in tableBout.findAll('tr'):
            allCellsInRow = row.findAll('td')
            if(len(allCellsInRow) != 3):
                continue
            self.__setBoutDataInRowCells(bout, allCellsInRow)

        bout.boxerA.refreshBoutNumber()
        bout.boxerB.refreshBoutNumber()

        return bout
    
    def __getBoutContryFromSoup(self, soup):
        countryAnchor = soup.findAll('a', attrs={'href': lambda value: value and value.startswith('/en/locations/event?country=')})
        return countryAnchor[-1].text
    
    def __setBoutDataInRowCells(self, bout, allCellsInRow):        
        titleRow = allCellsInRow[1].text
        if(titleRow == '' and bout.boxerA.name == None and bout.boxerB.name == None):
            bout.winner = self.__getBoutWinner(allCellsInRow)
            bout.boxerA.name = self.__getBoxerName(allCellsInRow[0])
            bout.boxerB.name = self.__getBoxerName(allCellsInRow[2])
        elif(titleRow == 'age'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.age = int(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.age = int(allCellsInRow[2].text)
        elif(titleRow == 'stance'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.stance = ''.join(e for e in allCellsInRow[0].text if e.isalnum())
            if(allCellsInRow[2].text != ''):
                bout.boxerB.stance = ''.join(e for e in allCellsInRow[2].text if e.isalnum())
        elif(titleRow == 'height'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.height = self.__getHeightReachInCM(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.height = self.__getHeightReachInCM(allCellsInRow[2].text)
        elif(titleRow == 'reach'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.reach = self.__getHeightReachInCM(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.reach = self.__getHeightReachInCM(allCellsInRow[2].text)
        elif(titleRow == 'won'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.recordWon = int(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.recordWon = int(allCellsInRow[2].text)
        elif(titleRow == 'lost'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.recordLost = int(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.recordLost = int(allCellsInRow[2].text)
        elif(titleRow == 'drawn'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.recordDraw = int(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                    bout.boxerB.recordDraw = int(allCellsInRow[2].text)
        elif(titleRow == 'KOs'):
            if(allCellsInRow[0].text != ''):
                bout.boxerA.recordKOs = int(allCellsInRow[0].text)
            if(allCellsInRow[2].text != ''):
                bout.boxerB.recordKOs = int(allCellsInRow[2].text)

    def __getBoutWinner(self, allCellsInRow):
        leftCell:str = allCellsInRow[0].text
        rightCell:str = allCellsInRow[2].text

        if(leftCell.find('won ')>=0):
            return -1
        elif(rightCell.find('won ')>=0):
            return 1
        return 0

    def __getBoxerName(self, boxerCell):
        splitedTextCell = boxerCell.text.split('\n')
        if(len(splitedTextCell) <= 1):
            return
        return splitedTextCell[1].strip()


    def __getHeightReachInCM(self, textValue: str):
        cmString = textValue.split('/')[-1]
        numericCM = ''.join(c for c in cmString if c.isnumeric())
        if(not numericCM.isnumeric()):
            return -1
        return int(numericCM)


    
    