import app.models as script


class TestParser:

    def setup_method(self):
        self.parser = script.Parser("Hello GrandPy! Je cherche l'adresse d'OpenClassrooms...")
    
    def test_parse(self):
        self.parser.parse()
        assert self.parser.result == 'openclassrooms'

class TestGoogleAPI:

    def setup_method(self):
        self.parser = script.Parser("Salut GrandPy! J'ai besoin de l'adresse d'OpenClassrooms!")
        self.parser.parse()
        self.google_api = script.GoogleAPI(self.parser.result)

        self.geodata = {
            'latitude': 48.8975156,
            'longitude': 2.3833993
        }
        self.map = 'https://www.google.com/maps/embed/v1/view?center=48.8975156%2C2.3833993&zoom=18&key=AIzaSyC6CfQwsFI04fin1yEpsR3Il-6gYHaMr1M'

        self.google_api.get_geodata()
        self.google_api.get_map()

    def test_get_query(self):
        assert self.google_api.query == 'openclassrooms'

    def test_get_geodata(self):
        assert self.geodata == self.google_api.geodata

    def test_get_map(self):
        assert self.map == self.google_api.map


class TestMediaWikiAPI:

    def setup_method(self):
        self.parser = script.Parser("J'aurais besoin de l'adresse d'OpenClassrooms s'il te plait GrandPy!")
        self.parser.parse()
        self.mediawiki_api = script.MediaWikiAPI(self.parser.result)

        self.url = 'https://fr.wikipedia.org/w/api.php?action=query&list=search&srsearch=openclassrooms&format=json'

        self.mediawiki_api.get_url()

    def test_get_url(self):
        assert self.url == self.mediawiki_api.url