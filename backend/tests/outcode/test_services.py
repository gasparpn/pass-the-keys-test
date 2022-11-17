import json
from unittest.mock import patch

from django.test import TestCase

from backend.outcode import services


class OutcodeServiceTestCase(TestCase):

    def test_get_outcode_listings_from_output_file_return_expected_outcode(self):
        with self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'):
            listings = services.get_outcode_listings_from_output_file('M4')
            self.assertIsInstance(listings, list)
            self.assertEqual(len(listings), 1)
            self.assertEqual(listings[0]['id'], '310742')

    def test_get_nearest_outcodes_return_list_of_out_codes(self):
        with (
            patch('backend.outcode.services.requests.get') as mock_get,
            open('backend/tests/fixtures/nearest_outcode.json') as file
        ):
            mock_get.return_value.json.return_value = json.load(file)
            outcodes = services.get_nearest_outcodes('M4')
            self.assertIsInstance(outcodes, list)
            self.assertEqual(len(outcodes), 8)
            self.assertIn('M30', outcodes)

    def test_get_average_daily_price_return_average(self):
        with self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'):
            listings = services.get_outcode_listings_from_output_file('M4')
            self.assertEqual(services.get_average_daily_price(listings), 34.0)

    def test_get_average_daily_price_return_zero_when_list_is_empty(self):
        with self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'):
            self.assertEqual(services.get_average_daily_price([]), 0.0)

    def test_get_outcodes_informations_return_outcode_data(self):
        with self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'):
            listings = []
            listings.append(services.get_outcode_listings_from_output_file('M4'))
            listings.append(services.get_outcode_listings_from_output_file('M7'))
            outcodes_informations = services.get_outcodes_informations(listings)
            self.assertEqual(len(outcodes_informations), 2)
            self.assertEqual(outcodes_informations[0]['average-daily-price'], 34.0)
