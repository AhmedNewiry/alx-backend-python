from django.http import HttpResponseForbidden
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# Configure logging to write to requests.log
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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Restrict access outside 9 AM to 6 PM."""
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour >= 18:
            return HttpResponseForbidden("Access restricted outside 9 AM - 6 PM")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
        self.request_counts = defaultdict(lambda: {'count': 0, 'reset_time': datetime.now()})
        self.MAX_REQUESTS = 5
        self.WINDOW_SECONDS = 60

    def __call__(self, request):
        """Limit POST requests to 5 per minute per IP address."""
        if request.method == 'POST' and 'messages' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            record = self.request_counts[ip_address]
            now = datetime.now()

            # Reset count if window has expired
            if now >= record['reset_time']:
                record['count'] = 0
                record['reset_time'] = now + timedelta(seconds=self.WINDOW_SECONDS)

            record['count'] += 1
            self.request_counts[ip_address] = record

            if record['count'] > self.MAX_REQUESTS:
                return HttpResponseForbidden("Too many messages sent. Please wait before sending more.")

        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Restrict actions to users with admin or moderator roles."""
        if request.method in ['PUT', 'PATCH', 'DELETE'] and 'messages' in request.path:
            if not request.user.is_authenticated or request.user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Admin or moderator role required")
        response = self.get_response(request)
        return response