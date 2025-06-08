from django.http import HttpResponse
import logging
from datetime import datetime

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Log the request details and pass the request to the next middleware/view."""
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response