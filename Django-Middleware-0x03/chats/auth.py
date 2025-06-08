from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view to include user details in the response."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        serializer = UserSerializer(user)
        response.data['user'] = serializer.data
        return response