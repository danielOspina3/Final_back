from rest_framework.response import Response
from request.serializer import CustomUserManagerSerializer
from ..models import CustomerUser
from request.serializer import CustomUserManagerSerializer
from request.serializer.CustomUserManagerSerializer import CustomUserSerializer
from ..serializer.CustomUserManagerSerializer import CustomerUserIsActive,CustomerUser
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

import logging
 
logger = logging.getLogger(__name__)

@api_view(['GET'])
def getUser(request):
    try:
        # Obtener todos los usuarios
        list_user = CustomerUser.objects.all().order_by('-id')
        
        # Verificar si hay usuarios
        if not list_user:
            return Response({'error': 'No hay usuarios disponibles.'}, status=status.HTTP_204_NO_CONTENT)
        
        # Serializar los datos
        serializer = CustomUserSerializer(list_user, many=True)
        
        # Retornar la respuesta con todos los usuarios
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Error: {e}')
        return Response({'error': 'Error al obtener los datos de los usuarios.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
@api_view(['GET'])
def getUsers(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 50  # Número de elementos por página.
        list_user = CustomerUser.objects.all().order_by('-id')
        if not list_user:
            return Response({'error': 'No hay usuarios disponibles.'}, status=status.HTTP_204_NO_CONTENT)
        
        result_page = paginator.paginate_queryset(list_user, request)
        serializer = CustomUserSerializer(result_page, many=True)
        
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
        return Response({'error': 'Error al obtener los datos de los usuarios.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def createUser(request):
    data = request.data.copy()
    
    serializer = CustomUserManagerSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    errors = serializer.errors
    
    # if 'email' in errors:
    #     errors = ['email'] = "El email ya existe"
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateUserIsActive(request, pk):
    user = CustomerUser.objects.get(id=pk)
    serializer = CustomerUserIsActive(
        instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def updateUser(request, pk):
    try:
        user = CustomerUser.objects.get(id=pk)
        print(user)
    except CustomerUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Copy request data to avoid modifying the original data directly
    request_data = request.data.copy()
    
    # Check if the password is being updated and hash it
    if 'password' in request_data:
        request_data['password'] = make_password(request_data['password'])

    serializer = CustomUserSerializer(instance=user, data=request_data)
    print(request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getOneUser(request, pk):
    user = CustomerUser.objects.get(id=pk)
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def getOneUserToken(request, num_document):
    user = CustomerUser.objects.get(num_document=num_document)
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def getOneUserRol(request, pk):
    user = get_object_or_404(CustomerUser, id=pk)
    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

