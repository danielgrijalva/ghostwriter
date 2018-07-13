from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def upper(request):
    text = request.query_params['text'].upper()

    return Response({'result': text})