from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import stock
from .serializers import StockSerializer
from bs4 import BeautifulSoup
import requests
import json
import random
from lxml.html import fromstring

# Create your views here.
# Lists all stocks or create a new one
# stocks/
#
# def some(request):
#     print(request)
#     print(request.method)
#     # print(request.data)
#     return HttpResponseRedirect('/admin')

class codespanview(APIView):

    def get(self, request):
        serializer = StockSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        stocks = stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    ###
    #   Params of POST method of stockList
    #   'query' for actual query
    #   'lang' for specifing the language of programming
    #

    def post(self, request):
        # obj = request.data
        # st = stock()
        # serializer = StockSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # try:
        # proxies = [
        # '217.61.107.28:3128',
        # '151.80.140.233:54566',
        # '217.61.107.28:3128',
        # '151.80.140.233:54566',
        # '46.8.119.71:53281',
        # '160.16.127.184:3128',
        # '159.65.0.210:3128',
        # '217.9.94.145:8080'
        # ]
        # def get_proxies():
        #     url = 'https://free-proxy-list.net/'
        #     response = requests.get(url)
        #     parser = fromstring(response.text)
        #     proxies = []
        #     for i in parser.xpath('//tbody/tr')[:10]:
        #         if i.xpath('.//td[7][contains(text(),"yes")]'):
        #             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        #             proxies.append(proxy)
        #     return proxies
        #
        # proxies = get_proxies()
        # proxy = random.choice(proxies)
        # proxy = proxy.split(':')[0]
        # print(proxy)
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        #Set the headers
        headers = {'User-Agent': userAgent}
        query = request.POST['query']
        lang = request.POST['lang']
        keywords = []
        keywords.append(query)
        keywords.append(lang)
        # for making less obviuos queries
        random.shuffle(keywords)
        resultedUrl2 = {}
        defaultUrl = "https://www.google.co.in/search?q="
        for key in keywords:
            defaultUrl = defaultUrl + '+' + key
        Query = defaultUrl.replace('+', "", 1)
        r = requests.get(Query)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        counter = 0
        varForCombiningModules = []
        for link in soup.find_all('h3', class_='r'):
            test = link.a.get('href').split('q=')[1].split('&')[0]
            Id = 'id' + str(counter)
            counter = counter + 1
            resultedUrl2[Id] = test
            varForCombiningModules.append(test)
            # resultedUrl2.append(test)
        results = []
        methodUsed = []
        urls = []
        for url in varForCombiningModules:
            Query = url
            r = requests.get(Query)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            if(len(soup.find_all('pre'))>0):
                content = []
                for c in soup.find_all('pre'):
                    content.append(c.text)
                results.append(content)
                methodUsed.append(1)
                urls.append(url)
                # print("loop 1")
            elif(soup.pre is not None):
                if(len(soup.pre.get_text().split('\n'))>0):
                    results.append(soup.pre.get_text().split('\n'))
                    methodUsed.append(2)
                    urls.append(url)
                    # print("loop 2")
            elif(len(soup.find_all('code'))>0):
                content = []
                for c in soup.find_all('code'):
                    content.append(c.text)
                results.append(content)
                methodUsed.append(3)
                urls.append(url)
                # print("loop 3")

        outputBuff  = []
        outputBuff.append(results)
        outputBuff.append(urls)
        r = json.dumps(outputBuff, sort_keys=True)
        return Response(r)
