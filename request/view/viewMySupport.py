from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..models import CustomerUser,Support
import logging
from django.utils import timezone
from django.db.models import Min, Max, Count
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
import pandas as pd
from django.http import HttpResponse
from ..serializer.CustomUserManagerSerializer import CustomUserSerializer
from ..serializer.SupportSerializer import SupportSerializer


logger = logging.getLogger(__name__)

@api_view(['GET'])
def getbysupport(request, id):
    try:
        user= CustomerUser.objects.get(id=id)
        print(user)
        supports = Support.objects.filter(id_CustomerUser=user)
        
        if not supports.exists():
            return Response({'error': 'No support records found for the person.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serializa los soportes encontrados
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error retrieving support by person ID {id}: {str(e)}")
        return Response({'error': 'Error retrieving support by person.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    