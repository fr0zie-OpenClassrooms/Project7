import app.models as script
import pytest
import requests
from unittest.mock import Mock


class TestParser:
    @pytest.mark.parametrize(
        "input, expected",
        [
            (
                "Hello GrandPy! Je cherche l'adresse d'OpenClassrooms...",
                "openclassrooms",
            ),
            (
                "J'ai besoin que tu me donnes l'adresse de la Tour Eiffel, GrandPy!",
                "tour eiffel",
            ),
            (
                "Salut papy, peux-tu me dire comment rejoindre l'Arc de Triomphe?",
                "arc triomphe",
            ),
        ],
    )
    def test_parse(self, input, expected):
        self.parser = script.Parser(input)
        assert self.parser.result == expected


class TestGoogleAPI:
    def test_get_geodata(self, monkeypatch):
        def get(url, params):
            values = [
                {
                    "results": [
                        {
                            "formatted_address": "10 Quai de la Charente, 75019 Paris, France",
                            "geometry": {
                                "location": {"lat": 48.8975156, "lng": 2.3833993},
                            },
                        }
                    ]
                }
            ]
            mock = Mock()
            mock.json.side_effect = values
            return mock

        monkeypatch.setattr(requests, "get", get)
        self.google_api = script.GoogleAPI("openclassrooms")
        assert self.google_api.geodata == {
            "address": "10 Quai de la Charente, 75019 Paris, France",
            "latitude": 48.8975156,
            "longitude": 2.3833993,
        }


class TestMediaWikiAPI:
    def test_get_extract(self, monkeypatch):
        values = [
            {"query": {"geosearch": [{"pageid": 3120649}]}},
            {
                "query": {
                    "pages": {
                        "3120649": {
                            "extract": "Le quai de la Gironde",
                        }
                    }
                }
            },
        ]
        mock = Mock()
        mock.json.side_effect = values

        def get(url, params):
            return mock

        monkeypatch.setattr(requests, "get", get)
        self.mediawiki_api = script.MediaWikiAPI(
            {"latitude": 48.8975156, "longitude": 2.3833993}
        )
        assert isinstance(self.mediawiki_api.extract, str)
        assert self.mediawiki_api.extract.startswith("Le quai de la Gironde")
