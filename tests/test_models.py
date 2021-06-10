import app.models as script


class TestParser:

    def setup_method(self):
        self.parser = script.Parser("Hello GrandPy! Je cherche l'adresse d'OpenClassrooms...")
    
    def test_parse(self):
        self.parser.parse()
        assert self.parser.result == "openclassrooms"

class TestGoogleAPI:

    def setup_method(self):
        self.parser = script.Parser("Salut GrandPy! J'ai besoin de l'adresse d'OpenClassrooms!")
        self.parser.parse()
        self.google_api = script.GoogleAPI(self.parser.result)
        self.geodata = {
            'latitude': 48.8975156,
            'longitude': 2.3833993
        }

    def test_get_query(self):
        assert self.google_api.query == "openclassrooms"

    def test_get_geodata(self):
        self.google_api.get_geodata()
        assert self.geodata == self.google_api.geodata