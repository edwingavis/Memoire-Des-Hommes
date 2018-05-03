import bs4
import progressbar
import time as systime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#BUILT-INS: 
import collections
import re
import os
import csv
import sys

columns = (
	"surname", 
	"given_name", 
	"status",
	"rank",
	"unit", 
	"date_death", 
	"place_death", 
	"country_death",
	"cause_of_death",
	"main_battles",
	"date_birth",
	"place_birth",
	"place_of_transcription_of_death",
	"place_of_burial",
	"recruitment_office",
	"recruitment_roll_number",
	"class",
	"document_reference",
	"reference",
	"sources",
	)

def get_links(files, war):
	'''
	takes the links from the given filenames (in <war>/html) and writes them to files 
	one line per link and starts a new file every 1k, with final segment being tucked into last file 
	even if sub-1k 
	files are in <war>/links/ with names like links1_s1000.txt  
	'''
	count = 1
	links = []
	last = False 
	bar = progressbar.ProgressBar()
	for filename in bar(files):
		if filename == files[-1]:
			last = True
		html = open(war + "/html/" + filename).read()
		soup = bs4.BeautifulSoup(html, "lxml")
		permas = soup.find_all("a", title = "Access to permalink")
		for link in permas:
			links.append(link['href'])
			if len(links) >= 1000 or (last and link == permas[-1]):
				with open(war + "/links/links" + str(count) + "_" + str(count+1000) +".txt" ,"w") as f:
					for link in links:
						f.write(link + "\n")
				links = []
				count += 1000

def scrape_links(links, war):
	'''
	links: list of links (strings)
	war: the war (string)
	'''
	count = len(get_file_names(war)) + 1
	print(count)
	caps = DesiredCapabilities().FIREFOX
	caps["marionette"] = True
	caps["pageLoadStrategy"] = "eager"
	driver = webdriver.Firefox(capabilities = caps)
	bar = progressbar.ProgressBar()
	###
	if sys.argv[2]:
	    links = links[sys.argv[2]:] #USE IF BREAKS IN MIDDLE, SET LIKE: [last:]
	###
	for link in bar(links):
		try:
			driver.get(link)
		except:
			continue
		#systime.sleep(2)
		html = driver.page_source
		new_file = war + "/details/" + war + str(count)
		with open(new_file, "w") as file_:
			file_.write(str(html))
		count += 1
		#systime.sleep(5)
	driver.close()

def get_data_from_files(files, war):
	'''
	inputs: list of html filenames as strings (full path from wd)
	ouputs: list of dictionaries of vital info
	'''
	rv = []
	print("\nPulling data from files")
	bar = progressbar.ProgressBar()
	for filename in bar(files):
		html = open(war + "/details/" + filename).read()
		soup = bs4.BeautifulSoup(html, "lxml")
		content = soup.findAll("div", {"class": "champ_formulaire"})
		info = collections.defaultdict(str)
		for c in content:
			key = c.label.text.lower().replace(" ", "_")
			info[key] = c.span.text
		name = soup.find("h1")
		if name:
			info["given_name"] = re.split("[A-Z][A-Z]+", name.text)[0].strip(" ")
			info["surname"] = re.split("[a-z]+", name.text)[-1].strip(" é")
		birth = soup.find("h4")
		if birth:
			dob = re.search("[0-9]+[0-9-]*", birth.text)
			if dob:
				info["date_birth"] = dob.group(0)
			fr_birth = re.search("à [\w()\- ]+", birth.text)
			if fr_birth:
				info["place_birth"] = fr_birth.group(0).split("(", 1)[0].strip("à\(\) ")
			else: 
				nf_birth = re.search("\(\w\w[\w)]+", birth.text)
				if nf_birth:
					info["place_birth"] = nf_birth.group(0).strip("()")
		death = soup.find("h3")
		if death:
			date_death = re.search("[0-9]+[0-9-]*", death.text)
			if date_death: 
				info["date_death"] = date_death.group(0)
			p_d = re.search("\([A-Z].+\)", death.text)
			if p_d:
				try:
					p_d_p, p_d_c = p_d.group(0).strip("()").split(",", 1)
				except:
					p_d_c = p_d.group(0).strip("()")
					p_d_p = ""
				info["place_death"] = p_d_p
				if re.search("France", p_d_c):
					info["country_death"] = "France"
				else:
					info["country_death"] = p_d_c.strip(" ") 
		rv.append(info)
	return rv

def write_csv(details, filename):
	'''
	inputs: 
	    details: list of dictionaries
	    filename: filename as str()
	outputs:
	    filename.csv w/ details
	'''
	with open(filename +'.csv', 'w') as csvfile:
	    spamwriter = csv.writer(csvfile, dialect='excel')
	    spamwriter.writerow(columns)
	    for d in details:
	    	row = [d[key] for key in columns]
	    	spamwriter.writerow(row)

def get_file_names(war, folder = "details"):
	'''
	'''
	files = os.listdir(war + "/" + folder)
	def natural_key(string_):
		return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
	return sorted(files, key = natural_key)

def read_links(war, i):
	'''
	'''
	link_names = get_file_names(war, "links")
	print(str(i) +  "/" + str(len(link_names)))
	with open(war + "/links/" + link_names[i], "r") as f:
		return f.read().split("\n")

#USE THIS TO SET WHICH WAR IT IS
war = "indochina" #"korea", "algeria", "indochina"

#USE THIS TO GET THE LINKS FROM THE INITIAL HTML
names = get_file_names(war, "html")
get_links(names, war)

#DO SCRAPING, MANUALLY INCREMENT... 0 - n --- 29 total...
#links = read_links(war, int(sys.argv[1])) #3
#scrape_links(links, war)

#USE THIS TO CREATE THE FINAL CSV
#names = get_file_names(war)
#data = get_data_from_files(names, war)
#write_csv(data, war)

##NOTE FOR INDOCHINA:
#place of birth in form "ne le/en date a Place (Region) (Country)"