# Import your newly installed selenium package
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def jamedaSearch(doctor_discipline, city_name):
	driver = webdriver.Chrome("C:/Users/hasan/Downloads/chromedriver.exe") #Path to webdriver
	#loading web page
	driver.get('https://www.jameda.de/search/');
	time.sleep(1) #selenium recommends puffer time > 0

	#filling out form (what/where) 
	elem1 = driver.find_element_by_xpath('//*[@id="what"]')
	actions = webdriver.ActionChains(driver)
	actions.move_to_element(elem1)
	actions.click()
	actions.send_keys(doctor_discipline)
	actions.perform()

	elem2 = driver.find_element_by_xpath('//*[@id="where"]')
	actions = webdriver.ActionChains(driver)
	actions.move_to_element(elem2)
	actions.click()
	actions.send_keys(city_name)
	actions.perform()

	element = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div[2]/div/header/div[2]/div/form/button')
	element.click()
	time.sleep(1)

	#getting the url
	url = driver.current_url
	driver.quit()
	return url

def getProfilLinks(link):
	
	driver = webdriver.Chrome("C:/Users/hasan/Downloads/chromedriver.exe")  # Optional argument, if not specified will search path.
	#loading web page
	driver.get(link);
	time.sleep(1)

	#click in order to close the overlay
	element = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/button')
	element.click()
	time.sleep(1)

	#if more results than 30 available click to load more 
	try:
		element1 = driver.find_element_by_xpath('.//*[@id="app"]/div/div/div[3]/div[2]/div[2]/div[3]/div[2]/button/span[2]')
		element1.click()
		time.sleep(1)
	except:
		pass

	#try again (jameda.de will not load more than 30 + 30 + 30 profiles)
	try:
		element1.click()
		time.sleep(1)
	except:
		pass

	#all profile links appear twice on the webpage but only one is needed 
	profil_links = []
	ungerade = True
	for a in driver.find_elements_by_xpath('.//h2/a'):
		if ungerade == True:
			profil_links.append(a.get_attribute('href'))
			ungerade = False
		else: ungerade = True

	#in this file many duplicates appear because jameda.de searches inaccurate (searching for doctors in 10115 Berlin shows also         doctors who are located in 10117 Berlin)
	#but scrapy filters them later automatically
	with open('profil_links.txt', 'a') as the_file:
		for line in profil_links:
			the_file.write(str(line) + '\n')
	the_file.close()
	driver.quit()

link = jamedaSearch('augenaerzte','berlin')
print(link)
getProfilLinks(link)
