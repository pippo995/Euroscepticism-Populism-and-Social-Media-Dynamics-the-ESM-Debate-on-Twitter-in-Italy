# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:05:37 2019

@author: pippo
"""
import botometer
import json
import pandas as pd 

# load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    twitter_app_auth = {
        'consumer_key': info['CONSUMER_KEY'],
        'consumer_secret': info['CONSUMER_SECRET'],
        'access_token':  info['ACCESS_KEY'],
        'access_token_secret': info['ACCESS_SECRET'],
      }

#pass security information to variables
rapidapi_key = ""
botometer_api_url = 'https://botometer-pro.p.rapidapi.com'

bom = botometer.Botometer(botometer_api_url=botometer_api_url,
                          wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check an account
#account = "@FilippoScotti95"
#result = bom.check_account(account)
#print("cap: " + str(result["cap"]["universal"]) + ", un: " + str(result["scores"]["universal"]))

# Do stuff with `screen_name` and `result`
#print(str(result["user"]["screen_name"]), str(result["cap"]["universal"]))

# Check a sequence of accounts
#accounts = ['@clayadavis', '@onurvarol', '@vonpippo']
#for result in bom.check_accounts_in(accounts):
#    print(result)

 
def botfilter(auth, ind):  
    try:
        result = bom.check_account(auth)
        print(ind.name)
        print(auth + " p of bot " + str(result["cap"]["universal"]) + ", un: " + str(result["scores"]["universal"]))
        return pd.Series([str(result["cap"]["universal"]), str(result["scores"]["universal"]), str(result["categories"]["friend"]), str(result["categories"]["temporal"]), str(result["categories"]["user"]), str(result["categories"]["network"])])
    except:
        print("no access to " + auth)
        return(-1)
    
df = pd.read_csv('authors.csv')
dt = df.loc[(df.index >= 29000) & (df.index < 29523)]
#dt[['cap'],['universal']] = dt['0'].apply(botfilter)
dt[['cap','universal', 'friend', 'temporal', 'user', 'network']] = dt.apply(lambda x: pd.Series(botfilter(x['0'], x)), axis=1)
dt.to_csv('authors_bot29000to29523.csv', index=None)


#for row in df.iterrows():
    #result = bom.check_account(row[1])
   # print(str(result["user"]["screen_name"]), str(result["cap"]["universal"]))
