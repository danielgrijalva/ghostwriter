from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from brain.textgenrnn import textgenrnn


@api_view(['GET'])
def get_suggestions(request):
    t = textgenrnn()
    
    suggestions = t.generate(max_gen_length=280, top_n=5, temperature=2)
    
    return Response({'suggestions': suggestions})
