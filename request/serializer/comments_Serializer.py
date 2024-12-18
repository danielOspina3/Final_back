from rest_framework import serializers
from request.models import Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id','id_support','text','image')

