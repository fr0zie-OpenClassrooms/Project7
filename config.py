from os import getenv
from dotenv import load_dotenv

load_dotenv()

APP = {
    'name': 'GrandPy Bot',
    'author': 'Axel Rayet',
    'repository': 'https://www.github.com/fr0zie-OpenClassrooms/Project7'
}

GOOGLE_API = {
    'api_key': getenv('API_KEY'),
    'url': 'https://maps.googleapis.com/maps/api/geocode/json'
}