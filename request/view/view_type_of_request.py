from ..models import typeRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializer.type_of_request_Serializer import typeRequestSerializer
from rest_framework import status
import logging;

logger = logging.getLogger(__name__)

@api_view(['GET'])
def getType_request(request):
    try:
        listTypes = typeRequest.objects.all().order_by('id')
        serializer = typeRequestSerializer(listTypes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error al obtener Tipo: " + str(e))
        return Response({"error": "Error al obtener Tipo de requerimiento"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def createType_of_request(request):
    try:
        serializer = typeRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("Error al crear Tipo de requerimiento: " + str(e))
        return Response({"error": "Error al crear el tipo de requerimiento"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
