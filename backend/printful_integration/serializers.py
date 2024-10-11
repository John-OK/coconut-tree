from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    # Define fields according to your order structure
    recipient_name = serializers.CharField(max_length=100)
    recipient_address = serializers.CharField(max_length=200)
    # Add other necessary fields
