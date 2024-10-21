import unittest
from src.components.external import External

class TestExternalFetchData(unittest.TestCase):
    
    def test_fetch_data_valid_date(self):
        external = External()
        response_df = external.fetch_data("2024-02-01")
        self.assertIsNotNone(response_df)
        self.assertGreater(len(response_df), 0)

    def test_fetch_data_invalid_date(self):
        external = External()
        with self.assertRaises(ValueError):
            external.fetch_data("invalid-date")

