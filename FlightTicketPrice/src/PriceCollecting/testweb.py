'''
Created on Jan 13, 2020
@author: K
'''
import time
#import selenium as se
from selenium import webdriver
import re
import pandas as pd
import PriceCollecting.FlightPriceCollecting

flightype = ['roundTrip','oneWay']
fromto = ['origin_O_0', 'destination_O_0']
#op = webdriver.ChromeOptions()
driver = webdriver.Chrome('D:\\PersonalDoc\\PythonProjects\\FlightTicketPrice\\ChromeDriver\\chromedriver.exe')
driver.get('https://www.google.ca/flights?lite=0#flt=YYZ.TNA.2020-04-18;c:CAD;e:1;px:2;sd:1;t:f;tt:o')
driver.maximize_window()
time.sleep(5)

#for conts in driver.find_elements_by_xpath('//div[@class="gws-flights-results__itinerary-card gws-flights-results__result-item-content gws-flights__flex-filler gws-flights-widgets-expandablecard__card gws-flights-widgets-expandablecard__elevation-1"]')[:3]:
flightcom = []
flyinghour = []
flightstops = []
flightprice = []

reslist = pd.DataFrame(columns=['company', 'hours', 'stops', 'price'])

for company in driver.find_elements_by_xpath('//span[@class="gws-flights__ellipsize"]'):
    if (company.text != ''):
        flightcom.append(company.text)

for hours in driver.find_elements_by_xpath('//div[@class="gws-flights-results__duration flt-subhead1Normal"]'):
    if (hours.text != ''):
        flyinghour.append((hours.text).replace(' h ', ':')[:5])

for stops in driver.find_elements_by_xpath('//div[@class="gws-flights-results__itinerary-stops gws-flights__ellipsize"]'):
    if (stops.text[:7] != ''):
        flightstops.append(stops.text[:1])

for price in driver.find_elements_by_xpath('//div[@class="gws-flights-results__itinerary-price"]'):
    if (price.text != ''):
        if((price.text).replace(',', '')[1:].isdigit()):
            flightprice.append((price.text).replace(',', '')[1:])
        else:
            flightprice.append('0')

print(flightcom)
print(flyinghour)
print(flightstops)
print(flightprice)
#print(reslist)

time.sleep(1)
#driver.close()
exit()
#driver.find_element_by_id('enCAEdition').click()

#driver.find_element_by_id('oneWay').click()
#driver.find_element_by_id('origin_O_0').clear()
# driver.find_element_by_id('origin_O_0').send_keys('Toronto-Pearson Int.')
# time.sleep(0.5)
# driver.find_element_by_id('flightLocationListOrginId0').click()
# #driver.find_element_by_class_name('location-wrapper-airport').click()
# #driver.find_element_by_id('flightLocationListOrginId0_locationListItem_0').click()
# driver.find_element_by_id('destination_O_0').clear()
# driver.find_element_by_id('destination_O_0').send_keys('Beijing Capital Int.')
# time.sleep(0.5)
# driver.find_element_by_id('flightLocationListDestinationId0').click()
# #driver.find_element_by_class_name('location-wrapper-airport').click()
# #driver.find_element_by_id('flightLocationListDestinationId0_locationListItem_0').click()
# time.sleep(3)
#time.sleep(0.5)
#driver.find_element_by_id('fligthDepartureDate').click()

#driver.find_elements_by_class_name('managed-wrapper supplementary-wrapper row single-line-date col-sm-4 new-calendar-wrapper')

#driver.find_element_by_class_name('')
