'''
Created on Jan 16, 2020
@author: K
Collecting by url
'''

import re
import time
import datetime
from selenium import webdriver
import pandas as pd
import os


class FlightPriceCollecting(object):
    def __init__(self):
        
        self.googleurl = 'https://www.google.ca/flights?lite=0#flt='  ##part of google searching url
        self.ceairurl = 'http://www.ceair.com/booking/a'  ##part of google searching url
        self.CeAirCsvfilepath = '..\\..\\CeAirFlightPriceCNY.csv'  ##destination of ceairflightprice
        self.GoogleCsvfilepath = '..\\..\\GoogleFlightPriceCAD.csv'  ##destination of googleflightprice
        self.browser = webdriver.Chrome('..\\..\\ChromeDriver\\chromedriver.exe')  ##load chromediver
        self.airportcodepath = '..\\..\\AirPortCode.xlsx'  ##airport code path
        self.airportcodesheet = ['Canadian', 'USA', 'International']

        
    def GetGoogleWebContent(self):       
        self.browser.get(self.googleurl) ##open google url
        self.browser.maximize_window()
        time.sleep(5)  ##wait for the price loading from backstage
        
        flightcom = []
        flyinghour = []
        flightstops = []
        flightprice = []
        reslist = pd.DataFrame(columns=['company', 'hours', 'stops', 'price'])  ##build a blank dataframe with columns

        for company in self.browser.find_elements_by_xpath('//span[@class="gws-flights__ellipsize"]'):  ##get company name
            if (company.text != ''):
                flightcom.append(company.text)
        for hours in self.browser.find_elements_by_xpath('//div[@class="gws-flights-results__duration flt-subhead1Normal"]'):  ##get flight hours
            if (hours.text != ''):
                flyinghour.append((hours.text).replace(' h ', ':')[:5])
        for stops in self.browser.find_elements_by_xpath('//div[@class="gws-flights-results__itinerary-stops gws-flights__ellipsize"]'):  ##get stops
            if (stops.text[:7] != ''):
                flightstops.append(stops.text[:1])
        for price in self.browser.find_elements_by_xpath('//div[@class="gws-flights-results__itinerary-price"]'):  ##get price
            if (price.text != ''):
                if((price.text).replace(',', '')[1:].isdigit()):
                    flightprice.append((price.text).replace(',', '')[1:])
                else:
                    flightprice.append('0')
                    
        for i in range(0, len(flightcom)):  ##form data to dataframe
            reslist.loc[i + 1] = [flightcom[i], flyinghour[i], flightstops[i], flightprice[i]]
        return reslist

    def GetCeairWebContent(self):
        self.browser.get(self.ceairurl)
        self.browser.maximize_window()
        time.sleep(5)
        
        flightcom = 'China Eastern'
        flyinghour = []
        flightstops = '99'
        flightprice = []
        reslist = pd.DataFrame(columns=['company', 'hours', 'stops', 'price'])
        
        for hours in self.browser.find_elements_by_tag_name('dfn'):
            if (hours != ''):
                a = ':'
                flyinghour.append(a.join(re.findall(r'\d+', hours.text)))
        for prices in self.browser.find_elements_by_xpath('//dd[@class="price economy SCW_OD_MU_FF"]'):
            if (prices != ''):
                price = re.findall(r'\d+', prices.text)
                flightprice.append(int(price[0]+price[1]) + int(price[2] + price[3]))
        
        for i in range(0, len(flightprice)):
            reslist.loc[i + 1] = [flightcom, flyinghour[i], flightstops, flightprice[i]]
        return reslist
            
    
    #paytype = ['USD', 'CAD', 'CNY']
    #departplace, arriveplace = 'airportcode' string
    #passengernum = 'adult,child' string
    #departdate, returndate = 'yyyy-mm-dd' string  
    def SetGoogleUrl(self, departplace, arriveplace, paytype, passengernum, departdate, returndate = '', isdirect = True):
        if ((returndate == '') and (isdirect == True)):
            self.googleurl = self.googleurl + departplace + '.'  + arriveplace + '.' + departdate + ';' + 'c:' + paytype + ';e:1;s:0;px:' + passengernum + ';sd:1;t:f;tt:o'
            #print(self.googleurl)
        elif ((returndate == '') and (isdirect == False)):
            self.googleurl = self.googleurl + departplace + '.'  + arriveplace + '.' + departdate + ';' + 'c:' + paytype + ';e:1;px:' + passengernum + ';sd:1;t:f;tt:o'
            #print(self.googleurl)
        elif ((returndate != '') and (isdirect == True)):
            self.googleurl = self.googleurl + departplace + '.'  + arriveplace + '.' + departdate + '*' + arriveplace + '.' + departplace + '.' + returndate + ';' + 'c:' + paytype + ';e:1;s:0*0;px:' + passengernum + ';sd:1;t:f'
            #print(self.googleurl)
        elif ((returndate != '') and (isdirect == False)):
            self.googleurl = self.googleurl + departplace + '.'  + arriveplace + '.' + departdate + '*' + arriveplace + '.' + departplace + '.' + returndate + ';' + 'c:' + paytype + ';e:1;px:' + passengernum + ';sd:1;t:f'
            #print(self.googleurl)
        else:
            return False
        
    #paytype = ['USD', 'CAD', 'CNY']
    #departplace, arriveplace = 'airportcode' string
    #adt = 'adult' string
    #chd = 'child' string
    #departdate, returndate = 'yyyy-mm-dd' string
    def SetCeairUrl(self, departplace, arriveplace, adt, chd, departdate, returndate = ''):
        if ((returndate == '') and (chd == '')):
            self.ceairurl = self.ceairurl + departplace + '-a' + arriveplace + '-' + departdate + '_CNY.html?adt=' + adt
        elif ((returndate == '') and (chd != '')):
            self.ceairurl = self.ceairurl + departplace + '-a' + arriveplace + '-' + departdate + '_CNY.html?adt=' + adt + '&chd=' + chd
        elif ((returndate != '') and (chd == '')):
            self.ceairurl = self.ceairurl + departplace + '-a' + arriveplace + '-' + departdate + '-a' + arriveplace + '-a' + departplace + '-' + returndate + '_CNY.html?adt=' + adt
        elif ((returndate != '') and (chd != '')):
            self.ceairurl = self.ceairurl + departplace + '-a' + arriveplace + '-' + departdate + '-a' + arriveplace + '-a' + departplace + '-' + returndate + '_CNY.html?adt=' + adt + '&chd=' + chd        
        else:
            return False
        
    def GetAirportCity(self, departcode, arrivecode): ##get city name from airport code
        if ((departcode != '') and (arrivecode != '')):
            df = pd.DataFrame(columns = ['City','Code'])
            departcode = departcode.upper()
            arrivecode = arrivecode.upper()
            for i in self.airportcodesheet:
                df = df.append(pd.read_excel(self.airportcodepath, sheet_name = i, usecols = [0,1], sort = False, skiprow = 1, index = False))
            return (df.query('Code == @departcode').iloc[0, 0], df.query('Code == @arrivecode').iloc[0, 0])            
        else:
            return False
    
    def GetAirportCode(self, placename):  ##get city name from airport code
        if (placename != ''):
            df = pd.DataFrame(columns = ['City','Code'])
            for i in self.airportcodesheet:
                df = df.append(pd.read_excel(self.airportcodepath, sheet_name = i, usecols = [0,1], sort = False, skiprow = 1, index = False))
            return df.loc[df['City'].str.contains(placename)]
        else:
            return False
    
    def SaveDataToCSV(self, df, airflight = 'Google'):  ##write down dataframe to csv file
        if (airflight == 'Google'):
            if (os.path.exists(self.GoogleCsvfilepath)):
                df.to_csv(self.GoogleCsvfilepath, mode = 'a', header = False)
            else:
                df.to_csv(self.GoogleCsvfilepath)
        elif (airflight == 'Ceair'):
            if (os.path.exists(self.CeAirCsvfilepath)):
                df.to_csv(self.CeAirCsvfilepath, mode = 'a', header = False)
            else:
                df.to_csv(self.CeAirCsvfilepath)
        else:
            return False
    
    def CloseBrowser(self):
        self.browser.close()
        exit(0)

if __name__ == '__main__':
    fpc = FlightPriceCollecting()
    afterdays = 80  ##search future 80 days
    for i in range(1, afterdays):
        ceairtime = (datetime.datetime.now() + datetime.timedelta(days = i)).strftime('%y%m%d')
        googletime = (datetime.datetime.now() + datetime.timedelta(days = i)).strftime('%Y-%m-%d')
        
        fpc.SetCeairUrl('YYZ', 'PEK', '1', '', ceairtime, '')
        fpc.SaveDataToCSV(fpc.GetCeairWebContent(), 'Ceair')
        
        fpc.SetGoogleUrl('YYZ', 'PEK', 'CAD', '1', googletime, '', True)
        fpc.SaveDataToCSV(fpc.GetGoogleWebContent(), 'Google')
    
    fpc.CloseBrowser()
    exit(0)