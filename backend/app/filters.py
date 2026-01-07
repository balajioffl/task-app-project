import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:

        model = Task

        fields = ['status','priority','created_at']