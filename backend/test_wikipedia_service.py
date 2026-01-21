import sys
import os
import unittest

# Add backend directory to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.wikipedia_service import WikipediaService

class TestWikipediaService(unittest.TestCase):
    def setUp(self):
        self.service = WikipediaService()

    def test_search_location(self):
        results = self.service.search_location("Paris")
        self.assertTrue(len(results) > 0)
        self.assertIn("Paris", results)

    def test_get_location_details_paris(self):
        details = self.service.get_location_details("Paris")
        self.assertNotIn("error", details)
        self.assertEqual(details["title"], "Paris")
        self.assertIsNotNone(details["coordinates"])
        self.assertTrue(isinstance(details["coordinates"]["lat"], float))
        self.assertTrue(isinstance(details["coordinates"]["lon"], float))

    def test_page_not_found(self):
        details = self.service.get_location_details("ThisPageDefinitelyDoesNotExist12345")
        self.assertIn("error", details)
        self.assertEqual(details["error"], "Page not found")

if __name__ == '__main__':
    unittest.main()
