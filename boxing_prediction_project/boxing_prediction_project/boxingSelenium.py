from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time
import random
import bout as BoutData
import string
import numpy as np
import scipy.interpolate as si


class BoxingSelenium:

    def __init__(self, rootLink):
        ## maybe (executable_path=r'your\path\geckodriver.exe') is nos necessary
        self.driver = webdriver.Firefox(executable_path='C:\\Python\\geckodriver.exe')
        self.rootLink = rootLink
        self.x_i, self.y_i = self.__getMoveMousePoints()

    def login(self, loginLink, userName, password):
        self.get(loginLink)
        userNameElem = self.driver.find_element_by_id('username')
        userNameElem.send_keys(userName)
        passwordElem = self.driver.find_element_by_id('password')
        passwordElem.send_keys(password)
        goElem = self.driver.find_element_by_name("login[go]")
        self.moveMouse(goElem)
        goElem.click()
    
    def tryCloseCookiesAdvice(self):
        # time.sleep(random.choice(range(5, 10)))
        button = self.driver.find_element_by_class_name('ffdCHe')
        self.moveMouse(button)
        button.click()
        time.sleep(random.choice(range(2, 7)))

        
    def __makeSoup(self, link: str):
        response = self.driver.page_source    
        return BeautifulSoup(response, 'html.parser')
    
    def getAllBoutLinks(self, allBoutsLink, boxerId):
        self.goBackToBoxer(boxerId)
        soup = self.__makeSoup(allBoutsLink)
        boutLinks = []
        allActionCells = soup.findAll('td', attrs={'class': 'actionCell drawRowBorder'})

        for actionCell in allActionCells:
            anchorsInCell = actionCell.findAll('a')
            boutHref = anchorsInCell[1]['href']
            # boutLinks.append(self.rootLink + boutHref)
            boutLinks.append(boutHref)

        return boutLinks
    
    def getBoutData(self, boutLink: str, boxerLink, boxerId):
        if(self.driver.current_url != boxerLink):
            self.goBackToBoxer(boxerId)
        
        id = self.getIdFromLink(boutLink)

        boutLinkElem = self.driver.find_element_by_xpath('//a[@href="'+boutLink+'"]')
        self.__scrollToElement(boutLinkElem)
        # time.sleep(random.choice(range(2, 6)))
        self.moveMouse(boutLinkElem)
        self.driver.execute_script("arguments[0].click()", boutLinkElem)
        # self.clickElementWhenClickable(boutLinkElem, '//a[@href="'+boutLink+'"]')
        
        time.sleep(random.choice(range(2, 6)))
        soup = self.__makeSoup(boutLink)
        result = self.__getBoutDataFromSoup(id, soup)
        time.sleep(random.choice(range(2, 6)))

        self.driver.execute_script("window.history.go(-1)")
        return result
    
    
    def getIdFromLink(self, boutLink):
        splittedLink = boutLink.split('/')
        return splittedLink[-2] + splittedLink[-1]

    def randomSearch(self):
        if(random.choice(range(0, 2)) == 1):
            # time.sleep(random.choice(range(5, 9)))
            searchBox = self.driver.find_element_by_id('si_search_text')
            searchBox.clear()
            randomTerm = self.__getRandomString(random.choice(range(2, 7)))
            searchBox.send_keys(randomTerm, Keys.ENTER)

            if(random.choice(range(0, 10)) > 6):
                self.__clickAResult()

            self.randomSearch()
            return True

        return False
    
    def goBackToBoxer(self, boxerId):
        searchBox = self.driver.find_element_by_id('si_search_text')
        searchBox.clear()
        searchBox.send_keys(boxerId, Keys.ENTER)
        time.sleep(random.choice(range(4, 9)))
        
    def moveMouse(self, element):
        action =  ActionChains(self.driver)

        action.move_to_element(element);
        action.perform();

        for mouse_x, mouse_y in zip(self.x_i, self.y_i):
            action.move_by_offset(mouse_x,mouse_y);
            action.perform();

    def get(self, link):
        self.driver.get(link)
        time.sleep(random.choice(range(5, 9)))
    
    def clickElementWhenClickable(self, elememt, xpath):
        element = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))

        self.moveMouse(element)
        element.click();
    
    def __getMoveMousePoints(self):
        # Curve base:
        points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]];
        points = np.array(points)

        x = points[:,0]
        y = points[:,1]


        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 25)

        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list) # x interpolate values
        y_i = si.splev(ipl_t, y_list) # y interpolate values
        return x_i, y_i
    
    def __clickAResult(self):
        try:
            time.sleep(random.choice(range(7, 13)))
            allHrefInSamePage = self.driver.find_elements_by_xpath("//a[starts-with(@href, '/en/')]")
            if(len(allHrefInSamePage)==0):
                return
            selectedAnchor = random.choice(allHrefInSamePage)
            while (not selectedAnchor.is_enabled() or not selectedAnchor.is_displayed()):
                selectedAnchor = random.choice(allHrefInSamePage)
            
            # self.__scrollToElement(selectedAnchor)
            # time.sleep(random.choice(range(3, 5)))
            # selectedAnchor.click()
            self.clickElementWhenClickable(selectedAnchor, "//a[starts-with(@href, '/en/')]")

            # time.sleep(random.choice(range(5, 8)))
            if(random.choice(range(0, 10)) >= 7):
                self.__clickAResult()
        except Exception:
            return
        
    def __scrollToElement(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @staticmethod
    def __getRandomString(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
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

