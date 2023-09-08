# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import time

from Bet import Bet


def get_elements(driver1, url_, identifier_elements, name):
    driver1.get(url_)
    driver1.get(url_)
    time.sleep(10)
    elements = driver1.find_elements(identifier_elements, name)
    return elements


def get_bets_efbet(elements_efbet_):
    bets = []
    for i in range(0, len(elements_efbet_)):
        element = elements_efbet_[i]
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


def get_bets_winbet(elements_winbet_):
    bets = []
    for i in range(0, len(elements_winbet_)):
        element = elements_winbet_[i]
        els = element.text.split('\n')
        dates = els[2].split()
        if len(dates) > 2:
            date = els[2].split()[1]
        else:
            date = els[2].split()[0]

        team1 = els[0].split()[0].lower()
        team2 = els[1].split()[0].lower()
        coef1 = els[4]
        coefe = els[5]
        coef2 = els[6]
        bet = Bet(date, team1, team2, coef1, coefe, coef2)
        bets.append(bet)
    return bets


def is_float(string):
    try:
        # float() is a built-in function
        float(string)
        return True
    except ValueError:
        return False


def find_best_bets(bets_1, bets_2):
    bets_1.sort(key=lambda x: (x.team1, x.team2, x.date))
    bets_2.sort(key=lambda x: (x.team1, x.team2, x.date))
    i = 0
    k = 0
    bestods = []
    while i != len(bets_1) and k != len(bets_2):
        efbet_bet = bets_1[i]
        winbet_bet = bets_2[k]
        if not is_float(winbet_bet.coef1):
            k += 1
            continue
        if efbet_bet == winbet_bet:
            bestods.append(Bet(efbet_bet.date, efbet_bet.team1, efbet_bet.team2, max(efbet_bet.coef1, winbet_bet.coef1),
                               max(efbet_bet.coefequal, winbet_bet.coefequal), max(efbet_bet.coef2, winbet_bet.coef2)))
            i += 1
            k += 1
        elif efbet_bet > winbet_bet:
            bestods.append(winbet_bet)
            k += 1
        else:
            bestods.append(efbet_bet)
            i += 1

    if i == len(bets_1):
        while k != len(bets_2):
            bestods.append(bets_2[k])
            k += 1

    if k == len(bets_2):
        while i != len(bets_1):
            bestods.append(bets_1[i])
            i += 1

    bestods.sort(key=lambda x: 1 / float(x.coef1) + 1 / float(x.coef2) + 1 / float(x.coefequal))
    bestods.reverse()
    return bestods


import winsound

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        # TODO Get all the matches for the current days
        # Probably just changing the url and some little bit of tweaking should work

        # Get all the bets from efbet
        # TODO Make a class for getting them

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options=chrome_options)

        url_efbet = 'https://www.efbet.com/BG/sports#bo-navigation=474582.1,475410.1,475411.1&action=market-group-list'
        elements_efbet = get_elements(driver, url_efbet, By.TAG_NAME, 'tr')
        bets_efbet_0margin = get_bets_efbet(elements_efbet)

        url_efbet = 'https://www.efbet.com/BG/sports#bo-navigation=282241.1&action=market-group-list'
        elements_efbet = get_elements(driver, url_efbet, By.TAG_NAME, 'tr')
        bets_efbet = get_bets_efbet(elements_efbet)

        # Get all the bets from winbet
        bets_winbet = []

        url_winbet_bulg = ('https://winbet.bg/sports/tournament?sportIds=soccer-19000000247,19000000007,19000001135,'
                           '19000040249,19000000480,19000000384,19000034480,19000000679')
        elements_winbet = get_elements(driver, url_winbet_bulg, By.XPATH, '//div[@class=\'d-flex event__wrapper\']')
        bets_winbet_bulg = get_bets_winbet(elements_winbet)

        bets_winbet.extend(bets_winbet_bulg)

        url_winbet_england = ('https://winbet.bg/sports/tournament?sportIds=soccer-19000000173,19000000025,19000000024,'
                              '19000000018,19000000019,19000000021,19000000017')
        elements_winbet = get_elements(driver, url_winbet_england, By.XPATH, '//div[@class=\'d-flex event__wrapper\']')
        bets_winbet_england = get_bets_winbet(elements_winbet)

        bets_winbet.extend(bets_winbet_england)

        url_winbet_germ_spain = (
            'https://winbet.bg/sports/tournament?sportIds=soccer-19000034834,19000000054,19000000329,'
            '19000000008,19000000491,19000000044,19000000217,19000000035')
        elements_winbet = get_elements(driver, url_winbet_germ_spain, By.XPATH,
                                       '//div[@class=\'d-flex event__wrapper\']')
        bets_winbet_germ_spain = get_bets_winbet(elements_winbet)

        bets_winbet.extend(bets_winbet_germ_spain)

        url_winbet_0margin = 'https://winbet.bg/sports/accents/1236'
        elements_winbet = get_elements(driver, url_winbet_0margin, By.XPATH, '//div[@class=\'d-flex event__wrapper\']')
        bets_winbet_0margin = get_bets_winbet(elements_winbet)

        # # Get all the bets from betano
        # url_betano = ('https://winbet.bg/sports/tournament?sportIds=soccer-19000034834,19000000054,19000000329,'
        #                          '19000000008,19000000491,19000000044,19000000217,19000000035')
        # elements_winbet = get_elements(url_winbet_germ_spain, By.XPATH, '//div[@class=\'d-flex event__wrapper\']',
        #                                By.CLASS_NAME,
        #                                'accordion accordion--level-1 accordion--level-1--open')
        # bets_winbet_germ_spain = get_bets_winbet(elements_winbet)

        # for bet in bets_efbet:
        #     print(str(bet))
        #
        # print('--------------------')
        #
        # for bet in bets_winbet:
        #     print(str(bet))

        driver.quit()
        bestods1 = find_best_bets(bets_efbet, bets_winbet)

        # bestods2 = find_best_bets(bestods1, bets_efbet_0margin)
        #
        # bestods3 = find_best_bets(bestods2, bets_winbet_0margin)

        w = 1
        for odd in bestods1:
            print(w, end='')
            print('. | ', end=' ')
            print(str(odd), end=' ')
            print(
                'Profit:' + str(-(1 / float(odd.coef1) + 1 / float(odd.coef2) + 1 / float(odd.coefequal)) * 100 + 100))
            w += 1

        best_odd = bestods1[len(bestods1) - 1]
        if -(1 / float(best_odd.coef1) + 1 / float(best_odd.coef2) + 1 / float(best_odd.coefequal)) * 100 + 100 > 0.5:
            frequency = 2500
            duration = 1000
            winsound.Beep(frequency, duration)

        time.sleep(300)
