from django.http import JsonResponse
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .api import PrintfulAPI
from .serializers import OrderSerializer

# This view is just an example of how to use the Printful API.
# It should not be used. Instead, a separate function for each
# Printful API endpoint should be created.
def printful_proxy(request):

    if request.method == 'POST':
        endpoint = request.POST.get('endpoint')
        data = request.POST.get('data')

        headers = {
            'Authorization': f'Bearer {settings.PRINTFUL_API_TOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.post(f'https://api.printful.com/{endpoint}', headers=headers, json=data)
        
        return JsonResponse(response.json())

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_printful_order(request):
    if request.method == 'POST':
        order_data = request.POST.get('order_data')
        result = PrintfulAPI.create_order(order_data)
        return JsonResponse(result)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_with_image(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        try:
            image_file = request.FILES.get('image')
            if not image_file:
                return Response({'error': 'Image file is required'}, status=status.HTTP_400_BAD_REQUEST)

            image_data = image_file.read()
            order_data = serializer.validated_data

            result = PrintfulAPI.upload_image_and_create_order(image_data, order_data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
