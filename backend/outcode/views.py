import csv

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



class GetOutCode(APIView):

    def get(self, request, outcode: str):
        listings = []
        with open(settings.OUTPUT_FILE_NAME, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                if row['outcode'] == outcode:
                    listings.append(row)

        if not listings:
            data = {
                'error': f'No information found for the outcode {outcode}'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        price_sum: float = 0.0
        for item in listings:
            price_sum += float(item['price'])

        data = {
            'listing-count': len(listings),
            'average-daily-price': price_sum/len(listings),
            'outcode': outcode,
        }

        return Response(data)


class GetNearOutCode(APIView):

    def get(self, request, outcode: str):
        return Response({'test': outcode})

