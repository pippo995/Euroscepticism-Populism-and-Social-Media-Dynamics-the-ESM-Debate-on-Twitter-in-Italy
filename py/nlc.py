# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:33:45 2020

@author: pippo
"""

import json
from ibm_watson import NaturalLanguageClassifierV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('')
natural_language_classifier = NaturalLanguageClassifierV1(
    authenticator=authenticator
)

natural_language_classifier.set_service_url('https://api.eu-de.natural-language-classifier.watson.cloud.ibm.com/instances/a54be3b1-d001-4246-985f-b3595b34b279')


with open('mes_cat.csv', 'rb') as training_data:
    classifier = natural_language_classifier.create_classifier(
    training_data=training_data,
    training_metadata='{"name": "MesClassifier","language": "it"}'
  ).get_result()
print(json.dumps(classifier, indent=2))
