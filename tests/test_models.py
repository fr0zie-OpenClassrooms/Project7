import app.models as script
import pytest
import requests


class TestParser:

    @pytest.mark.parametrize('input, expected', [
            ('Hello GrandPy! Je cherche l\'adresse d\'OpenClassrooms...', 'openclassrooms'),
            ('J\'ai besoin que tu me donnes l\'adresse de la Tour Eiffel, GrandPy!', 'tour eiffel'),
            ('Salut papy, peux-tu me dire comment rejoindre l\'Arc de Triomphe?', 'arc triomphe')
        ])
    def test_parse(self, input, expected):
        self.parser = script.Parser(input)
        self.parser.parse()
        assert self.parser.result == expected

class TestGoogleAPI:

    @pytest.mark.parametrize('input, expected', [
            ('openclassrooms', {'latitude': 48.8975156, 'longitude': 2.3833993}),
            ('tour eiffel', {'latitude': 48.85837009999999, 'longitude': 2.2944813}),
            ('arc triomphe', {'latitude': 48.8737917, 'longitude': 2.2950275}),
        ])
    def test_get_geodata(self, input, expected):
        self.google_api = script.GoogleAPI(input)
        self.google_api.get_geodata()
        assert self.google_api.geodata == expected

class TestMediaWikiAPI:

    def setup_method(self):
        self.mediawiki_api = script.MediaWikiAPI({'latitude': 48.8975156, 'longitude': 2.3833993})
        self.mediawiki_api.get_pageid()
        self.mediawiki_api.get_extract()

    def test_get_pageid(self, monkeypatch):
        def mock_result():
            return 3120649
        monkeypatch.setattr(script.MediaWikiAPI, 'get_pageid', mock_result)
        assert self.mediawiki_api.pageid == 3120649

    def test_get_extract(self, monkeypatch):
        def mock_result():
            return "Le quai de la Gironde est un quai situé le long du canal Saint-Denis, à Paris, dans le 19e arrondissement."
        monkeypatch.setattr(script.MediaWikiAPI, 'get_extract', mock_result)
        assert self.mediawiki_api.extract == "Le quai de la Gironde est un quai situé le long du canal Saint-Denis, à Paris, dans le 19e arrondissement."