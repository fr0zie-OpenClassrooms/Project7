import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import app.models as script


class TestQuery:

    def setup_method(self):
        self.query = script.Query("Hello GrandPy! Je cherche l'adresse d'OpenClassrooms...")

    def test_get_casefold_input(self):
        assert self.query.input == "hello grandpy! je cherche l'adresse d'openclassrooms..."
    
    def test_parse(self):
        self.query.parse()
        assert self.query.query == "openclassrooms"

class TestResult:

    def setup_method(self):
        self.query = script.Query("Hello GrandPy! Je cherche l'adresse d'OpenClassrooms...")
        self.query.parse()
        self.result = script.Result(self.query.query)
        self.maps_data = {
            'formatted_address': '10 Quai de la Charente, 75019 Paris, France',
            'address': {
                'street_number': '10',
                'route': 'Quai de la Charente',
                'postal_code': '75019',
                'locality': 'Paris',
                'country': 'France',
                'administrative_area_level_1': 'Île-de-France',
                'administrative_area_level_2': 'Département de Paris'
            }
        }

    def test_get_result_query(self):
        assert self.result.query == "openclassrooms"

    def test_get_result_maps_data(self):
        self.result.get_maps_data()
        assert self.maps_data == self.result.maps_data