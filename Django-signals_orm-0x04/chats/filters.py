from django_filters import rest_framework as filters
from .models import Message, User

class MessageFilter(filters.FilterSet):
    sent_at__gte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = filters.ModelChoiceFilter(queryset=User.objects.all(), field_name='sender__user_id')

    class Meta:
        model = Message
        fields = ['sent_at__gte', 'sent_at__lte', 'sender', 'conversation']