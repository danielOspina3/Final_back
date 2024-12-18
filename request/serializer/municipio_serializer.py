from rest_framework import serializers
from request.models import Municipio

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id', 'nombre_municipio', 'codigo_municipio')


class MunicipioSerializerActive(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id', 'codigo_municipio')