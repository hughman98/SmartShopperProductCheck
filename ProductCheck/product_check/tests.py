import csv
from django.test import TestCase
from .models import Product
from .product_scraping import AmazonScrapper, WalmartScrapper, TargetScrapper, CostcoScrapper
from .views import scraping_class
from .utilities import mail_user
from .Google_Scraping import GoogleScraping,GoogleSearch


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(product_url="https://www.amazon.com/", product_category="amazon", is_active=False)
        Product.objects.create(product_url="https://www.walmart.com/", product_category="walmart", is_active=False)

    def test_product_details(self):
        """Created instances are retrieved and respective categories are verified"""
        amazon_product = Product.objects.get(product_url="https://www.amazon.com/")
        walmart_product = Product.objects.get(product_url="https://www.walmart.com/")
        self.assertEqual(amazon_product.product_category, "amazon")
        self.assertEqual(walmart_product.product_category, "walmart")

    def test_product_details_post(self):
        """Test for ProductDetailsAPIView post method """
        test_file = open('product_check/test_data/test_data.csv', 'r')
        response = self.client.post('/product_check/details/', {'file': test_file})
        self.assertEqual(response.status_code, 200)

    def test_amazon_scrapper(self):
        """Test for Amazon Scrapper class """
        test_file = csv.DictReader(open('product_check/test_data/amazon_test_data.csv', 'r'))
        for row in test_file:
            scrapper = scraping_class[row['product_category']](row['product_url'])
            data = scrapper.fetch_product_details()
            self.assertEqual(data.get('product_url'), row['product_url'])

    def test_walmart_scrapper(self):
        """Test for Walmart Scrapper class """
        test_file = csv.DictReader(open('product_check/test_data/walmart_test_data.csv', 'r'))
        for row in test_file:
            scrapper = scraping_class[row['product_category']](row['product_url'])
            data = scrapper.fetch_product_details()
            self.assertEqual(data.get('product_url'), row['product_url'])

    def test_target_scrapper(self):
        """Test for Target Scrapper class """
        test_file = csv.DictReader(open('product_check/test_data/target_test_data.csv', 'r'))
        for row in test_file:
            scrapper = scraping_class[row['product_category']](row['product_url'])
            data = scrapper.fetch_product_details()
            self.assertEqual(data.get('product_url'), row['product_url'])

    def test_costco_scrapper(self):
        """Test for Costco Scrapper class """
        test_file = csv.DictReader(open('product_check/test_data/costco_test_data.csv', 'r'))
        for row in test_file:
            scrapper = scraping_class[row['product_category']](row['product_url'])
            data = scrapper.fetch_product_details()
            self.assertEqual(data.get('product_url'), row['product_url'])

    def test_mail_user(self):
        """Test for mail_user function in utilities.py """
        test_file = csv.DictReader(open('product_check/test_data/test_data.csv', 'r'))
        for row in test_file:
            mail_user(row)
            self.assertEqual(row.get('product_url'), row['product_url'])

    def test_target_google_search_scrapper(self):
        """Test for Google scrapping to get links on target"""
        instance = GoogleScraping()
        result1 = instance.searchQuery("Coffee","Target.com")
        result2 = instance.searchQueryShop("Coffee","Target.com")
        instance.GoogleSearch(result1,"Target.com")
        instance.GoogleSearchShop(result2,"Target.com")
        # check if returning scraped links
        self.assertTrue(len(result1) or len(result2))
    
    def test_walmart_google_search_scrapper(self):
        """Test for Google scrapping to get links on walmart"""
        instance = GoogleScraping()
        result1 = instance.searchQuery("Coffee","Walmart.com")
        result2 = instance.searchQueryShop("Coffee","Walmart.com")
        instance.GoogleSearch(result1,"Walmart.com")
        instance.GoogleSearchShop(result2,"Walmart.com")
        # check if returning scraped links
        self.assertTrue(len(result1) or len(result2))
    
    def test_amazon_google_search_scrapper(self):
        """Test for Google scrapping to get links on amazon"""
        instance = GoogleScraping()
        result1 = instance.searchQuery("Coffee","Amazon.com")
        result2 = instance.searchQueryShop("Coffee","Amazon.com")
        instance.GoogleSearch(result1,"Amazon.com")
        instance.GoogleSearchShop(result2,"Amazon.com")
        # check if returning scraped links
        self.assertTrue(len(result1) or len(result2))
    
    def test_costco_google_search_scrapper(self):
        """Test for Google scrapping to get links on costco"""
        instance = GoogleScraping()
        result1 = instance.searchQuery("Coffee","Costco.com")
        result2 = instance.searchQueryShop("Coffee","Costco.com")
        instance.GoogleSearch(result1,"Costco.com")
        instance.GoogleSearchShop(result2,"Costco.com")
        # check if returning scraped links
        self.assertTrue(len(result1) or len(result2))
