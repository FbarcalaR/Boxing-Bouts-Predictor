# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 10:01:10 2020

@author: OHyic
"""

#system libraries
import os
import random
import time

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

import mouseMovementMaker

class RecaptchaSolver:
    
    def __init__(self, userName, password, loginLink):
        ## maybe (executable_path=r'your\path\geckodriver.exe') is nos necessary
        self.driver = None
        self.userName = userName
        self.password = password
        self.loginLink = loginLink
        self.tryNumber = 1
        self.mouseMovement = mouseMoventMaker.MouseMoventMaker()
    
    def solveRecaptcha(self):
        try:
            self.__getFirefoxSession()
            self.__login()

            self.__switchToRecaptchaFrame()
            self.__clickOnCheckBox()

            self.driver.switch_to.default_content()
            divContainingFrames = self.__switchToRecaptchaAudioControlFrame()

            self.__clickOnAudioChallenge()
            self.__switchToRecaptchaAudioChallengeFrame()

            self.__solveAudio()

            while(len(divContainingFrames)>0):
                divContainingFrames = self.__switchToRecaptchaAudioControlFrame()
                if(divContainingFrames == None):
                    continue
                self.__solveAudio()
            
            self.tryNumber = 1
            self.driver.quit()
        except Exception:
            print("Seems like the captcha needs a cooldown")
            print("\tSleeping for " + str(600 * self.tryNumber)+ " seconds")
            self.driver.quit()

            time.sleep(600 * self.tryNumber)
            self.tryNumber += 1
            self.solveRecaptcha()

    def __getFirefoxSession(self):
        self.driver = webdriver.Firefox(executable_path='C:\\Python\\geckodriver.exe')
        self.__delay()

    def __login(self):
        self.driver.get(self.loginLink)

        userNameElem = self.driver.find_element_by_id('username')
        self.mouseMovement.moveMouse(userNameElem)
        userNameElem.send_keys(self.userName)

        passwordElem = self.driver.find_element_by_id('password')
        self.mouseMovement.moveMouse(passwordElem)
        passwordElem.send_keys(self.password)
        
        loginSubmitElement = self.driver.find_element_by_name("login[go]")
        loginSubmitElement.click()

    def __switchToRecaptchaFrame(self):
        frames=self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[0]);
        self.__delay()

    def __clickOnCheckBox(self):
        recaptchaCheckBoxElement = self.driver.find_element_by_class_name("recaptcha-checkbox-border")
        self.mouseMovement.moveMouse(recaptchaCheckBoxElement)
        recaptchaCheckBoxElement.click()

    def __switchToRecaptchaAudioControlFrame(self):
        divContainingFrames = self.driver.find_elements_by_xpath("/html/body/div[2]/div[4]")
        if(len(divContainingFrames)==0):
            return None
        frames = divContainingFrames[0].find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[0])
        self.mouseMovement.moveMouse(frames[0])
        return divContainingFrames
        
    def __clickOnAudioChallenge(self):
        recaptachAudioButtonElement = self.driver.find_element_by_id("recaptcha-audio-button")
        self.mouseMovement.moveMouse(recaptachAudioButtonElement)
        recaptachAudioButtonElement.click()

    def __switchToRecaptchaAudioChallengeFrame(self):
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements_by_tag_name("iframe")
        self.driver.switch_to.frame(frames[-1])
        self.mouseMovement.moveMouse(frames[-1])

    def __solveAudio(self):
        playButton = self.driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button")
        playButton.click()

        mp3AudioSegment = self.__downloadMp3()
        wavAudio = self.__convertMp3ToWav(mp3AudioSegment)
        
        key = self.__getAudioKey(wavAudio)

        audioInputElement = self.driver.find_element_by_id("audio-response")
        self.mouseMovement.moveMouse(audioInputElement)
        self.__enterKeyAndSubmit(audioInputElement, key)

    def __downloadMp3(self):
        mp3FileElement = self.driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s"%mp3FileElement)
        #download the mp3 audio file from the source
        urllib.request.urlretrieve(mp3FileElement, "\\sample.mp3")
        mp3AudioSegment = pydub.AudioSegment.from_mp3("\\sample.mp3")
        return mp3AudioSegment

    def __convertMp3ToWav(self, mp3AudioSegment):
        mp3AudioSegment.export("\\sample.wav", format="wav")
        wavAudio = sr.AudioFile("\\sample.wav")
        return wavAudio

    def __getAudioKey(self, wavAudio):
        recognizer = sr.Recognizer()

        with wavAudio as source:
            audio = recognizer.record(source)

        key=recognizer.recognize_google(audio)
        print("[INFO] Recaptcha Passcode: %s"%key)
        return key
        
    def __enterKeyAndSubmit(self, audioInputElement, key):
        audioInputElement.send_keys(key.lower())
        audioInputElement.send_keys(Keys.ENTER)
        self.driver.switch_to.default_content()
        self.__delay()





    @staticmethod
    def __delay ():
        time.sleep(random.randint(4,6))
    