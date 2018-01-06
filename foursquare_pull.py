# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 09:05:27 2018
@author: FSinohui
"""
import json, requests
import pandas as pd
import os


path = r'\\hftdata02\sysdata02\RedCat\Exports\python_exports'
#read in all the needed tables
store_lat_lon_pd         = pd.read_csv(path+'\store_lat_lon.csv')  


store_stat_list_df = pd.DataFrame()
store_rating_list_df = pd.DataFrame()
missingStore = []

for i, row in store_lat_lon_pd.iterrows():
    
    lat = store_lat_lon_pd.get_value(i, str("LATITUDE"), takeable=False)
    lon = store_lat_lon_pd.get_value(i, str("LONGITUDE"), takeable=False)
    lat_lon=str(lat)+','+str(lon)
    print(lat_lon,'   ',i)
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
      client_id = 'U35350IEZB4GPFJM0RGD4JC0IFNBVDRYSEZLEIZYEXFJJSFN',
      client_secret = 'NXHB0CMRGYYABMI3RG53CKA1YLXRSVDO0YL25YISLEG5LRKH',
      v='20180101',
      ll=lat_lon,
      intent='match',
      query='harbor freight',
      limit=1
      )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
        

    try:
        try:
            city = data['response']['venues'][0]['location']['city']
        except:
            city = store_lat_lon_pd.get_value(i, str("CITY"), takeable=False)
        state = data['response']['venues'][0]['location']['state']
        name = data['response']['venues'][0]['name']
        try:
            store = data['response']['venues'][0]['storeId']
        except KeyError:
            store = store_lat_lon_pd.get_value(i, str("STORE_NUM"), takeable=False)
        checkinsCount = data['response']['venues'][0]['stats']['checkinsCount']
        usersCount = data['response']['venues'][0]['stats']['usersCount']
        
        store_stat_df = pd.DataFrame({'StoreID': store,
                              'City':city,
                              'State': state,
                              'Check ins Count':checkinsCount,
                              'Users Count': [usersCount]})
        store_stat_list_df = pd.concat([store_stat_list_df,store_stat_df]) 
    except IndexError:
        store_stat_df = pd.DataFrame({'StoreID': store,
                                      'City':store_lat_lon_pd.get_value(i, str("CITY"), takeable=False),
                                      'State': store_lat_lon_pd.get_value(i, str("STATE"), takeable=False),
                                      'Check ins Count':[0],
                                      'Users Count': [0]})
        store_stat_list_df = pd.concat([store_stat_list_df,store_stat_df]) 
    
    
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
      client_id = 'U35350IEZB4GPFJM0RGD4JC0IFNBVDRYSEZLEIZYEXFJJSFN',
      client_secret = 'NXHB0CMRGYYABMI3RG53CKA1YLXRSVDO0YL25YISLEG5LRKH',
      v='20180101',
      ll=lat_lon,
      intent='match',
      query='harbor freight',
      limit=1
      )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    try: 

        #print(data)
        try:
            name = data['response']['groups'][0]['items'][0]['venue']['name']
        except:
            name  = 'Not Found'
        try:
            rating = data['response']['groups'][0]['items'][0]['venue']['rating']
        except :
            rating = 0.001
        #print(city + ' ' + name + ' ' +str(rating))
        store_rating_df = pd.DataFrame({'StoreID': store,
                                      'Rating':[rating],
                                      'Name': [name]})
        store_rating_list_df = pd.concat([store_rating_list_df,store_rating_df]) 
    except KeyError:
        store_rating_df = pd.DataFrame({'StoreID': store,
                                      'Rating':[0],
                                      'Name': 'Not found'})

try: 
    os.remove(r'\\hftdata02\sysdata02\RedCat\Exports\FourSquare_Rating_Data.xlsx')
except FileNotFoundError:
    print('file not found')
    
rating_writer = pd.ExcelWriter(r'\\hftdata02\sysdata02\RedCat\Exports\FourSquare_Rating_Data.xlsx',
                             engine='xlsxwriter')
   
store_stat_list_df.to_excel(rating_writer,
                    sheet_name='stat',
                    columns=['City','State','Store','Check ins Count','Users Count'],
                    index=False)
store_rating_list_df.to_excel(rating_writer,
                    sheet_name='Ratings',
                    columns=['StoreID','Rating','Name'],
                    index=False)


