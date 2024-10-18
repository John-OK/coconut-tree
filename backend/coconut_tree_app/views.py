from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import UserInput
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

def send_the_homepage(request):
    print('home')
    theIndex = open('static/index.html').read()
    return HttpResponse(theIndex)

@api_view(['POST'])
def user_answer(request):
    if request.method == 'POST':
        try:
            user_input = request.data.get('answer')

            # Try to get the existing entry or create a new one
            input_entry, created = UserInput.objects.get_or_create(
                input_text=user_input,
                defaults={'count': 1}
            )

            if not created:
                # If the entry already existed, increment the count
                input_entry.count = F('count') + 1
                input_entry.save()

            # Refresh from db to get the updated count
            input_entry.refresh_from_db()

            # Get top 100 inputs ordered by count
            top_inputs = UserInput.objects.order_by('-count')[:15].values('input_text', 'count')

            return Response({
                'status': 'success',
                'message': 'Answer received and processed',
                'input': input_entry.input_text,
                'count': input_entry.count,
                'top_inputs': list(top_inputs)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)