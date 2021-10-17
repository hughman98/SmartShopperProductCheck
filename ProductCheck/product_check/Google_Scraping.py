"""
Scraping multiple ecommerce sites to obtain poduct links using serpAPI

"""

from bs4 import element
from requests import NullHandler
from serpapi import GoogleSearch
from .product_scraping import AmazonScrapper, WalmartScrapper, TargetScrapper, CostcoScrapper
from django.conf import settings
from googlesearch import search


class GoogleScraping:
    """
    Scrapes product urls from google search and google shopping using SerpAPI.

    """

    def __init__(self):
        self.results = {}
        self.apiKey = "372726d62f51909d9141009c3c0788837f8deef52fcacfd394bff687d320a958"
        self.Amazon = "Amazon"
        self.Target = "Target"
        self.Costco = "Costco"
        self.Walmart = "Walmart"

    def free_search(self, query):
        """
        Scrapes Product URLS without using the SerpAPI, so that they're free.
        Returns a list of URLS from Amazon, Target, Costco, and Walmart
        """
        results = []
        sites = ["amazon", "target", "costco", "walmart"]

        for site in sites:
          for url in search(query + " " + site, tld="co.in", num=1, stop=1):
            results.append(url)

        return results

    # return the results scraped from google search
    def searchQueryShop(self, key, store):

        params = {
            "tbm": "shop",
            "hl": "en",
            "gl": "us",
            "engine": "google",
            "q": key + " " + store,
            "api_key": self.apiKey
        }
        search = GoogleSearch(params)
        self.results = search.get_dict()
        return self.results

    # return the results scraped from Google Shopping
    def searchQuery(self, key, store):
        params = {
            "hl": "en",
            "gl": "us",
            "engine": "google",
            "q": key + " " + store,
            "api_key": self.apiKey
        }
        search = GoogleSearch(params)
        self.results = search.get_dict()
        return self.results

    # returns product links from google search
    def GoogleSearch(self, results, store):
        links = []

        def shoppingResults():
            try:
                for i in range(0, len(results["shopping_results"])):
                    if store in results["shopping_results"][i]["source"]:
                        links.append(results["shopping_results"][i]["link"])
            except:
                pass

        def organicResultsInline():
            try:
                organicResults = []
                for i in range(0, len(results["organic_results"])):
                    organicResults.append(results["organic_results"][i])
                inlineOrganicResults = organicResults[0]["sitelinks"]["inline"]
                for i in range(0, len(inlineOrganicResults)):
                    if store in inlineOrganicResults[i]["link"]:
                        links.append(inlineOrganicResults[i]["link"])
            except:
                pass

        def organicresultsExpanded():
            try:
                organicResults = []
                for i in range(0, len(results["organic_results"])):
                    organicResults.append(results["organic_results"][i])
                inlineOrganicResults = organicResults[0]["sitelinks"]["expanded"]
                for i in range(0, len(inlineOrganicResults)):
                    if store in inlineOrganicResults[i]["link"]:
                        links.append(inlineOrganicResults[i]["link"])
            except:
                pass

        organicResultsInline()
        organicresultsExpanded()
        shoppingResults()
        return links

    # return product links from google shopping
    def GoogleSearchShop(self, results, store):
        links = []

        def shoppingResults():
            try:
                for i in range(0, len(results['shopping_results'])):
                    if store in results['shopping_results'][i]['source']:
                        links.append(results['shopping_results'][i]['link'])
            except:
                pass

        def shoppingResultsInline():
            try:
                for i in range(0, len(results['inline_shopping_results'])):
                    if store in results['inline_shopping_results'][i]['source']:
                        links.append(results['inline_shopping_results'][i]['link'])
            except:
                pass

        shoppingResults()
        shoppingResultsInline()

        return links

    def callSearch(self, key):
        links = []
        data = []
        ref = GoogleScraping()
        resShop = ref.searchQueryShop(key, self.Amazon)
        resSearch = ref.searchQuery(key, self.Amazon)
        links = links + ref.GoogleSearchShop(resShop, self.Amazon)
        links = links + ref.GoogleSearch(resSearch, self.Amazon)
        if len(links) > 5:
            for i in range(0, 5):
                amazonScrapper = AmazonScrapper(links[i])
                data.append(amazonScrapper.fetch_product_details())
        else:
            for i in range(0, len(links)):
                amazonScrapper = AmazonScrapper(links[i])
                data.append(amazonScrapper.fetch_product_details())

        links = []
        resShop = ref.searchQueryShop(key, self.Target)
        resSearch = ref.searchQuery(key, self.Target)
        links = links + ref.GoogleSearchShop(resShop, self.Target)
        links = links + ref.GoogleSearch(resSearch, self.Target)
        if len(links) > 5:
            for i in range(0, 5):
                targetScrapper = TargetScrapper(links[i])
                data.append(targetScrapper.fetch_product_details())
        else:
            for i in range(0, len(links)):
                targetScrapper = TargetScrapper(links[i])
                data.append(targetScrapper.fetch_product_details())

        links = []
        resShop = ref.searchQueryShop(key, self.Walmart)
        resSearch = ref.searchQuery(key, self.Walmart)
        links = links + ref.GoogleSearchShop(resShop, self.Walmart)
        links = links + ref.GoogleSearch(resSearch, self.Walmart)
        if (len(links) > 5):
            for i in range(0, 5):
                walmartScrapper = WalmartScrapper(links[i])
                data.append(walmartScrapper.fetch_product_details())
        else:
            for i in range(0, len(links)):
                walmartScrapper = WalmartScrapper(links[i])
                data.append(walmartScrapper.fetch_product_details())

        links = []
        resShop = ref.searchQueryShop(key, self.Costco)
        resSearch = ref.searchQuery(key, self.Costco)
        links = links + ref.GoogleSearchShop(resShop, self.Costco)
        links = links + ref.GoogleSearch(resSearch, self.Costco)
        if len(links) > 5:
            for i in range(0, 5):
                costcoscrapper = CostcoScrapper(links[i])
                data.append(costcoscrapper.fetch_product_details())
        else:
            for i in range(0, len(links)):
                costcoscrapper = CostcoScrapper(links[i])
                data.append(costcoscrapper.fetch_product_details())

        return data
