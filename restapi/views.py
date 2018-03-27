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
        for link in soup.find_all('h3', class_='r'):
            test = link.a.get('href').split('q=')[1].split('&')[0]
            Id = 'id' + str(counter)
            counter = counter + 1
            resultedUrl2[Id] = test
            # resultedUrl2.append(test)

        dicti = {'asd': 'dfg', 'zcx': 'dh'}
        r = json.dumps(resultedUrl2)
        # works
        # except (KeyError, Choice.DoesNotExist):
        # # Redisplay the question voting form.
        #     return render(request, 'polls/detail.html', {
        #         'question': question,
        #         'error_message': "You didn't select a choice.",
        #     })
        # else:
        # selected_choice.votes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # somethingExtra = query + "abcd"
        return Response(r)
