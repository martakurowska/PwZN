import argparse
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

parser = argparse.ArgumentParser(description="This script scrapes")
parser.add_argument("f", help="Name of file", type=str)
args = parser.parse_args()

options = Options()
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

fc = "52.348952:20.942986"
tc = "52.219780:21.015305"

day = datetime.date.today().strftime("%d.%m.%Y")[:6]+datetime.date.today().strftime("%d.%m.%Y")[8:]
hour = datetime.datetime.now().strftime("%H:%M")

# day = "12.11.21"  # DD.MM.YY
# hour = "10:00"  # HH:MM

ia = "false"  # "true" if hour means on time, "false" if hour means departure

url = f"https://jakdojade.pl/warszawa/trasa/?fc={fc}&tc={tc}&d={day}&h={hour}&ia={ia}&t=1"

driver.get(url)
time.sleep(2)
button1 = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div/div[6]/button[2]")))
button1.click()
button2 = driver.find_element(By.XPATH, "//*[@id=\"cn-planner\"]/div[1]/div/div[2]/div[2]/button[2]")
button2.click()
time.sleep(3)

lst = []

elements = driver.find_element(By.XPATH, "//*[@id=\"cn-planner\"]/div[3]/div/div[2]/div/div[1]").find_elements(By.CSS_SELECTOR, "div.cn-vehicle-info")

for e in elements:
    vehicles = e.find_elements(By.CSS_SELECTOR, "div.route-vehicles > div > div")
    r = [v.text for v in vehicles]
    route = " + ".join(r)
    departure = e.find_element(By.CSS_SELECTOR, "div.cn-departure-time > div.ng-scope.cn-route-transport.cn-first-stop > span.cn-time-container.ng-scope").text
    arrival = e.find_element(By.CSS_SELECTOR, "div.cn-departure-time > div.ng-scope.cn-route-transport.cn-end-route").text
    dic = {"vehicles": route, "departure": departure, "arrival": arrival}
    lst.append(dic)

driver.close()

with open(f"{args.f}.json", "w", encoding="utf-8") as f:
    json.dump(lst, f)
