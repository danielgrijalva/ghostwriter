from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_suggestions(request):
    text = request.query_params['text']

    suggestions = None
    
    # testing stuff
    if text.startswith('t'):
        suggestions = ['Tree', 'The', 'To']
    elif text.startswith('s'):
        suggestions = ['Some', 'She', 'Sometimes']
    
    return Response({'result': suggestions})