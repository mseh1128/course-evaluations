import requests
from bs4 import BeautifulSoup as soup
from bs4 import SoupStrainer as strainer
import threading
import sqlite3
import re
import json

def number_of_urls(num_of_elements):
	url_amount = 0
	while num_of_elements > 0:
		num_of_elements -= 10
		url_amount += 1
	return url_amount


def url_list(element_number):
	num_of_urls = number_of_urls(element_number)
	urls = set()
	for i in range(1, num_of_urls + 1):
		urls.add(my_url + "&page=" + str(i))
	return urls


def standardize_professor_name(name_of_profs):
	stand_professor_names = list(name_of_profs)
	for idx, name in enumerate(stand_professor_names):
		temp_name = name.split(",")
		# Removes Middle Name
		temp_name[1] = temp_name[1].split(" ")[0]
		stand_professor_names[idx] = temp_name
	return stand_professor_names


def rate_my_professor_name(prof_name):
	my_url = "http://www.ratemyprofessors.com/search.jsp?query=" + prof_name[0] + "+" + prof_name[1]
	page_html = requests.get(my_url)
	page_soup = soup(page_html.content, "lxml")
	all_names = page_soup.find_all("li", {"class": "listing PROFESSOR"})
	temporary_name = prof_name[0] + ", " + prof_name[1]
	for present_name in all_names:
		name_text = present_name.find("span", {"class": "sub"}).text
		if "Stony Brook University (SUNY)" in name_text:
			url_suffix = present_name.find('a').get('href')
			response = requests.get("http://www.ratemyprofessors.com" + url_suffix)
			if not response.history:
				names_links[temporary_name] = url_suffix
				return
	names_links[temporary_name] = None


# def attributes:
def process_html(url):
	page_html = requests.get(url)
	potential_names = strainer("div", {"class": "resultItemLine2"})
	page_soup = soup(page_html.content, "lxml", parse_only=potential_names)
	containers = page_soup.findAll("a")
	for container in containers:
		if container.text != "TBA":
			professor_names.add(container.text)


def thread_creator(method, all_args):
	if(isinstance(all_args,dict)):
		threads = [threading.Thread(target=method, args=(name_arg,url_arg)) for name_arg,url_arg in all_args.items()]
	else:
		threads = [threading.Thread(target=method, args=(single_arg,)) for single_arg in all_args]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()						

def rmfstats(name, url):
	if (url != None):
		conn = sqlite3.connect('Class Stats.db')
		c = conn.cursor()
		url = "http://www.ratemyprofessors.com" + url
		page_html = requests.get(url)
		required_stats = strainer("div", {"class": "left-breakdown"})
		requied_review_stats = strainer("div", {"class": "table-toggle rating-count active"})
		page_soup = soup(page_html.content, "lxml", parse_only=required_stats)
		reviews_soup = soup(page_html.content, "lxml", parse_only=requied_review_stats)
		quality = re.findall("\d\.\d",page_soup.find("div", {"class":"breakdown-container quality"}).text)[0]
		grade = page_soup.find_all("div",{"class":"breakdown-header"})[1].text
		level_of_hotness = page_soup.find("img")['src']
		reviews = int(re.findall("\d+",reviews_soup.text)[0])
		reviews = re.findall("\d+",reviews_soup.text)[0]
		if "cold-chili" in level_of_hotness:
			level_of_hotness = "Cold"
		elif "new-hot-chili" in level_of_hotness:
			level_of_hotness = "Hot"
		c.execute("UPDATE {} SET Hotness = (?) WHERE Professor_Name = (?)".format(class_name), (level_of_hotness, name))
		difficulty_level = grade.strip().split()[7]
		grade = grade.strip().split()[3]
		if grade != "N/A":
			c.execute("UPDATE {} SET Would_Take_Again = (?) WHERE Professor_Name = (?)".format(class_name), (grade, name))
		c.execute("UPDATE {} SET Level_Of_Difficulty = (?) WHERE Professor_Name = (?)".format(class_name), (difficulty_level, name))
		c.execute("UPDATE {} SET Overall_Quality = (?) WHERE Professor_Name = (?)".format(class_name), (quality, name))
		c.execute("UPDATE {} SET Number_Of_Reviews = (?) WHERE Professor_Name = (?)".format(class_name), (reviews, name))
		conn.commit()

# def sentimentanalysis(dirty_url):
# 	contentOnPage = True
# 	pageNumber = 1
# 	numberOfRatings = 0
# 	while contentOnPage:
# 		url = "http://www.ratemyprofessors.com/paginate/professors/ratings?" + re.search('tid=\d+$',dirty_url).group(0) + "&page=" + str(pageNumber)
# 		page_html = requests.get(url)
# 		print(page_html.json()['remaining'])
# 		print(url)
# 		contentOnPage = False
# 		pageNumber+=1
		

	

# http://www.ratemyprofessors.com/paginate/professors/ratings?tid=520630&page=7

if __name__ == '__main__':
	class_name = input('Enter a class: ').replace(" ", "").upper()
	conn = sqlite3.connect('Class Stats.db')
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS {}'.format('class_name'))
	c.execute('CREATE TABLE IF NOT EXISTS {} (Professor_Name TEXT PRIMARY KEY UNIQUE, URL TEXT, Overall_Quality REAL, Would_Take_Again INTEGER, Level_Of_Difficulty REAL, Hotness TEXT, Number_Of_Reviews INTEGER, Sentiment_Analysis INTEGER)'.format(class_name))
	conn.commit()
	my_url = 'http://classfind.stonybrook.edu/vufind/Search/Results?lookfor=' + class_name + '&type=callnumber&filter%5B%5D=ctrlnum%3A%22Spring+2018%22'
	page_html = requests.get(my_url)
	elementVals = strainer("div", {"class": "floatleft"})
	page_soup = soup(page_html.content, "lxml", parse_only=elementVals)
	numberOfElements = int(page_soup.findAll("strong")[2].text)
	all_urls = url_list(numberOfElements)
	professor_names = set()
	names_links = {}
	thread_creator(process_html, all_urls)
	standarized_prof_names = standardize_professor_name(professor_names)
	print(len(standarized_prof_names))
	print(standarized_prof_names)
	'''
	thread_creator(rate_my_professor_name, standarized_prof_names)
	for key, value in names_links.items():
		c.execute('INSERT OR IGNORE INTO {} (Professor_Name, URL) VALUES (?,?)'.format(class_name), (key, value))
	conn.commit()
	thread_creator(rmfstats, names_links) 
	'''

	# c.execute('SELECT * FROM {} WHERE URL IS NOT NULL'.format(class_name))
	# table = c.fetchone()
	# sentimentanalysis((table[1]))
#	c.execute('"UPDATE {} SET Level_Of_Difficulty = (?) WHERE Professor_Name = (?)".format(class_name), (difficulty_level, name))')
	c.close()
	conn.close()


			# if key == val:
			# 	continue
			# print(key)
# stop it from making another table
# combine repeating values
# http://www.ratemyprofessors.com/paginate/professors/ratings?tid=520630&page=7

	
