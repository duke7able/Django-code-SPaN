from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import stock
from .serializers import StockSerializer
from bs4 import BeautifulSoup
import requests
import json

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
        query = request.POST['query']
        lang = request.POST['lang']
        enteredInput = query + lang
        keywords = enteredInput.split(' ')
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
                # print("loop 1")
            elif(soup.pre is not None):
                if(len(soup.pre.get_text().split('\n'))>0):
                    results.append(soup.pre.get_text().split('\n'))
                    methodUsed.append(2)
                    # print("loop 2")
            elif(len(soup.find_all('code'))>0):
                content = []
                for c in soup.find_all('code'):
                    content.append(c.text)
                results.append(content)
                methodUsed.append(3)
                # print("loop 3")

        r = json.dumps(results, sort_keys=True)
        return Response(r)
