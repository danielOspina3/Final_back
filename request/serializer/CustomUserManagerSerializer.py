from rest_framework import serializers
from request.models import CustomerUser
from ..models import CustomerUser
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomerUser
        fields = ('id','email','password','name','last_name','document_type','num_document','role','is_active')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
      
        user = CustomerUser.objects.create_user(**validated_data)
        user.save()
        return user
        
class CustomerUserIsActive(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['is_active']

class CustomerUserIsAdmin(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['is_admin']


class CustomUserSerializerRole(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'role']  # Incluye solo los campos necesarios
