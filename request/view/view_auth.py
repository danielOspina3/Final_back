from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from request.models import CustomerUser
from request.serializer.CustomUserManagerSerializer import CustomUserSerializer
from django.contrib.auth import authenticate
import logging;
from django.contrib.auth.models import update_last_login
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




User = get_user_model()
logger = logging.getLogger(__name__)



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerUser
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerUser
    permission_classes = [permissions.IsAuthenticated]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if the email exists
        try:
            user = CustomerUser.objects.get(email=email)
        except user.DoesNotExist:
            return Response({'error': _('Correo inválido')}, status=status.HTTP_200_OK)

        # Check if the user is active
        if not user.is_active:
            return Response({'error': _('Usuario no activo')}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': _('Contraseña incorrecta')}, status=status.HTTP_401_UNAUTHORIZED)

        # If authentication is successful, create or get the token
        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)




class CreateUserAPIView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.name + ' ' + user.last_name
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                logger.warning("email or password not provided")
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomerUser.objects.get(email=email)

            if not user.is_active:
                logger.warning("Inactive user tried to login")
                return Response({'error': 'La cuenta del usuario esta inactiva.'}, status=status.HTTP_401_UNAUTHORIZED)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user.email
                }, status=status.HTTP_200_OK)
            else:
                logger.warning("Invalid credentials provided")
                return Response({'error': 'Correo o contraseña inválidos'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomerUser.DoesNotExist:
            logger.warning("User not found")
            return Response({'error': 'Usuario no encontrado. Verifíque sus credenciales.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            return Response({'error': 'Error interno en el servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)