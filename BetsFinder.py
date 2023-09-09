import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Bet import Bet


def transform_into_bets_efbet_football(elements):
    bets = []
    for i in range(0, len(elements)):
        element = elements[i]
        els = element.text.split('\n')
        if len(els) < 6:
            continue
        date = els[1]
        team1 = els[2].split('vs')[0].split()[0].lower()
        team2 = els[2].split('vs')[1].split()[0].lower()
        coef1 = els[3]
        coefe = els[4]
        coef2 = els[5]
        bet = Bet(date, team1, team2, coef1, coefe, coef2)
        bets.append(bet)
    return bets


def transform_into_bets_efbet_today(elements):
    bets = []
    for i in range(0, len(elements)):
        element = elements[i]
        # print(element.text)
        # print('----------------')
        els = element.text.split('\n')
        if len(els) < 7 or els[0] == '<' or els[len(els) - 1] == '>':
            continue
        date = els[0]
        team1 = els[1].split()[0].lower()
        team2 = els[3].split()[0].lower()
        coef1 = els[4]
        if len(els) == 7:
            coefe = '-1'
            coef2 = els[5]
        else:
            coefe = els[5]
            coef2 = els[6]
        bet = Bet(date, team1, team2, coef1, coefe, coef2)
        bets.append(bet)
    return bets


def get_elements(driver, url_, identifier_elements, name):
    driver.get(url_)
    driver.get(url_)
    time.sleep(10)

    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    # WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions) \
    #     .until(expected_conditions.presence_of_element_located((identifier_elements, name)))

    elements = driver.find_elements(identifier_elements, name)
    return elements


class BetsFinder:
    def __init__(self, driver):
        self.driver = driver

    def get_efbet_bets_football(self, url, identifier_elements, name):
        elements = get_elements(self.driver, url, identifier_elements, name)
        bets = transform_into_bets_efbet_football(elements)
        return bets

    def get_efbet_bets_today(self, url, identifier_elements, name):
        elements = get_elements(self.driver, url, identifier_elements, name)
        bets = transform_into_bets_efbet_today(elements)
        return bets
