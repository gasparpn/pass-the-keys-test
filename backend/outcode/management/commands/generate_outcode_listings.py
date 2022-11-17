import csv

import requests

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        write_outcode_to_listings_file()


def write_outcode_to_listings_file():
    postcode_data = get_postcode_data(settings.INPUT_FILE_NAME)
    with (
        open('backend/listings.csv') as read_csvfile,
        open(settings.OUTPUT_FILE_NAME, 'w') as write_csvfile, ):
        reader = csv.DictReader(read_csvfile, delimiter=',')
        field_names = reader.fieldnames
        field_names.append('outcode')
        writer = csv.DictWriter(write_csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in reader:
            row['outcode'] = None
            for item in postcode_data:
                if item['query']['latitude'] == row['latitude'] and item['query']['longitude'] == row['longitude']:
                    try:
                        row['outcode'] = item['result'][0]['postcode'].split(' ')[0]
                    except TypeError:  # No information about the outcode was found
                        pass
            writer.writerow(row)


def get_postcode_data(path_to_listing_file: str):
    with open(path_to_listing_file) as read_csvfile:
        reader: csv.DictReader = csv.DictReader(read_csvfile, delimiter=',')
        data: dict = {}
        for index, row in enumerate(reader):
            data[f'geolocations[{index}][longitude]'] = row.get('longitude')
            data[f'geolocations[{index}][latitude]'] = row.get('latitude')
            data[f'geolocations[{index}][radius]'] = 100
            data[f'geolocations[{index}][limit]'] = 1

        response = requests.post(settings.POSTCODE_URL, data=data)
        return response.json()['result']