import os
import sys
import tempfile
import unittest
import types
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("NOCTURNE_DB", str(Path(tempfile.gettempdir()) / "nocturne_32_tests.db"))
sys.path.insert(0, str(ROOT))
# The build container may not have Flask installed. Stub only the decorators
# for offline unit testing; the application itself still requires Flask from
# requirements.txt when run by the user.
try:
    import flask  # noqa: F401
except ModuleNotFoundError:
    fake_flask = types.ModuleType("flask")
    class _FakeFlask:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda fn: fn
        def post(self, *args, **kwargs): return lambda fn: fn
        def delete(self, *args, **kwargs): return lambda fn: fn
    fake_flask.Flask = _FakeFlask
    fake_flask.jsonify = lambda value: value
    fake_flask.render_template_string = lambda *args, **kwargs: ""
    fake_flask.request = types.SimpleNamespace(args={})
    sys.modules["flask"] = fake_flask
import otakudesu_gothic as appmod  # noqa: E402


class ProviderNormalizationTests(unittest.TestCase):
    def test_first_list_handles_array_and_jsonapi(self):
        self.assertEqual(appmod._first_list([{"id": "1"}, "bad"]), [{"id": "1"}])
        self.assertEqual(appmod._first_list({"data": [{"id": "2"}]}), [{"id": "2"}])

    @patch.object(appmod, "_external_json")
    def test_kitsu_search_normalizes(self, get_json):
        get_json.return_value = {"data": [{"id": "44", "attributes": {
            "canonicalTitle": "Test Anime", "averageRating": "82.1", "posterImage": {"large": "https://img.example/a.jpg"},
            "startDate": "2024-01-01", "episodeCount": 12, "status": "finished"
        }}]}
        rows = appmod._kitsu_search("Test Anime")
        self.assertEqual(rows[0]["title"], "Test Anime")
        self.assertEqual(rows[0]["provider_id"], "44")
        self.assertIn("https://img.example", rows[0]["image"])

    @patch.object(appmod, "_external_json")
    def test_anipub_relative_image_is_completed(self, get_json):
        get_json.return_value = [{"id": 12, "Name": "Sample", "ImagePath": "/covers/a.jpg", "MALScore": "8.1"}]
        row = appmod._anipub_search("Sample")[0]
        self.assertEqual(row["provider_id"], 12)
        self.assertEqual(row["image"], "https://anipub.org/covers/a.jpg")

    @patch.object(appmod, "_external_json")
    def test_mitenime_search_handles_attributes(self, get_json):
        get_json.return_value = {"data": [{"slug": "sample-series", "attributes": {"title": "Sample", "poster": "https://img.example/p.jpg", "rating": 8.2}}]}
        row = appmod._mitenime_search("Sample")[0]
        self.assertEqual(row["provider_id"], "sample-series")
        self.assertEqual(row["title"], "Sample")

    @patch.object(appmod, "_external_json")
    def test_animap_mapping(self, get_json):
        get_json.return_value = [{"mal_id": 1, "anilist_id": [21], "kitsu_id": [18], "titles": ["Cowboy Bebop"], "year": 1998}]
        row = appmod._animap_search("Cowboy Bebop")[0]
        self.assertEqual(row["title"], "Cowboy Bebop")
        self.assertEqual(row["mapping"]["anilist_id"], [21])

    @patch.object(appmod, "_external_text")
    def test_ann_xml_parser(self, get_text):
        get_text.return_value = '<ann><anime id="13"><info type="Main title">Cowboy Bebop</info></anime></ann>'
        row = appmod._ann_search("Cowboy Bebop")[0]
        self.assertEqual(row["provider_id"], "13")
        self.assertEqual(row["title"], "Cowboy Bebop")


class AggregationTests(unittest.TestCase):
    @patch.object(appmod, "mal_search", return_value=[])
    @patch.object(appmod, "_ann_search", return_value=[])
    @patch.object(appmod, "_animap_search", return_value=[])
    @patch.object(appmod, "_mitenime_search", side_effect=RuntimeError("provider offline"))
    @patch.object(appmod, "_anipub_search", return_value=[])
    @patch.object(appmod, "_kitsu_search", return_value=[])
    @patch.object(appmod, "_anilist_search", return_value=[])
    def test_multisearch_keeps_other_providers_when_one_fails(self, *_mocks):
        result = appmod.multiverse_search("Naruto")
        self.assertEqual(result["query"], "Naruto")
        self.assertEqual(result["provider_count"], 6)
        self.assertFalse(result["providers"]["MiteNime"]["ok"])

    def test_multisearch_rejects_short_query(self):
        with self.assertRaises(ValueError):
            appmod.multiverse_search("a")

    def test_health_route(self):
        response = appmod.api_health()
        payload = response.get_json() if hasattr(response, "get_json") else response
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["app"], "NOCTURNE 3.2 Multiverse Archive")


if __name__ == "__main__":
    unittest.main(verbosity=2)
