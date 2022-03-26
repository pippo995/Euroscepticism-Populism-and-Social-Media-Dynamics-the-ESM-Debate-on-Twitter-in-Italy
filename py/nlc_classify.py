# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 18:39:00 2020

@author: pippo
"""

import pandas as pd 
from ibm_watson import NaturalLanguageClassifierV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('')
natural_language_classifier = NaturalLanguageClassifierV1(
    authenticator=authenticator
)

natural_language_classifier.set_service_url('https://api.eu-de.natural-language-classifier.watson.cloud.ibm.com/instances/a54be3b1-d001-4246-985f-b3595b34b279')


df = pd.read_csv('mes_2019-12-14.csv', low_memory=False)
#df1 = pd.read_csv('mes_2019-11-28.csv', low_memory=False)
#df2 = pd.read_csv('mes_2019-11-29.csv', low_memory=False)
#df3 = pd.read_csv('mes_2019-11-30.csv', low_memory=False)

def prev(text, ind):    
    try:
        cs = natural_language_classifier.classify('a23150x78-nlc-77', text).get_result()   
        print(ind)
        return cs['top_class'], cs['classes'][0]['confidence']
    except:
        print("An exception occurred at index " + str(ind))
        return 0, 0

df['prev'], df['p'] = zip(*df.apply(lambda x: prev(x['complete_text'], x.name),axis=1))
#df1['prev'], df1['p'] = zip(*df.apply(lambda x: prev(x['complete_text'], x.name),axis=1))
#df2['prev'], df2['p'] = zip(*df.apply(lambda x: prev(x['complete_text'], x.name),axis=1))
#df3['prev'], df3['p'] = zip(*df.apply(lambda x: prev(x['complete_text'], x.name),axis=1))



df.to_csv('mes_2019-12-14.csv', index = None, header = True)
#df1.to_csv('mes_2019-11-28.csv', index = None, header = True)
#df2.to_csv('mes_2019-11-29.csv', index = None, header = True)
#df3.to_csv('mes_2019-11-30.csv', index = None, header = True)

#cs = natural_language_classifier.classify('a23150x78-nlc-77, 'tradimento').get_result() 
#print ( cs['top_class'], cs['classes'][0]['confidence'])
df = pd.read_csv('mes_2019-12-15.csv', low_memory=False)
df['prev'], df['p'] = zip(*df.apply(lambda x: prev(x['complete_text'], x.name),axis=1))
df.to_csv('mes_2019-12-15.csv', index = None, header = True)

