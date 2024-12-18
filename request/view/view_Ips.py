from ..models import Ips
from ..models import Municipio
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializer.ips_serializer import IpsSerializer,IpsSerializerActive
from .. serializer.municipio_serializer import MunicipioSerializer


from rest_framework import status
import logging;
from django.db import DatabaseError
from django.db import IntegrityError

logger = logging.getLogger(__name__)

@api_view(['GET'])
def getEPS(request):
    try:
        listIps = Ips.objects.all().order_by('municipio_id__nombre_municipio')
        serializer = IpsSerializer(listIps, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error al obtener EPS: " + str(e))
        return Response({"error": "Error al obtener EPS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getEPSActive(request):
    try:
        listIps = Ips.objects.filter(is_active=True).order_by('nombre_ips')
        if not listIps.exists():
            return Response({"error": "No hay EPS disponibles."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = IpsSerializer(listIps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except DatabaseError as e:
        logger.error("Error de base de datos al obtener EPS: " + str(e))
        return Response({"error": "Error al obtener EPS."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error("Error inesperado al obtener EPS: " + str(e))
        return Response({"error": "Error al procesar la solicitud de EPS."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def createEPS(request):
    try:
        # Verificar si ya existe un registro con el mismo cod_ips
        cod_ips = request.data.get('cod_ips')
        if Ips.objects.filter(cod_ips=cod_ips).exists():
            logger.error("Error: El código IPS ya está en uso.")
            return Response({"error": "El código IPS ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)


        # Crear datos del `formData`
        formData = {
            'nombre_ips': request.data.get('nombre_ips'),
            'cod_ips': request.data.get('cod_ips'),
            'is_active': request.data.get('is_active', True),
            'id_municipio_id': request.data.get('id_municipio_id') # Aquí asignamos el objeto `Municipio` (o `None` si no existe)
        }

        # Usamos el serializer para validar y guardar los datos
        serializer = IpsSerializer(data=formData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        logger.error("Error de integridad al crear EPS: " + str(e))
        return Response({"error": "Error de integridad al crear EPS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error("Error al crear EPS: " + str(e))
        return Response({"error": "Error al crear EPS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getOneIps(request, pk):
    support = Ips.objects.get(id=pk)
    serializer = IpsSerializer(support, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
   
    

@api_view(['PUT'])
def updateIpsActive(request, pk):
    print(request.data)
    try:
        support = Ips.objects.get(id=pk)
        if not request.data:
            return Response({'error': 'No se han proporcionado datos para actualizar la ips.'}, status=status.HTTP_400_BAD_REQUEST)

        serialize = IpsSerializerActive(instance=support, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    except Ips.DoesNotExist:
        return Response({'error': 'ips no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al actualizar la ips.'})
@api_view(['GET'])
def getEPSByMunicipio(request, municipio_id):
    try:
        municipio = Municipio.objects.filter(id=municipio_id).first()  # Usamos .first() para obtener None si no existe
        if not municipio:
            return Response({"error": "Municipio no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        listIps = Ips.objects.filter(municipio=municipio).order_by('nombre_ips')
        if not listIps.exists():
            return Response({"error": "No hay EPS disponibles en este municipio."}, status=status.HTTP_404_NOT_FOUND)

        serializer = IpsSerializer(listIps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error("Error al obtener EPS para el municipio: " + str(e))
        return Response({"error": "Error al obtener EPS para el municipio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
def getMunicipio(request):
    try:
        listMunicipio = Municipio.objects.all().order_by('nombre_municipio')
        serializer = MunicipioSerializer( listMunicipio, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error("Error al obtener EPS: " + str(e))
        return Response({"error": "Error al obtener EPS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)