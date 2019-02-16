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

class codespanview(APIView):

    def get(self, request):
        return Response("Currently no GET queries please")

    ###
    #   Params of POST method of stockList
    #   'query' for actual query
    #   'lang' for specifing the language of programming
    #

    def post(self, request):
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        #Set the headers
        headers = {'User-Agent': userAgent}
        query = request.POST['query']
        lang = request.POST['lang']
        enteredInput = query + ' ' + lang
        keywords = enteredInput.split(' ')
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
        for url in varForCombiningModules:
            Query = url
            r = requests.get(Query)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            block = []
            if(len(soup.find_all('pre'))>1):
                content = []
                for c in soup.find_all('pre'):
                    content.append(c.text)
                block.append("one")
                block.append(content)
            elif(soup.pre is not None):
                if(len(soup.pre.get_text().split('\n'))>0):
                    block.append("two")
                    block.append(soup.pre.get_text().split('\n'))
            elif(len(soup.find_all('code'))>0):
                content = []
                for c in soup.find_all('code'):
                    content.append(c.text)
                block.append("three")
                block.append(content)

            # combing it up here
            if not block:
                continue
            block.append(url)
            results.append(block)

        outputBuff  = []
        outputBuff.append(results)
        r = json.dumps(outputBuff, sort_keys=True)
        return Response(r)
