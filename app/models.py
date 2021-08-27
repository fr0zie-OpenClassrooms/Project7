import json
import requests
import re
import random
from config import GOOGLE_API, MEDIAWIKI_API


class Parser:
    """Class parsing the user input to get only keywords."""

    def __init__(self, input: str):
        """Class initialization."""

        self.input = input
        self.result = ""

        self.parse()

    def parse(self):
        """Method used to parse the user input."""

        result = []
        stop_words = json.load(open("app/data/stop_words.json"))

        self.input = re.sub("-", " ", self.input).lower()

        for word in self.input.split():
            word = word[2:] if "'" in word else word

            word = re.sub("[!@#$?,:;.]*", "", word)

            if word in stop_words["words"]:
                continue

            result.append(word)

        self.result = " ".join(result)


class GoogleAPI:
    """Class used to get geodata from the user input."""

    def __init__(self, query):
        """Class initialization."""

        self.answers = [
            "Voici l'adresse:",
            "Il a fallu que je me rappelle... C'est",
            "Si ma mémoire est bonne, il me semble que ça se trouve",
        ]

        self.query = query
        self.address = ""
        self.status = ""
        self.geodata = {}

        self.get_geodata()

    def get_geodata(self):
        """Method used to get geodata."""

        params = {"address": self.query + ",+FR", "key": GOOGLE_API["api_key"]}

        result = requests.get(GOOGLE_API["url"], params)
        json = result.json()

        self.geodata["status"] = json["status"]

        if json["status"] != "ZERO_RESULTS":
            address = json["results"][0]["formatted_address"]
            self.address = (
                random.choice(self.answers)
                + " "
                + address[0].lower()
                + address[1:]
                + "."
            )
            self.status = "alert-success"
            self.geodata["latitude"] = json["results"][0]["geometry"]["location"]["lat"]
            self.geodata["longitude"] = json["results"][0]["geometry"]["location"][
                "lng"
            ]
        else:
            self.address = "Désolé mon grand, je ne connais pas " + self.query + "..."
            self.status = "alert-warning"


class MediaWikiAPI:
    """Class used to get details about a place from Media Wiki."""

    def __init__(self, geodata):
        """Class initialization."""

        self.answers = [
            "D'ailleurs, ça me fait penser... Pas loin se trouve l'endroit où j'ai rencontré ma femme, GrandMy.",
            "Mais t'ai-je déjà expliqué l'histoire de cet endroit? Non? Alors je vais plutôt te raconter l'histoire de sa rue mitoyenne!",
            "Haaa oui, dans ma jeunesse j'y ai passé pas mal de temps! Enfin, dans la rue juste à côté...",
        ]

        if geodata["status"] != "ZERO_RESULTS":
            self.geodata = "|".join(
                [str(geodata["latitude"]), str(geodata["longitude"])]
            )
            self.pageid = 0
            self.extract = ""

            self.get_pageid()
            self.get_extract()
        else:
            self.extract = "Peux-tu répéter ta question?"

    def get_pageid(self):
        """Method used to get page ID from geodata."""

        params = {
            "action": "query",
            "list": "geosearch",
            "gscoord": self.geodata,
            "gsradius": 1000,
            "format": "json",
        }

        result = requests.get(MEDIAWIKI_API["url"], params)
        json = result.json()

        self.pageid = json["query"]["geosearch"][0]["pageid"]

    def get_extract(self):
        params = {
            "action": "query",
            "pageids": self.pageid,
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "format": "json",
        }

        result = requests.get(MEDIAWIKI_API["url"], params)
        json = result.json()

        self.extract = (
            random.choice(self.answers)
            + " "
            + json["query"]["pages"][str(self.pageid)]["extract"]
        )
