import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PrintfulAPI:
    BASE_URL = 'https://api.printful.com'

    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.PRINTFUL_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def create_mockup(self, product_id, variant_id, image_url):
        """Initiates a mockup generation task."""
        endpoint = f'{self.BASE_URL}/mockup-generator/create-task/{product_id}'
        payload = {
            "variant_ids": [variant_id],
            "format": "png",
            "files": [
                {
                    "placement": "front",
                    "image_url": image_url,
                    "position": {
                        "area_width": 1800,
                        "area_height": 2400,
                        "width": 1800,
                        "height": 2400,
                        "top": 0,
                        "left": 0
                    }
                }
            ]
        }
        return self._post_request(endpoint, payload)

    def check_mockup_task_status(self, task_key):
        """Checks the status of a mockup generation task."""
        endpoint = f'{self.BASE_URL}/mockup-generator/task'
        params = {'task_key': task_key}
        return self._get_request(endpoint, params)

    def retrieve_mockup_results(self, task_key):
        """Retrieves the results of a mockup generation task."""
        endpoint = f'{self.BASE_URL}/mockup-generator/task'
        params = {'task_key': task_key}
        return self._get_request(endpoint, params)

    def _post_request(self, endpoint, payload):
        """Helper method to send POST requests."""
        logger.debug(f"Sending POST request to {endpoint} with payload: {payload}")
        response = requests.post(endpoint, json=payload, headers=self.headers)
        
        if response.status_code != 200:
            logger.error(f"Printful API error: {response.status_code} - {response.text}")
            return response.json()
        
        return response.json()

    def _get_request(self, endpoint, params):
        """Helper method to send GET requests."""
        logger.debug(f"Sending GET request to {endpoint} with params: {params}")
        response = requests.get(endpoint, params=params, headers=self.headers)
        
        if response.status_code != 200:
            logger.error(f"Printful API error: {response.status_code} - {response.text}")
            return None
        
        return response.json()