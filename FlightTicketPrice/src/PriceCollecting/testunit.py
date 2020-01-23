import time
#import selenium as se
from selenium import webdriver
import re
import pandas as pd
from PriceCollecting import FlightPriceCollecting

fp = FlightPriceCollecting.FlightPriceCollecting()
#a, b = fp.GetAirportCity('yyz', 'tna')
#print(fp.GetAirportCode('Beijing'))

#fp.SetGoogleUrl('YYZ', 'PEK', 'CAD', '2,1', '2020-01-31', '', True)
#fp.SetCeairUrl('yyz', 'tna', '2', '2', '200418', '')
#print(fp.ceairurl)
fp.CloseBrowser()