import json
import xml.etree.ElementTree as ET
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class OutCodeViewTestCase(TestCase):

    def test_get_return_listings_information_according_to_outcode(self):
        client = APIClient()
        with (self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'),
              patch('backend.outcode.services.requests')):
            response = client.get('/api/outcode/M4/')
            content = response.content.decode()
            root = ET.fromstring(content)
            self.assertEqual(root[0].tag, 'listing-count')
            self.assertEqual(root[0].text, '1')
            self.assertEqual(root[1].tag, 'average-daily-price')
            self.assertEqual(root[1].text, '34.0')

    def test_get_return_404_error_when_information_not_found_for_the_outcode(self):
        client = APIClient()
        with (self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'),
              patch('backend.outcode.services.requests')):
            response = client.get('/api/outcode/M212124/')
            self.assertEqual(response.status_code, 404)


class OutCodeViewTestCase(TestCase):

    def test_get_return_nearest_listings_information_according_to_outcode(self):
        client = APIClient()
        with (self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'),
              patch('backend.outcode.services.requests.get') as mock_get,
              open('backend/tests/fixtures/nearest_outcode.json') as response_file):
            mock_get.return_value.json.return_value = json.load(response_file)
            response = client.get('/api/nexus/M4/')
            content = response.content.decode()
            root = ET.fromstring(content)
            self.assertEqual(root[0][0].tag, 'listing-count')
            self.assertEqual(root[0][0].text, '1')
            self.assertEqual(root[0][1].tag, 'average-daily-price')
            self.assertEqual(root[0][1].text, '41.0')
            self.assertEqual(root[0][2].tag, 'nexus')
            self.assertEqual(root[0][2].text, 'M50')

    def test_get_return_404_error_when_information_not_found_for_the_outcode(self):
        client = APIClient()
        with (self.settings(OUTPUT_FILE_NAME='backend/tests/fixtures/output_file.csv'),
              patch('backend.outcode.services.requests.get') as mock_get,
              open('backend/tests/fixtures/nearest_outcode.json') as response_file):
            mock_get.return_value.json.return_value = {'result': []}
            response = client.get('/api/nexus/M212124/')
            self.assertEqual(response.status_code, 404)