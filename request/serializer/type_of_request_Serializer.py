from rest_framework import serializers
from request.models import typeRequest

class typeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeRequest
        fields = 'id','typerequest'