from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializer.SupportSerializer import SupportSerializer
from ..models import Support
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import logging
import pandas as pd
from django.http import HttpResponse



logger = logging.getLogger(__name__)

@api_view(['GET'])
def supportGetAll(request):
    try:
        typerequest_id = request.query_params.get('typerequest_id', None)
        
        supports = Support.objects.filter(is_active=True)
        
        if typerequest_id:
            supports = supports.filter(typerequest_id=typerequest_id)
        ips = request.query_params.get('ips', None)
        
        supports = Support.objects.filter(is_active=True)
        
        if ips:
            supports = supports.filter(id_ips=ips)
        
        supports = supports.order_by('-id')
        
        paginator = PageNumberPagination()
        paginator.page_size = 50
        if not supports:
            return Response({'error': 'No hay soportes disponibles.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_page = paginator.paginate_queryset(supports, request)
        serializer = SupportSerializer(result_page, many=True)
        
        # Obtener el número total de elementos y páginas
        total_count = paginator.page.paginator.count
        total_pages = paginator.page.paginator.num_pages
        
        # Crear la respuesta paginada
        paginated_response = paginator.get_paginated_response(serializer.data)
        paginated_response.data['total_count'] = total_count
        paginated_response.data['total_pages'] = total_pages
        
        return paginated_response
    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al obtener los datos de los soportes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def supportGetAllFinal(request):
    
    try:
        supports = Support.objects.filter(is_active=False).order_by('id')
        if not supports:
            return Response({'error': 'No hay soportes disponibles.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = SupportSerializer(supports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al obtener los datos de los soportes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# def supportGetAllActiveFalse(request):
#     try:
#         supports = Support.objects.filter(is_active=False).order_by('id')
#         if not supports:
#             return Response({'error': 'No hay soportes disponibles.'}, status=status.HTTP_204_NO_CONTENT)
#         serializer = SupportSerializer(supports, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f'Error: {e}')
#         return Response({'error': 'Error al obtener los datos de los soportes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def createSupport(request):
    data = request.data.copy()
    print(data)
    if not data.get('id_ips_id') or not data.get('id_type_request_id') or not data.get('id_Subtype_request_id'):
        return Response(
            {"error": "Faltan IDs de las claves foráneas."},
            status=status.HTTP_204_NO_CONTENT
        )

    serializer = SupportSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateSupport(request, pk):
    try:
        support = Support.objects.get(id=pk)
        if not request.data:
            return Response({'error': 'No se han proporcionado datos para actualizar el soportes.'}, status=status.HTTP_400_BAD_REQUEST)

        serialize = SupportSerializer(instance=support, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    except Support.DoesNotExist:
        return Response({'error': 'soporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al actualizar el soporte.'})
    
    


@api_view(['GET'])
def getOneSupport(request, pk):
    support = Support.objects.get(id=pk)
    serializer = SupportSerializer(support, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
def update_customeruser2(request, pk):
    try:
        print(pk)
        # Obtener el soporte por el id (pk)
        support = Support.objects.get(id=pk)
        
        # Verificar si se envió el campo 'id_customeruser2_id' en los datos del request
        new_customeruser2_id = request.data.get('id_CustomerUser2_id', None)
        if new_customeruser2_id is None:
            return Response({'error': 'No se proporcionó id_customeruser2_id.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar el campo id_CustomerUser2_id
        support.id_CustomerUser2_id = new_customeruser2_id
        support.save()
        
        return Response({'message': 'id_customeruser2 actualizado correctamente.'}, status=status.HTTP_200_OK)
    
    except Support.DoesNotExist:
        return Response({'error': 'Soporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f'Error actualizando id_customeruser2: {e}')
        return Response({'error': 'Error interno al actualizar el soporte.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['PUT'])
def update_support_details(request, pk):
    try:
        print(pk)
        # Obtener el soporte por el id (pk)
        support = Support.objects.get(id=pk)

        # Obtener los nuevos valores desde los datos del request
        new_how_it_conclude = request.data.get('how_it_conclude', None)
        new_answer = request.data.get('answer', None)

        # Verificar que ambos campos se hayan proporcionado
        if new_how_it_conclude is None or new_answer is None:
            return Response({'error': 'Se deben proporcionar los campos how_it_conclude y answer.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar los campos correspondientes
        support.how_it_conclude = new_how_it_conclude
        support.answer = new_answer
        support.is_active = False
        support.save()

        return Response({'message': 'Soporte actualizado correctamente.'}, status=status.HTTP_200_OK)

    except Support.DoesNotExist:
        return Response({'error': 'Soporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Error actualizando el soporte: {e}', exc_info=True)  # Captura detalles del error
        return Response({'error': 'Error interno al actualizar el soporte.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def export_supports_to_excel(request):
    try:
        # Assuming 'Support' model is used for export
        supports = Support.objects.all()  # or apply any filter as needed
        serializer = SupportSerializer(supports, many=True)
        df = pd.DataFrame(serializer.data)

        # Create an Excel file
        excel_file = 'soportes.xlsx'
        df.to_excel(excel_file, index=False, sheet_name='Soportes')

        # Return the file as an HTTP response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{excel_file}"'
        df.to_excel(response, index=False, sheet_name='Soportes')

        return response

    except Exception as e:
        logger.error(f"Error exporting supports to Excel: {str(e)}")
        return Response({'error': 'Error exporting supports to Excel.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)