from rest_framework import serializers
from request.models import Ips
from request.models import Municipio
from .. serializer.municipio_serializer import MunicipioSerializer




class IpsSerializer(serializers.ModelSerializer):
    # Relación con Municipio usando PrimaryKeyRelatedField
    id_municipio_id = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all(), source='municipio_id', write_only=True, required=False, allow_null=True)
    municipio_id = MunicipioSerializer(read_only=True)  # Relación solo de lectura con Municipio

    class Meta:
        model = Ips
        fields = ('id', 'nombre_ips', 'cod_ips', 'is_active', 'id_municipio_id', 'municipio_id')


class IpsSerializerActive(serializers.ModelSerializer):
    # Relación con Municipio en el serializer activo
    id_municipio_id = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all(), source='municipio_id', write_only=True, required=False, allow_null=True)
    municipio_id = MunicipioSerializer(read_only=True)  
    
    class Meta:
        model = Ips
        fields = ('id', 'is_active', 'id_municipio_id', 'municipio_id')