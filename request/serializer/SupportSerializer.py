from rest_framework import serializers
from request.models import Support
from request.models import Ips,CustomerUser,typeRequest,SubtypeRequest
from .ips_serializer import IpsSerializer
from .type_of_request_Serializer import typeRequestSerializer
from .Subtype_of_request_Serializer import SubtypeRequestSerializer
from .CustomUserManagerSerializer import CustomUserSerializer


class SupportSerializer(serializers.ModelSerializer):
    
    id_type_request_id = serializers.PrimaryKeyRelatedField(queryset=typeRequest.objects.all(), source='typerequest_id', write_only=True, required=False, allow_null=True)
    typerequest_id = typeRequestSerializer(read_only=True)
    
    id_Subtype_request_id = serializers.PrimaryKeyRelatedField(queryset=SubtypeRequest.objects.all(), source='subtype_request', write_only=True, required=False, allow_null=True)
    subtype_request = SubtypeRequestSerializer(read_only=True)
    
    id_ips_id = serializers.PrimaryKeyRelatedField(queryset=Ips.objects.all(), source='id_ips', write_only=True, required=False, allow_null=True)
    id_ips = IpsSerializer(read_only=True)
    
    id_CustomerUser_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerUser.objects.all(), source='id_CustomerUser', write_only=True, required=False, allow_null=True)
    id_CustomerUser = CustomUserSerializer(read_only=True)
    
    id_CustomerUser2_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerUser.objects.all(), source='id_CustomerUser2', write_only=True, required=False, allow_null=True)
    id_CustomerUser2 = CustomUserSerializer(read_only=True)
    
    support_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Support
        fields = ('id','id_ips','id_ips_id','id_CustomerUser','id_CustomerUser_id','role2','medio','name_solicited',
                  'number','requirement','email','typerequest_id','id_type_request_id','subtype_request',
                  'id_Subtype_request_id','support_date','create_date','update_date','is_active','is_close','how_it_conclude',
                  'answer','id_CustomerUser2','id_CustomerUser2_id')
        
class SupportIdUser2Serializer(serializers.ModelSerializer):
    
    id_CustomerUser2_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerUser.objects.all(), source='id_CustomerUser2', write_only=True, required=False, allow_null=True)
    id_CustomerUser2 = CustomUserSerializer(read_only=True)
    
    
    class Meta:
        model = (Support)
        fields = ('id','id_CustomerUser2','id_CustomerUser2_id')