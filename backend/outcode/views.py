import itertools

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .services import (
    get_average_daily_price,
    get_nearest_outcodes,
    get_outcode_listings_from_output_file,
    get_outcodes_informations,
)


class OutCodeView(APIView):

    def get(self, request, outcode: str):
        listings = get_outcode_listings_from_output_file(outcode)

        if not listings:
            data = {
                'error': f'No information found for the outcode {outcode}'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        average_daily_price = get_average_daily_price(listings)
        data = {
            'listing-count': len(listings),
            'average-daily-price': average_daily_price,
            'outcode': outcode,
        }

        return Response(data)


class NearestOutCodeView(APIView):

    def get(self, request, outcode: str):
        outcodes: list = get_nearest_outcodes(outcode)
        if not outcodes:
            data = {
                'error': f'No information found for the outcode {outcode}'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        listings: list = []
        for outcode in outcodes:
            listings.append(get_outcode_listings_from_output_file(outcode))

        listings = [item for item in listings if len(item) > 0]  # Remove empty lists

        nearest_outcodes = get_outcodes_informations(listings)

        overall_values = {}
        # Merge all lists to get overall information
        flatten_listings = list(itertools.chain(*listings))
        average_daily_price = get_average_daily_price(flatten_listings)

        overall_values['listing-count'] = len(flatten_listings)
        overall_values['average-daily-price'] = average_daily_price
        overall_values['nexus'] = outcode
        overall_values['nearest_outcodes'] = nearest_outcodes

        return Response({'list': overall_values})

