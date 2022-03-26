# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 17:43:17 2020

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

status = natural_language_classifier.get_classifier('a23150x78-nlc-77').get_result()
print (json.dumps(status, indent=2))
