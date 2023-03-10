# -*- coding: utf-8 -*-
"""fk_scrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14MjiyjY0xZywBpyIkKez_11may4GYM_w
"""

pip install pygsheets

import os
import re
import requests
import time
import pandas as pd
import pygsheets
import unicodedata
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone

def extract_fk_price(url):
    request = requests.get(url)
    soup = bs(request.content,'html.parser')
    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    new_str = unicodedata.normalize("NFKD", product_name)
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    prince_int = int(''.join(re.findall(r'\d+', price)))
    time_now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    return [new_str, prince_int, time_now]

path = '/content/akashscrapy-0c5d1ae1f416.json'
sheet_id = '1Wi2be1ph-_i7dvuDHHIVXHumDdqgJzg2rCXMtr0VJNE'
URL = "https://www.flipkart.com/motorola-edge-30-aurora-green-128-gb/p/itm819f84fdde956?pid=MOBGDCYGSKMGHQTA&lid=LSTMOBGDCYGSKMGHQTAEBOV0X&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_1&otracker=clp_bannerads_1_53.bannerAdCard.BANNERADS_moto-edge-30-sale-on%2B-%2BEnglish_mobile-phones-store_RO03NIAXT2ZN&fm=neo%2Fmerchandising&iid=29298dbc-87a5-4587-a545-8c5b2c346585.MOBGDCYGSKMGHQTA.SEARCH&ppt=clp&ppn=mobile-phones-store&ssid=xmnp2jakwg0000001671780231513"
gc = pygsheets.authorize(service_account_file = path)
gsheet_1 = gc.open_by_key(sheet_id)

output = extract_fk_price(URL)
df = pd.DataFrame([output], columns = ["Product", "Price", "Date Time"])

ws_1 = gsheet_1.worksheet()
sheet_df = ws_1.get_as_df()

if sheet_df.empty:
    ws_1.set_dataframe(df,
                     (1,1))
else:
    df = pd.concat([sheet_df, df], 
                   ignore_index=True)
    ws_1.set_dataframe(df,
                     (1,1))