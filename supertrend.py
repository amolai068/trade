import time
import pandas as pd
import numpy as np
import datetime
import schedule
from time import sleep
from datetime import timedelta, date
import yfinance as yf
import pandas_ta as ta
import warnings
import logging
import base64
import hmac
import os
import struct
from urllib.parse import urlparse, parse_qs
import requests
# from fyers_apiv3 import fyersModel
import pytz
import pyotp
import json
import math
import re

# Set display options for pandas
pd.set_option('display.max_columns', None)


import pyotp
from NorenRestApiPy.NorenApi import  NorenApi
class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')  
#start of our program
api = ShoonyaApiPy()
user    = "FA340196"
pwd     = "Amol$123456"
factor2 = "CHFPN0032H"
vc      = "FA340196_U"
app_key = "aa0a48765a59e188bb1dffc8ac38a032"
imei    = "abc1234"
token="L747MSG6725KTPS642E2V42D6273V542"
#make the api call
ret = api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei)

print(ret)







# user    = "FN111097"
# pwd     = "Adu@1403"
# factor2 = "ETVPP8180A"
# vc      = "FN111097_U"
# app_key = "626d13b741f64ad6ea3c876f2efac277"
# imei    = "abc1234"
# token="3PESI7P2EF7H776O2POCRCJA73XVFG6G"
# #make the api call
# ret = api.login(userid=user, password=pwd, twoFA=pyotp.TOTP(token).now(), vendor_code=vc, api_secret=app_key, imei=imei)

# print(ret)
 



import time
import csv
from datetime import datetime

# Specify the path where you want to store the CSV file
# mtm_csv_file = "mtm_history.csv"
mtm_csv_file = f"{datetime.now().date()} mtm_history.csv"

# Function to save MTM history and time to CSV
def save_mtm_to_csv(mtm, timestamp):
    # Check if the file already exists
    file_exists = os.path.isfile(mtm_csv_file)
    
    # Open the file in append mode
    with open(mtm_csv_file, mode='a', newline='') as file:
        fieldnames = ['time', 'pnl']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writeheader()
        
        # Write the MTM data
        writer.writerow({'time': timestamp, 'pnl': mtm})










# # Function to save MTM history and time to CSV
# def save_mtm_to_csv(mtm, timestamp):
#     # Initialize MTM and time history lists
#     mtm_history = []
#     time_history = []

#     # Append the data to the lists
#     mtm_history.append(mtm)
#     time_history.append(timestamp)
    
#     # Write MTM and time history to the CSV file
#     with open(mtm_csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([timestamp, mtm])





feed_opened = False
feedJson = {}

def event_handler_feed_update(tick_data):
    if 'lp' in tick_data and 'tk' in tick_data:
        timest = datetime.fromtimestamp(int(tick_data['ft'])).isoformat()
        feedJson[tick_data['tk']] = {'ltp': float(tick_data['lp']), 'tt': timest}
        # Optional delay for handling data at specific intervals
        time.sleep(1)  # 1-second delay between processing each tick data event
    
def event_handler_order_update(tick_data):
    print(f"Order update {tick_data}")

def open_callback():
    global feed_opened
    feed_opened = True

# Start the WebSocket and define callbacks
# if not feed_opened:
api.start_websocket(
    order_update_callback=event_handler_order_update,
    subscribe_callback=event_handler_feed_update, 
    socket_open_callback=open_callback
)

# Wait for the WebSocket connection to open
while not feed_opened:
    pass

# Subscribe to multiple tokens with delays between subscriptions if needed
tokens = ['NSE|26000']  # Add your list of tokens
for token in tokens:
    api.subscribe([token])
    time.sleep(2)  # 2-second delay between subscriptions



from datetime import datetime, timedelta
import pandas as pd

def get_time_series(exchange, token, days, interval):
    # Get the current date and time
    now = datetime.now()

    # Set the time to midnight
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Subtract days
    prev_day = now - timedelta(days=days)

    # Get the timestamp for the previous day
    prev_day_timestamp = prev_day.timestamp()

    # Use the prev_day_timestamp in your api call
    ret = api.get_time_price_series(exchange=exchange, token=token, starttime=prev_day_timestamp, interval=interval)
    if ret:
        return pd.DataFrame(ret)
    else:
        print("No Data for the given exchange, token, days and interval")




import pandas_ta as ta
import numpy as np
first_call = True
def supertrend(exchange, token, days, interval, ATR, Multi):
    global first_call
    # Get the time series data
    if first_call:
        df = get_time_series(exchange, token, days, interval)
        first_call = False
    else:
        df = get_time_series(exchange, token, days, interval)
    df = df.sort_index(ascending=False)
    df[['into','intl','intc','inth']] = df[['into','intl','intc','inth']].apply(pd.to_numeric)
    #df[['into','intl','intc','inth']]
    sti = ta.supertrend(df['inth'], df['intl'], df['intc'], length=ATR, multiplier=Multi)
    # sti = ta.supertrend(high=df['inth'], low=df['intl'], close=df['intc'], length=ATR, multiplier=Multi)
    sti = sti.sort_index(ascending=True)
   


  
    sti[['SUPERT_10_3.0','SUPERTd_10_3.0']]    
    # Calculate the SuperTrend
    sti['super_trend'] = sti[['SUPERT_10_3.0']]
    result = pd.concat([df, sti], axis=1)
    results = result.sort_index(ascending=True).rename(columns={'SUPERTd_10_3.0': 'signal', 'SUPERTl_10_3.0': 'S_UPT','SUPERTs_10_3.0': 'S_DT'})
    results[['into','inth','intl','intc','SUPERT_10_3.0','signal']]=results[['into','inth','intl','intc','SUPERT_10_3.0','signal']].apply(pd.to_numeric)


    return results[['time','into','inth','intl','intc','signal','SUPERT_10_3.0','S_UPT','S_DT']]



sd = api.searchscrip('NFO', 'NIFTY')
sd = (sd['values'])
for Symbol in sd:
    (Symbol['tsym'])
tsym_values = [Symbol['tsym'] for Symbol in sd[6:]]
dates = [re.search(r'\d+[A-Z]{3}\d+', tsym).group() for tsym in tsym_values]
formatted_dates = [datetime.strptime(date, '%d%b%y').strftime('%Y-%m-%d') for date in dates]
sorted_formatted_dates = sorted(formatted_dates)
sorted_dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%d%b%y').upper() for date in sorted_formatted_dates]
Expiry_date = (sorted_dates[0])
print(Expiry_date)



def get_order_status(orderno):
    OB = api.get_order_book()
    for item in OB:
        if item['norenordno'] ==orderno:
            return item['status']
        else:
            continue
        

def get_fillprice(norenordno):
    TB = api.get_trade_book()
    if TB is None:
        print('no order placed for the day')
    else:
        for item in TB:
            if item['norenordno'] == norenordno:
                return item['flprc']
    return "1"   

df  = supertrend('NSE', '26000', 5, 3, 10, 3)
df  #.signal[0]

def get_atm_ce_symbol(feedJson, sym, ExpDate):
    Atm = round(feedJson['26000']['ltp']/50, 0) * 50
    Atm_int = int(Atm)
    ce_symbol = sym + ExpDate + 'C' + str(Atm_int).rstrip('.')
    return ce_symbol


def get_atm_pe_symbol(feedJson, sym, ExpDate):
    Atm = round(feedJson['26000']['ltp']/50, 0) * 50
    Atm_int = int(Atm)
    pe_symbol = sym + ExpDate + 'P' + str(Atm_int).rstrip('.')
    return pe_symbol

def get_2otm_ce_symbol(feedJson, sym, ExpDate):
    Atm = (round(feedJson['26000']['ltp']/50, 0) * 50)+100
    Atm_int = int(Atm)
    ce_symbol = sym + ExpDate + 'C' + str(Atm_int).rstrip('.')
    return ce_symbol


def get_2otm_pe_symbol(feedJson, sym, ExpDate):
    Atm = (round(feedJson['26000']['ltp']/50, 0) * 50)-100
    Atm_int = int(Atm)
    pe_symbol = sym + ExpDate + 'P' + str(Atm_int).rstrip('.')
    return pe_symbol




# atm = get_atm_ce_symbol(feedJson, 'NIFTY', Expiry_date)

# feedJson['26000']['ltp']



def get_mtm():
                while True:
                    try:
                        ret = api.get_positions()
                        time.sleep(1)
                        break
                    except Exception:
                        print('Error Fetching MTM')
                        time.sleep(1)
                        continue
                mtm = 0
                pnl = 0
                day_m2m = 0
                try:
                    for i in ret:
                        mtm += float(i['urmtom'])
                        pnl += float(i['rpnl'])
                        day_m2m = round(mtm + pnl, 2)
                except TypeError:
                    # print('no open positions for the day, waiting for 1 minute before checking again')
                    return(day_m2m)
                    # time.sleep(60)


                current_time = datetime.now()
                save_mtm_to_csv(day_m2m, current_time)
                return(day_m2m)


# atm_ce=get_atm_ce_symbol(feedJson, 'NIFTY', Expiry_date)
# atm_pe=get_atm_pe_symbol(feedJson, 'NIFTY', Expiry_date)

# otm2_ce=get_2otm_ce_symbol(feedJson, 'NIFTY', Expiry_date)
# otm2_pe=get_2otm_pe_symbol(feedJson, 'NIFTY', Expiry_date)

import time

position_open = False
current_position = None  # Track the type of position ('put' or 'call')



while True:
    current_time3=datetime.now().strftime('%H:%M')
    Mtm_SL = 4000
    Mtm_target = 4000
    try:
        mtm=get_mtm()
    except:
        continue
        

    if current_time3 < "15:25" and -Mtm_SL <= mtm <= Mtm_target:

        # Fetch latest data for Supertrend signal
        try:
            df = supertrend('NSE', '26000', 5, 3, 10,3 )
            SIGNAL = []
            # Determine Buy or Sell signal
            if df['signal'][0] > df['signal'][1]:
                SIGNAL.append('Buy')
            elif df['signal'][0] < df['signal'][1]:
                SIGNAL.append('Sell')

        except:
            continue
        # else:
        #     continue
    
        # Check if there's a signal and if no position is currently open
        if SIGNAL and not position_open:
            # atm_ce = get_atm_ce_symbol(feedJson, 'NIFTY', Expiry_date)
            # atm_pe = get_atm_pe_symbol(feedJson, 'NIFTY', Expiry_date)
    
            otm2_ce = get_2otm_ce_symbol(feedJson, 'NIFTY', Expiry_date)
            otm2_pe = get_2otm_pe_symbol(feedJson, 'NIFTY', Expiry_date)
    
            if SIGNAL[0] == 'Buy':
                # Place a Sell order for put option (for option selling)
                entry_order = api.place_order(
                    buy_or_sell='S', product_type='M', exchange='NFO', 
                    tradingsymbol=otm2_pe, quantity=75, discloseqty=0,
                    price_type='MKT', price=0, trigger_price=0,
                    retention='DAY', remarks='option_sell_pe'
                )
                current_position = 'put'  # Track that we are in a put position
                time.sleep(10)

    
            elif SIGNAL[0] == 'Sell':
                # Place a Sell order for call option (for option selling)
                entry_order = api.place_order(
                    buy_or_sell='S', product_type='M', exchange='NFO', 
                    tradingsymbol=otm2_ce, quantity=75, discloseqty=0,
                    price_type='MKT', price=0, trigger_price=0,
                    retention='DAY', remarks='option_sell_ce'
                )
                current_position = 'call'  # Track that we are in a call position
                time.sleep(10)
            # else:
            #     continue
    
            # Mark position as open and retrieve order status
            # position_open = True
            ordno = entry_order["norenordno"]
            if entry_order['stat'] == 'Ok':
                print(f"Order placed successfully: {ordno}")
            else:
                print(f"Order error: {entry_order['emsg']}")
                break
            
            
            entry_order_no = entry_order["norenordno"]
            entry_order_status = get_order_status(entry_order_no) 
    
            if entry_order_status=='COMPLETE':
                position_open=True
            else:
                position_open=False
                print(f"status: {entry_order_status}")
            
    
            # Retrieve fill price and set stop-loss
            fill_price = float(get_fillprice(ordno))
            #Adjust SL as needed
            print(f"Entry price: {fill_price}")
    
            # Monitor for stop-loss hit or signal reversal
    
            stop_loss_hit = False
            while position_open:
                try:
                    df = supertrend('NSE', '26000', 10, 3, 10, 3)
                    SIGNAL = []
                    # Determine Buy or Sell signal
                    if df['signal'][0] > df['signal'][1]:
                        SIGNAL.append('Buy')
                    elif df['signal'][0] < df['signal'][1]:
                        SIGNAL.append('Sell')
                    else:
                        SIGNAL.append('Neutral')
                except:
                    continue
                
    
    
    
                current_signal = SIGNAL[0]
                current_ltp = feedJson['26000']['ltp']     
                Mtm_SL = 4000
                Mtm_target = 4000
                mtm = get_mtm() 
    
    
    
                try:
                    SL_mtm = mtm <= (-Mtm_SL)
                    Target_mtm = mtm >= Mtm_target
                except TypeError:
                    pass
               
                current_time2=datetime.now().strftime('%H:%M')
    
                # Check if stop-loss hit or signal reversal for specific position
                if current_position == 'put' and (SL_mtm or Target_mtm or current_signal == 'Sell' or current_time2 > '15:25'):
                    # Exit the put option position on SL hit or signal change from Buy to Sell
                    exit_order = api.place_order(
                        buy_or_sell='B', product_type='M', exchange='NFO',
                        tradingsymbol=otm2_pe, quantity=75, discloseqty=0,
                        price_type='MKT', price=0, trigger_price=0,
                        retention='DAY', remarks='option_exit_put'
                    )
                    time.sleep(8)
    
                elif current_position == 'call' and (SL_mtm or Target_mtm or current_signal == 'Buy' or current_time2 > '15:25'):
                    # Exit the call option position on SL hit or signal change from Sell to Buy
                    exit_order = api.place_order(
                        buy_or_sell='B', product_type='M', exchange='NFO',
                        tradingsymbol=otm2_ce, quantity=75, discloseqty=0,
                        price_type='MKT', price=0, trigger_price=0,
                        retention='DAY', remarks='option_exit_call'
                    )
                    time.sleep(8)
                else:
                    continue
    
                # Check if exit order completed successfully
                exit_ordno = exit_order["norenordno"]
                exit_status = get_order_status(exit_ordno)  # Replace with get_order_status(exit_ordno) if available
    
                if exit_status == "COMPLETE":
                    stop_loss_hit = True
                    position_open = False
                    current_position = None
                    print(f"Exit order {exit_ordno} completed. Re-entering after 1 minute.")
                    time.sleep(2)  # Wait for 5 minutes before re-checking signals

                elif exit_status=='PENDING':
                    api.cancel(exit_ordno)
                    continue

                else:
                    print("Exit order placed but not completed. Retrying in 5 seconds.")
                    time.sleep(3)
                    continue
    
        else:
            print("No valid trading signal or position already open.")
            time.sleep(22)  # Short pause before re-evaluating signals
    else:
        print('you cant take position after 3:20')
        time.sleep(30)
    
