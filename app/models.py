import json
import requests
import re
import urllib.parse as urlparse
from config import GOOGLE_API, MEDIAWIKI_API


class Parser:
    '''Class parsing the user input to get only keywords.'''

    def __init__(self, input: str):
        '''Class initialization.'''

        self.input = input
        self.result = ''

    def parse(self):
        '''Method used to parse the user input.'''

        result = []
        stop_words = json.load(open('app/data/stop_words.json'))

        self.input = re.sub('-', ' ', self.input).lower()

        for word in self.input.split():
            word = word[2:] if '\'' in word else word                

            word = re.sub('[!@#$?,:;.]*', '', word)
            
            if word in stop_words['words']:
                continue

            result.append(word)

        self.result = ' '.join(result)


class GoogleAPI:
    '''Class used to get geodata from the user input.'''

    def __init__(self, query):
        '''Class initialization.'''

        self.query = query
        self.geodata = {}
        self.map = ''

    def get_geodata(self):
        '''Method used to get geodata.'''

        params = {
            'address': self.query + ',+FR',
            'key': GOOGLE_API['api_key']
        }

        result = requests.get(GOOGLE_API['url'], params)
        json = result.json()

        self.geodata['latitude'] = json['results'][0]['geometry']['location']['lat']
        self.geodata['longitude'] = json['results'][0]['geometry']['location']['lng']


class MediaWikiAPI:
    '''Class used to get details about a place from Media Wiki.'''

    def __init__(self, geodata):
        '''Class initialization.'''

        self.geodata = '|'.join([str(geodata['latitude']), str(geodata['longitude'])])
        self.pageid = 0
        self.extract = ''

    def get_pageid(self):
        '''Method used to get page ID from geodata.'''

        params = {
            'action': 'query',
            'list': 'geosearch',
            'gscoord': self.geodata,
            'gsradius': 1000,
            'format': 'json'
        }

        result = requests.get(MEDIAWIKI_API['url'], params)
        json = result.json()

        self.pageid = json['query']['geosearch'][0]['pageid']
        return self.pageid

    def get_extract(self):
        params = {
            'action': 'query',
            'pageids': self.pageid,
            'prop': 'extracts',
            'exintro': 1,
            'explaintext': 1,
            'format': 'json'
        }

        result = requests.get(MEDIAWIKI_API['url'], params)
        json = result.json()

        self.extract = json['query']['pages'][str(self.pageid)]['extract']
        return self.extract

class Answer:
    '''Class used to answer the user's query with personalized responses.'''

    def __init__(self, google_api):
        '''Class initialization.'''

        self.google_api = google_api

    def get_place_address(self):
        '''Method used to answer a place address.'''

        answer = 'Bien sûr mon poussin ! La voici :'

    def get_place_details(self):
        '''Method used to answer a story about a place.'''

        answer = 'Mais t\'ai-je déjà raconté l\'histoire de ce quartier qui m\'a vu en culottes courtes ?'