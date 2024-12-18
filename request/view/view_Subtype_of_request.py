from ..models import SubtypeRequest,typeRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializer.Subtype_of_request_Serializer import SubtypeRequestSerializer
from rest_framework import status
import logging;

logger = logging.getLogger(__name__)



@api_view(['GET'])
def getSubType_of_request(request):
    try:
        listTypes = SubtypeRequest.objects.all().order_by('id')
        serializer = SubtypeRequestSerializer(listTypes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error al obtener Tipo: " + str(e))
        return Response({"error": "Error al obtener SubTipo de requerimiento"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getSubType_of_request_type(request, number):
    try:
        typerequest = typeRequest.objects.get(id=number)
        if not typerequest:
            return Response({'error': 'El reporte médico no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        subtypeRequest = SubtypeRequest.objects.filter(type_request_id=typerequest)
        if not subtypeRequest:
            return Response({'error': 'El paciente no tiene anexos.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = SubtypeRequestSerializer(subtypeRequest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al obtener los anexos de un reporte médico.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def createSubType_of_request(request):
    
    try:
        serializer = SubtypeRequest(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error("Error al crear el Subtipo de requerimiento: " + str(e))
        return Response({"error": "Error al crear el Subtipo de requerimiento"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
def getOneSubType(request, pk):
    user = SubtypeRequest.objects.get(id=pk)
    serializer = SubtypeRequestSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    
    

