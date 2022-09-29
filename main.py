from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

XPATHNEXTBUTTON = '//*[@id="scrollable-auto-tabpanel-0"]/div/p/div[3]/div/div[1]/nav/ul/li[9]/button'

# satu baris ada 6 kolom
# link ada di kolom ketiga
LIMITPERPAGE = 10
INDEXLINK = [2, 8, 14, 20, 26, 32, 38, 44, 50, 56]
INDEXSECTOR = [3, 9, 15, 21, 27, 33, 39, 45, 51, 57]

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('start-maximized')
browser = webdriver.Chrome("chromedriver", options=options)
browser.get("https://pse.kominfo.go.id/home/pse-domestik")


def checkExistByXpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except:
        return False
    return True


def goToTheNextPage():
    element = browser.find_element(By.XPATH, XPATHNEXTBUTTON)
    browser.execute_script('arguments[0].scrollIntoView();', element)
    browser.execute_script('window.scrollBy(0, -200);')
    element.click()


def collectUrl():
    html = browser.page_source
    soup = BeautifulSoup(html, features='html.parser')
    tds = soup.find_all('td')
    with open('result.txt', 'a') as file:  
        for i in range(LIMITPERPAGE):
            link = tds[INDEXLINK[i]].contents[0]
            sektor = tds[INDEXSECTOR[i]].contents[0]
            row = link + "," + sektor + "\n"
            file.write(row)

isOtherNextPage = True
page = 1
while isOtherNextPage:
    isOtherNextPage = checkExistByXpath(browser, XPATHNEXTBUTTON)
    goToTheNextPage()
    sleep(2)
    collectUrl()

browser.close()