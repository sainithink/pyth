# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:49:54 2020

@author: nanir
"""

import logging
from kiteconnect import KiteConnect
import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from kiteconnect import KiteTicker
from datetime import datetime,timedelta
import pandas as pd
import pytz
print("test")


api_key = 'j5fw51nqg33y1gp1'
api_secret = 'cjoyxq7gq7lqrebd3z8fpvh9boya0nju'
username = 'ZL2393'
password = 'Apple@4b5'
pin = '453945'

def getCssElement( driver , cssSelector ):
    return WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( ( By.CSS_SELECTOR, cssSelector ) ) )

def autologin():
    kite = KiteConnect(api_key=api_key)
    service = webdriver.chrome.service.Service('./chromedriver')
    service.start()
    options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
    options = options.to_capabilities()
    driver = webdriver.Remote(service.service_url, options)
    driver.get(kite.login_url())
    
    passwordField = getCssElement( driver , "input[placeholder=Password]" )
    passwordField.send_keys( password )
    
    userNameField = getCssElement( driver , "input[placeholder='User ID']" )
    userNameField.send_keys( username )
    
    loginButton = getCssElement( driver , "button[type=submit]" )
    loginButton.click()
    
    waitingEle = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'twofa-value')))
    pinField = driver.find_element_by_class_name('twofa-value').find_element_by_xpath(".//input[1]")
    pinField.send_keys( pin )
    
    loginButton = getCssElement( driver , "button[type=submit]" )
    loginButton.click()
    
    time.sleep(10)
    request_token=driver.current_url.split('=')[1].split('&action')[0]
    with open('request_token.txt', 'w') as the_file:
        the_file.write(request_token)
    driver.quit()
    time.sleep(10)

autologin()

request_token = open("request_token.txt",'r').read()
kite = KiteConnect(api_key=api_key)
data = kite.generate_session(request_token, api_secret=api_secret)
with open('access_token.txt', 'w') as file:
        file.write(data["access_token"])
data["access_token"]


access_token_zerodha = open("access_token.txt",'r').read()
# creating permanent kite connect object
kite = KiteConnect(api_key=api_key)
# setting access token ti kite connect object
kite.set_access_token(access_token_zerodha)


def movingAverage(data):
    res = (data[0]+data[1]+data[2]+data[3]+data[4])/5
      #for x in range(2,len(data)):
    #    res = (res+data[x])/2
    return res


allTokens = [4774913,1723649,
2939649,
2672641,
2815745,
1041153,
806401,
895745,
3520257,
3465729,
2170625,
969473,
681985,
5633,
6401,
3861249,
2079745,
25601,
325121,
40193,
41729,
54273,
60417,
5436929,
70401,
1510401,
4267265,
4268801,
81153,
579329,
94977,
98049,
103425,
108033,
2714625,
2911489,
134657,
140033,
2763265,
149249,
3905025,
160001,
160769,
175361,
177665,
5215745,
3876097,
1215745,
486657,
197633,
3513601,
2800641,
225537,
232961,
245249,
1207553,
1895937,
2585345,
4576001,
315393,
2513665,
1850625,
340481,
341249,
119553,
345089,
2747905,
359937,
356865,
1270529,
2865921,
408065,
424961,
3001089,
7670273,
462849,
492033,
511233,
519937,
3400961,
2674433,
7982337,
548353,
4488705,
3675137,
2955009,
633601,
617473,
3660545,
6191105,
3365633,
523009,
4708097,
3930881,
738561,
779521,
837889,
1102337,
1887745,
857857,
3431425,
878593,
873217,
884737,
2953217,
897537,
900609,
3529217,
4278529,
2952193,
2889473,
951809,
975873,
6054401,
2883073,
7712001,
261889,
4774913,
1723649,
2939649,
2672641,
2815745,
1041153,
806401,
895745,
3520257,
3465729,
2170625,
969473,
681985,
1346049,
3834113]
 #,264713,264969,258057,258569,260617,264457,256265,268041,265993,263433,260105,257289,257545,
#268297,257033,261641,257801,261897,270345,269065,269321,269577,269833,268553,268809,270089,261385,259849]
TOKENS = []
allTokens
baseTest = datetime.now() - timedelta(days=1)
testStart = baseTest.replace(hour = 14,minute=15,second=0)
testEnd = baseTest.replace(hour = 15,minute=29,second=59)
testStart = testStart.strftime('%Y-%m-%d %H:%M:%S')
testEnd = testEnd.strftime('%Y-%m-%d %H:%M:%S')

todayCandle = datetime.now()
todayCandleStart = todayCandle.replace(hour = 9,minute=15,second=0)
todayCandleEnd = todayCandle.replace(hour = 9,minute=29,second=59)
todayCandleStart = todayCandleStart.strftime('%Y-%m-%d %H:%M:%S')
todayCandleEnd = todayCandleEnd.strftime('%Y-%m-%d %H:%M:%S')

for token in allTokens:
    yesterdayData = 1
    #print(token)
    while yesterdayData:
        try:
            data = kite.historical_data(token,testStart,testEnd,'15minute')
        except:
            break
        if(data):
            yesterdayData = 0
        else:
            baseTest = baseTest - timedelta(days=1)
            testStart = baseTest.replace(hour = 14,minute=15,second=0)
            testEnd = baseTest.replace(hour = 15,minute=29,second=59)
            testStart = testStart.strftime('%Y-%m-%d %H:%M:%S')
            testEnd = testEnd.strftime('%Y-%m-%d %H:%M:%S')
    #print(kite.historical_data(token,todayCandleStart,todayCandleEnd,'15minute'))
    todayVolume = kite.historical_data(token,todayCandleStart,todayCandleEnd,'15minute')[0]['volume']
    movingAvg = [x['volume'] for x in data]
    movingAvg = movingAverage(movingAvg) * 1.5
    if(todayVolume>movingAvg):
        TOKENS.append(token)
    #print(todayVolume,movingAvg,token)
#baseTest
TOKENS

DATABASE = {token:[] for token in TOKENS}
fromDate = datetime(
    day = datetime.now().day,
    month = datetime.now().month,
    year = datetime.now().year,
    hour = 9,
    minute = 15,
    second = 0
)
toDate = fromDate + timedelta(minutes=29,seconds=59)
fromDate = fromDate.strftime('%Y-%m-%d %H:%M:%S')
toDate = toDate.strftime('%Y-%m-%d %H:%M:%S')
print(fromDate,toDate,TOKENS)
for token in TOKENS:
    data = kite.historical_data(token,fromDate,toDate,'30minute')
    print(data)
    DATABASE[token] = pd.DataFrame(data)
    
dataDump = kite.instruments()
tokenName = {}
for x in TOKENS:
    for y in dataDump:
        if(y['instrument_token']==x):
            tokenName[x] =y['tradingsymbol']
tokenName


for x in DATABASE:
    DATABASE[x]['buyonce'] = 1
    DATABASE[x]['sellonce'] = 1
    print(DATABASE[x])
    
kws = KiteTicker(api_key, access_token_zerodha)
BUYEND = datetime.now(pytz.timezone('Asia/Kolkata')).replace(hour=15,minute=30)
def on_ticks(ws, ticks):
    global BUYEND
    pnlToday = sum([x['pnl'] for x in kite.positions()['net']])
    if(pnlToday>5000 or pnlToday<-5000):
        ordersLeft = [x['order_id'] for x in kite.orders() if (x['status']=='OPEN' or x['status']=='PENDING') or x['status']=='TRIGGER PENDING' and x['']]
        print(ordersLeft)
        for x in ordersLeft:
            kite.cancel_order(variety=kite.VARIETY_REGULAR,order_id=x)
    Capital = 22000
    elm_count = len(TOKENS)
    qty = Capital/elm_count
#     print(ticks)
    print(datetime.now(),BUYEND)
    if(datetime.now(pytz.timezone('Asia/Kolkata'))>BUYEND):
        return
    for tick in ticks:
        currentToken = tick['instrument_token']
        #print(tokenName[currentToken],tick['last_price'],DATABASE[currentToken]['high'].iloc[0],DATABASE[currentToken]['buyonce'].iloc[0],DATABASE[currentToken]['low'].iloc[0],DATABASE[currentToken]['sellonce'].iloc[0])
        orderBook = kite.orders()
        checkBuy = 1
        checkSell = 1
        buyOrderCount = 0
        sellOrderCount = 0
        lastOrderType = None
        lastOrderTs = datetime(2020,1,1)
        for x in orderBook:
            if(x['instrument_token']==currentToken and x['status']=='COMPLETE'):
                if(x['transaction_type']=='BUY'):
                    buyOrderCount += 1
                    if(x['order_timestamp']>lastOrderTs):
                        lastOrderTs = x['order_timestamp']
                        lastOrderType = 'BUY'
                elif(x['transaction_type']=='SELL'):
                    sellOrderCount += 1
                    if(x['order_timestamp']>lastOrderTs):
                        lastOrderTs = x['order_timestamp']
                        lastOrderType = 'SELL'
        
        if(sellOrderCount>buyOrderCount):
            checkSell = 0
        elif(sellOrderCount<buyOrderCount):
            checkBuy = 0
        else:
            if(lastOrderType=='BUY'):
                checkSell=0
            elif(lastOrderType=='SELL'):
                checkBuy=0
            ordersLeft = [x['order_id'] for x in kite.orders() if (x['status']=='OPEN' or x['status']=='PENDING' or x['status']=='TRIGGER PENDING') and x['instrument_token']==currentToken]
            for x in ordersLeft:
                kite.cancel_order(variety=kite.VARIETY_REGULAR,order_id=x)
        print(currentToken,buyOrderCount,sellOrderCount)    
        if(tick['last_price']>DATABASE[currentToken]['high'].iloc[0] and checkBuy):
            #DATABASE[currentToken]['buyonce'] = 0
            print('o1',currentToken,tokenName[currentToken])
            orderId = kite.place_order(variety=kite.VARIETY_REGULAR, 
                        exchange=kite.EXCHANGE_NSE, 
                        tradingsymbol=tokenName[currentToken], 
                        transaction_type=kite.TRANSACTION_TYPE_BUY, 
                        quantity=1, 
                        product=kite.PRODUCT_MIS, 
                        order_type=kite.ORDER_TYPE_MARKET, 
                        price=None, 
                        validity=None, 
                        disclosed_quantity=None, 
                        trigger_price=None, 
                        squareoff=None, 
                        stoploss=None, 
                        trailing_stoploss=None)            
            kite.place_order(tradingsymbol=tokenName[currentToken],
                            exchange=kite.EXCHANGE_NSE,
                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                            quantity=1,
                            price = round(tick['last_price']*1.01,1),
                            order_type=kite.ORDER_TYPE_LIMIT,
                            product=kite.PRODUCT_MIS,
                            variety=kite.VARIETY_REGULAR)
            kite.place_order(tradingsymbol=tokenName[currentToken],
                            exchange=kite.EXCHANGE_NSE,
                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                            quantity=1,
                            order_type=kite.ORDER_TYPE_SLM,
                            price=round(tick['last_price']*0.98,1),
                            trigger_price=round(tick['last_price']*0.98,1),
                            product=kite.PRODUCT_MIS,
                            variety=kite.VARIETY_REGULAR)
            print(orderId)
        elif(tick['last_price']<DATABASE[currentToken]['low'].iloc[0] and checkSell):
            #DATABASE[currentToken]['sellonce'] = 0
            print('o2',currentToken,tokenName[currentToken])
            orderId = kite.place_order(variety=kite.VARIETY_REGULAR, 
                        exchange=kite.EXCHANGE_NSE, 
                        tradingsymbol=tokenName[currentToken], 
                        transaction_type=kite.TRANSACTION_TYPE_SELL, 
                        quantity=1, 
                        product=kite.PRODUCT_MIS, 
                        order_type=kite.ORDER_TYPE_MARKET, 
                        price=None, 
                        validity=None, 
                        disclosed_quantity=None, 
                        trigger_price=None, 
                        squareoff=None,
                        stoploss=None,
                        trailing_stoploss=None)
            kite.place_order(tradingsymbol=tokenName[currentToken],
                            exchange=kite.EXCHANGE_NSE,
                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                            quantity=1,
                            price = round(tick['last_price']*0.99,1),
                            order_type=kite.ORDER_TYPE_LIMIT,
                            product=kite.PRODUCT_MIS,
                            variety=kite.VARIETY_REGULAR)
            kite.place_order(tradingsymbol=tokenName[currentToken],
                            exchange=kite.EXCHANGE_NSE,
                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                            quantity=1,
                            order_type=kite.ORDER_TYPE_SLM,
                            price=round(tick['last_price']*1.02,1),
                            trigger_price = round(tick['last_price']*1.02,1),
                            product=kite.PRODUCT_MIS,
                            variety=kite.VARIETY_REGULAR)
            print(orderId)
    

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(TOKENS)


def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    pass

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.

while(datetime.now(pytz.timezone('Asia/Kolkata'))<datetime.now(pytz.timezone('Asia/Kolkata')).replace(hour=9,minute=45)):
    pass
kws.connect()
