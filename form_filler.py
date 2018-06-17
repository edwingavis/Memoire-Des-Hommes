#FRENCH NOTES: KOREA HAS 288 CASUALTIES
#INDOCHINA HAD 39000 CASUALTIES??? <---SURE SEEMS LIKE IT...
#Could be another 300000 in algeria

from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time as systime
import string
import progressbar

alphabet = list(string.ascii_lowercase)
war_link = {
	"indochina": "http://www.memoiredeshommes.sga.defense.gouv.fr/en/arkotheque/client/mdh/guerre_indochine/index.php",
	"korea": "http://www.memoiredeshommes.sga.defense.gouv.fr/en/arkotheque/client/mdh/guerre_coree_militaires_bf_onu/",
	"algeria": "http://www.memoiredeshommes.sga.defense.gouv.fr/en/arkotheque/client/mdh/guerre_algerie_combats_maroc_tunisie/"
	}
	
in_fail_set = {("a","b"), ("b","a"), ("b","j"), ("b","m"), ("b","r"),
               ("l","j"), ("m","a"), ("m","b"), ("m","j"), ("m","m"),
               ("m", "be")}#, ("m", "ben")} 

al_fail_set = {("b","a"), ("b","j"), ("b","m"), ("b","r"), ("c","j"), 
               ("l","j"), ("m","a"), ("m","j"), ("m","m")}

war_fail_dict = {"algeria": al_fail_set, "indochina": in_fail_set, "korea": {}}

def run_initial_scrape(war, sur_list = alphabet, given_pre = [], rescrape = False):
	caps = DesiredCapabilities().FIREFOX
	caps["marionette"] = True
	caps["pageLoadStrategy"] = "eager"
	failures = []
	driver = webdriver.Firefox(capabilities = caps)
	for count, a in enumerate(sur_list):
		bar = progressbar.ProgressBar()
		for b in bar(alphabet):
			if rescrape: 
				b = given_pre[count] + b 
			if (a,b) in war_fail_dict[war]:
			    continue
			driver.get(war_link[war])
			nom = driver.find_element_by_name("r_c_nom")
			nom.send_keys(a)
			prenom = driver.find_element_by_name("r_c_prenom")
			prenom.send_keys(b)
			submit = driver.find_element_by_css_selector("a[class='rechercher']")
			submit.click()
			try:
				all_pg = driver.find_element_by_link_text('All')
				all_pg.click()
			except:
				systime.sleep(1)
				continue
			page_source = driver.page_source
			if "only the first 300" in page_source:
				failures.append(a + b)
			soup = BeautifulSoup(page_source, "lxml")
			#WRITE TO TEXT FILE...
			file_ = war + "/html/" + a + b + ".html" 
			with open(file_, "w") as file__:
				file__.write(str(soup))
	driver.close()
	print (failures)

def re_scrape(war):
	sur_list = []
	given_list = []
	for pair in war_fail_dict[war]:
		sur_list.append(pair[0])
		given_list.append(pair[1])
	run_initial_scrape(war, sur_list, given_list, True)

#test()
#run_initial_scrape("indochina")
re_scrape("indochina")

''' 
day = driver.find_element_by_id("id_r_c_naissance_jour_mois_annee_jj_debut")
month = driver.find_element_by_id("r_c_naissance_jour_mois_annee_mm_debut")
year = driver.find_element_by_id("r_c_naissance_jour_mois_annee_yyyy_debut")
day.send_keys("01")
month.send_keys("02")
year.send_keys("1950")
day.submit
'''

