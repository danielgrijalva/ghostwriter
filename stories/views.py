from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from brain.textgenrnn import textgenrnn


@api_view(['GET'])
def get_suggestions(request):
    t = textgenrnn()

    next_word = request.query_params.get('nextWord')
    story = request.query_params.get('story')

    if next_word == settings.META_TOKEN:
        return Response({'suggestions': None, 'story': story})

    params = {
        'max_gen_length': 280,
        'top_n': int(request.query_params.get('topN')),
        'random': False,
        'story': story,
        'next_word': next_word,
    }

    suggestions = t.generate(**params)
        
    return Response({'suggestions': suggestions})
