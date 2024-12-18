from rest_framework import serializers
from request.models import typeRequest,SubtypeRequest
from .type_of_request_Serializer import typeRequestSerializer

class SubtypeRequestSerializer(serializers.ModelSerializer):
    
    id_type_request_id = serializers.PrimaryKeyRelatedField(queryset=typeRequest.objects.all(), source='type_request_id', write_only=True, required=False, allow_null=True)
    type_request_id = typeRequestSerializer(read_only=True)
    
    class Meta:
        model = SubtypeRequest
        fields = ('id','subtype_request','type_request_id','id_type_request_id')