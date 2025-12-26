from rest_framework import serializers
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ["created_by"]

    def validate_title(self, value):
        if value and len(value) > 50:
            raise serializers.ValidationError("Title should not exceed 50 letters")
        return value

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
