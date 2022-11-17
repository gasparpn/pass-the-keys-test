import csv

import requests
from django.conf import settings


def get_outcode_listings_from_output_file(outcode: str) -> list:
    listings = []
    with open(settings.OUTPUT_FILE_NAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            if row['outcode'] == outcode:
                listings.append(row)
    return listings


def get_nearest_outcodes(outcode: str):
    url: str = f'{settings.POSTCODE_BASE_URL}outcodes/{outcode}/nearest'
    outcodes: list = []

    response = requests.get(url)
    outcodes_data = response.json().get('result')
    if outcodes_data is None:
        return outcodes
    for item in response.json().get('result'):
        outcodes.append(item.get('outcode'))
    return outcodes


def get_average_daily_price(listings: list[dict]) -> float:
    price_sum: float = 0.0
    if len(listings) == 0:
        return price_sum
    for item in listings:
        price_sum += float(item['price'])
    return round(price_sum/len(listings), 2)


def get_outcodes_informations(listings: list) -> list[dict]:
    nearest_outcodes: list = []

    # Organize nearest outcode information
    for listing in listings:
        average_daily_price = get_average_daily_price(listing)

        nearest_outcodes.append({
            'listing-count': len(listing),
            'average-daily-price': average_daily_price,
            'outcode': listing[0]['outcode'],
        })

    return nearest_outcodes
