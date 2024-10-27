import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

from django.conf import settings
from .printful_api import PrintfulAPI
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import generate_text_image

from io import BytesIO
import json

import cloudinary
import cloudinary.uploader
import time

printful_api = PrintfulAPI()

logger = logging.getLogger(__name__)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        if not image.name.lower().endswith('.png'):
            return JsonResponse({'error': 'Only PNG files are allowed'}, status=400)

        try:
            # Generate a unique filename
            timestamp = int(time.time())
            original_name, extension = os.path.splitext(image.name)
            unique_filename = f"printful_mockup_{timestamp}_{original_name}"

            # Upload the image to Cloudinary
            upload_result = cloudinary.uploader.upload(
                image,
                public_id=unique_filename,
                folder="printful_mockups",
                use_filename=True,
                unique_filename=True,
                overwrite=False,
                resource_type="image",
                upload_preset="printful_mockups"
            )

            # Get the secure URL of the uploaded image
            image_url = upload_result['secure_url']

            return JsonResponse({
                'message': 'Image uploaded and shared successfully',
                'filename': f"{unique_filename}{extension}",
                'share_link': image_url
            })

        except cloudinary.exceptions.Error as e:
            logger.error(f"Cloudinary upload error: {str(e)}")
            return JsonResponse({'error': f'Failed to upload image: {str(e)}'}, status=500)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def create_printful_mockup(user_text, max_line_length=10):
    product_id = 438  # Example product ID for a T-shirt
    variant_id = 11562  # Example variant ID for a specific size/color of that T-shirt
    printful_api = PrintfulAPI()
    max_retries = 10
    retry_delay = 5

    try:
        # Generate the image
        image, warning_needed = generate_text_image(user_text, max_line_length=max_line_length)
        
        # Handle the warning_needed flag
        if warning_needed:
            logger.warning(f"Warning: Some words in '{user_text}' were too long to split or there were no logical breakpoints.")
            # You might want to add this warning to the return value or handle it in some other way

        # Convert PIL Image to InMemoryUploadedFile
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        image_file = InMemoryUploadedFile(
            image_io,
            None,
            f"{user_text.replace(' ', '_')}.png",
            'image/png',
            image_io.tell(),
            None
        )

        # Create a mock request object with the image file
        class MockRequest:
            method = 'POST'
            FILES = {'image': image_file}

        # Use the upload_image function
        upload_result = upload_image(MockRequest())

        if not isinstance(upload_result, JsonResponse):
            logger.error(f"Unexpected upload result type: {type(upload_result)}")
            return {"error": "Unexpected upload result type"}

        upload_data = json.loads(upload_result.content.decode('utf-8'))
        if 'share_link' not in upload_data:
            logger.error(f"Failed to get share link from upload result: {upload_data}")
            return {"error": "Failed to get share link from upload result"}

        # Use the Cloudinary URL for the Printful mockup
        image_url = upload_data['share_link']

        # Create the mockup and get task key
        mockup_response = printful_api.create_mockup(product_id, variant_id, image_url)

        if 'result' not in mockup_response or 'task_key' not in mockup_response['result']:
            logger.error(f"Unexpected mockup creation response: {mockup_response}")
            return {"error": "Unexpected mockup creation response"}

        task_key = mockup_response['result']['task_key']

        # Check mockup task status and get results
        for attempt in range(max_retries):
            mockup_results = printful_api.retrieve_mockup_results(task_key)

            if mockup_results and 'result' in mockup_results:
                status = mockup_results['result'].get('status')
                if status == 'completed':
                    if 'mockups' in mockup_results['result']:
                        return {
                            "task_key": task_key,
                            "image_url": image_url,
                            "filename": upload_data['filename'],
                            "mockups": mockup_results['result']['mockups']
                        }
                    else:
                        logger.error(f"Mockup completed but no mockups found: {mockup_results}")
                        return {"error": "Mockup completed but no mockups found"}
                elif status in ['failed', 'error']:
                    logger.error(f"Mockup task failed: {mockup_results}")
                    return {"error": f"Mockup task failed: {mockup_results['result'].get('error', 'Unknown error')}"}
                elif status == 'pending':
                    logger.info(f"Mockup task still pending. Attempt {attempt + 1}/{max_retries}")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Unknown mockup task status: {status}")
                    return {"error": f"Unknown mockup task status: {status}"}
            else:
                logger.error(f"Unexpected mockup results: {mockup_results}")
                return {"error": "Unexpected mockup results"}

        logger.error(f"Mockup task did not complete within {max_retries} attempts")
        return {"error": f"Mockup task did not complete within {max_retries} attempts"}

    except Exception as e:
        logger.exception(f"Error creating mockup: {str(e)}")
        return {"error": str(e)}