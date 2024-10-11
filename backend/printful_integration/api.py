import requests
from django.conf import settings
import base64

class PrintfulAPI:
    BASE_URL = 'https://api.printful.com'

    @staticmethod
    def get_headers():
        return {
            'Authorization': f'Bearer {settings.PRINTFUL_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    @classmethod
    def upload_image_and_create_order(cls, image_data, order_data):
        # First, upload the image
        upload_url = f'{cls.BASE_URL}/files'
        
        # Convert image data to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        upload_payload = {
            'file': image_base64,
            'type': 'default'
        }
        
        upload_response = requests.post(upload_url, json=upload_payload, headers=cls.get_headers())
        
        if upload_response.status_code != 200:
            return {'error': 'Failed to upload image', 'details': upload_response.json()}
        
        # Get the file ID from the upload response
        file_id = upload_response.json()['result']['id']
        
        # Now, create the order using the uploaded file
        order_url = f'{cls.BASE_URL}/orders'
        
        # Assuming order_data is a dictionary with the necessary order information
        # We'll add the file ID to the first item in the order
        if 'items' in order_data and len(order_data['items']) > 0:
            order_data['items'][0]['files'] = [{'id': file_id}]
        
        order_response = requests.post(order_url, json=order_data, headers=cls.get_headers())
        
        if order_response.status_code != 200:
            return {'error': 'Failed to create order', 'details': order_response.json()}
        
        return order_response.json()

    
    @classmethod
    def create_order(cls, order_data):
        url = f'{cls.BASE_URL}/orders'
        response = requests.post(url, json=order_data, headers=cls.get_headers())
        return response.json()

    # Add more methods for other API calls
