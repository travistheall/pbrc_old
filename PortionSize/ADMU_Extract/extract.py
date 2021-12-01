from selenium import webdriver
import json
import urllib.request
import pandas as pd
import time
import os

driver = webdriver.Chrome('chromedriver')
driver.get("https://admu2.pbrc.edu/")

SummariesDF = pd.DataFrame()
FoodPhotoEventDF = pd.DataFrame()
FoodPhotoEventPortionsDF = pd.DataFrame()
AfterPhotoEventDF = pd.DataFrame()
AfterPhotoEventTheLeftoversDF = pd.DataFrame()
ForgotMealsDF = pd.DataFrame()
ForgotMealPortionsDF = pd.DataFrame()
SettingsDF = pd.DataFrame()
AfterPhotoAteEverythingEventDF = pd.DataFrame()

subjectChoices = {
    'IntakeDaySummary': SummariesDF,
    'SelectionDaySummary': SummariesDF,
    'Food-Photo Event': FoodPhotoEventDF,
    'AfterPhotoAteEverything Event': AfterPhotoAteEverythingEventDF,
    'AfterPhotoLeftovers Event': AfterPhotoEventDF,
    'ForgotMeal Event': ForgotMealsDF,
    'Onboarding Event': SettingsDF,
    'Settings Event': SettingsDF,
}

participantElements = driver.find_elements_by_xpath(
    '//*[@id="ctl00_ContentPlacenHolderPageDescription_btcLocation_ulTreeView"]/li/ul/li/a')
numberOfParticipants = len(participantElements)  # use this number for loop
skip = ['A00-05-6637', 'Fake1', 'jfnfnf', 'Test 1', 'Test 2']
for participantElem in range(len(participantElements)):
    participantElements = driver.find_elements_by_xpath(
        '//*[@id="ctl00_ContentPlacenHolderPageDescription_btcLocation_ulTreeView"]/li/ul/li/a')
    if participantElements[participantElem].text in skip:
        pass
    else:
        participantElements[participantElem].click()
        time.sleep(10)
        pageElement = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlacenHolderPageDescription_lblCurrentPage"]')
        participantANumElement = driver.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlacenHolderPageDescription_lblSubject"]')
        ANum = participantANumElement.text
        pages = int(pageElement.text.split(' ')[-1])

        for page in range(pages):
            allCardElements = driver.find_elements_by_xpath(
                '/html/body/form/div[3]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div')
            numOfCards = len(allCardElements)
            for card in range(1, numOfCards + 1):
                cardSubject = driver.find_element_by_xpath(
                    f'/html/body/form/div[3]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[{card}]/div/div[3]/div/div[2]/div/div[2]/input').get_attribute(
                    'value')
                cardBody = json.loads(driver.find_element_by_xpath(
                    f'/html/body/form/div[3]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[{card}]/div/div[3]/div/div[3]/textarea').text)
                cardTitle = driver.find_element_by_xpath(
                    f'/html/body/form/div[3]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[{card}]/div/div[1]/h5/span').text
                if cardTitle != 'NoPhoto.jpg':
                    img = driver.find_element_by_xpath(f'/html/body/form/div[3]/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[{card}]/div/div[2]/div/div[1]/a/img')
                    src = img.get_attribute('src')
                    try:
                        os.mkdir(f"photos/{ANum}/")
                    except OSError:
                        pass
                    urllib.request.urlretrieve(src, f"photos/{ANum}/{cardTitle}")
                    cardBody['Image'] = f"photos/{ANum}/{cardTitle}"

                if len(subjectChoices[cardSubject].columns) == 0:
                    subjectChoices[cardSubject] = pd.DataFrame(columns=list(cardBody.keys()))

                subjectChoices[cardSubject] = subjectChoices[cardSubject].append(
                    pd.DataFrame(data=list(cardBody.values())).transpose())

            driver.find_element_by_xpath('// *[ @ id = "ctl00_ContentPlacenHolderPageDescription_btnNextPage"]').click()
            time.sleep(10)

subjectChoices['IntakeDaySummary'].to_excel('data/raw_extract/IntakeDaySummary.xlsx')
subjectChoices['SelectionDaySummary'].to_excel('data/raw_extract/SelectionDaySummary.xlsx')
subjectChoices['Food-Photo Event'].to_excel('data/raw_extract/Food-Photo Event.xlsx')
subjectChoices['AfterPhotoAteEverything Event'].to_excel('data/raw_extract/AfterPhotoAteEverything Event.xlsx')
subjectChoices['AfterPhotoLeftovers Event'].to_excel('data/raw_extract/AfterPhotoLeftovers Event.xlsx')
subjectChoices['ForgotMeal Event'].to_excel('data/raw_extract/ForgotMeal Event.xlsx')
subjectChoices['Onboarding Event'].to_excel('data/raw_extract/Onboarding Event.xlsx')
# Adjusted the column headers to be correct
