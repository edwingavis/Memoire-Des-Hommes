from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib
import time as systime

import urllib.request
link = ""
#with urllib.request.urlopen(link) as response:
#   html = response.read()
#   print(html)
'''
driver = webdriver.Firefox()
driver.get("http://www.memoiredeshommes.sga.defense.gouv.fr/en/arkotheque/client/mdh/guerre_indochine/index.php")
key1 = ""
key2 = "01 - Ain"
dept = driver.find_element_by_id("id_c_id_naissance_departement")
dept.send_keys(key2)
submit = driver.find_element_by_css_selector("a[class='rechercher']")
submit.click()
all_pg = driver.find_element_by_link_text('All')
all_pg.click()
page_source = driver.page_source
soup = BeautifulSoup(page_source, "lxml")
file_ = "indochina/indochina" + key1 + key2.replace(" ","_") + ".html" 
with open(file_, "w") as file__:
	file__.write(str(soup))
#the above lets me search this thing...
day = driver.find_element_by_id("id_r_c_naissance_jour_mois_annee_jj_debut")
month = driver.find_element_by_id("r_c_naissance_jour_mois_annee_mm_debut")
year = driver.find_element_by_id("r_c_naissance_jour_mois_annee_yyyy_debut")
day.send_keys("01")
month.send_keys("02")
year.send_keys("1950")
day.submit
systime.sleep(10)
driver.close()
'''
