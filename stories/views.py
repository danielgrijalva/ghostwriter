from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from brain.textgenrnn import textgenrnn


@api_view(['GET'])
def get_suggestions(request):
    t = textgenrnn()
    
    story = request.query_params.get('story')

    params = {
        'max_gen_length': 280,
        'top_n': 30,
        'story': story,
    }

    suggestions, probs = t.generate(**params)
        
    return Response({'suggestions': suggestions, 'probs': probs})
