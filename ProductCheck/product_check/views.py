import io
import csv

from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import ProductFileSerializer, ProductDetailsSerializer
from .product_scraping import AmazonScrapper, WalmartScrapper, TargetScrapper, CostcoScrapper
from rest_framework.generics import CreateAPIView

scraping_class = {
    'amazon': AmazonScrapper,
    'walmart': WalmartScrapper,
    'target': TargetScrapper,
    'costco': CostcoScrapper,
}


class ProductDetailsAPIView(CreateAPIView):
    """
    Implements several methods to
    create, delete and modify product details
    by providing data through csv

    Returns:
        Scraped data and success http code.

    Raises:
        Exception: Raises an exception.
    """
    serializer_class = ProductFileSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = serializer.validated_data['file']
            decoded_file = file.read().decode()
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            data = []
            for row in reader:
                serializer = ProductDetailsSerializer(data=row)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                scrapper = scraping_class[row['product_category']](row['product_url'])
                data.append(scrapper.fetch_product_details())
            return Response(status=status.HTTP_200_OK, data=data)
        except Exception as err:
            raise err


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def result_page(request):
    try:
        file = request.FILES['csv_file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        data = []
        for row in reader:
            serializer = ProductDetailsSerializer(data=row)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            scrapper = scraping_class[row['product_category']](row['product_url'])
            data.append(scrapper.fetch_product_details())
        return render(request, "result_page.html", {'views': data})
    except Exception as err:
        raise err
