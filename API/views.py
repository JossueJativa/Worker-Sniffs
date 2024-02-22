# Importaciones externas
import base64
import binascii

# Importaciones del programa
from .models import Manger, CallCenter, Certificate, Client, Comments, Problems, Problems_Tikets, Product, Stars, Tecnic, User
from .serializer import CallCenterSerializer, CommentsSerializer, LoginSerializer, StarsSerializer, ProductSerializer, ProblemsSerializer, Problems_TiketsSerializer, ClientSerializer, CertificateSerializer, UserSerializer, TecnicSerializer, ManagerSerializer

# Django
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

# Create your views here.
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class StarsViewSet(viewsets.ModelViewSet):
    queryset = Stars.objects.all()
    serializer_class = StarsSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProblemsViewSet(viewsets.ModelViewSet):
    queryset = Problems.objects.all()
    serializer_class = ProblemsSerializer

class Problems_TiketsViewSet(viewsets.ModelViewSet):
    queryset = Problems_Tikets.objects.all()
    serializer_class = Problems_TiketsSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class TecnicViewSet(viewsets.ModelViewSet):
    queryset = Tecnic.objects.all()
    serializer_class = TecnicSerializer

    @action(detail=False, methods=['GET'], url_path='search-by-user/(?P<user>[^/.]+)', url_name='search-by-user')
    def search_by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        user = get_object_or_404(User, pk=user_id)
        tecnic = Tecnic.objects.filter(user=user)
        serializer = self.get_serializer(tecnic, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manger.objects.all()
    serializer_class = ManagerSerializer

    @action(detail=False, methods=['GET'], url_path='search-by-user/(?P<user>[^/.]+)', url_name='search-by-user')
    def search_by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        user = get_object_or_404(User, pk=user_id)
        manager = Manger.objects.filter(user=user)
        serializer = self.get_serializer(manager, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CallCenterViewSet(viewsets.ModelViewSet):
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

    @action(detail=False, methods=['GET'], url_path='search-by-user/(?P<user>[^/.]+)', url_name='search-by-user')
    def search_by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        user = get_object_or_404(User, pk=user_id)
        callcenter = CallCenter.objects.filter(user=user)
        serializer = self.get_serializer(callcenter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Check if the password is already encrypted with Base64 and SHA before creating the user
        password = request.data.get('password')
        if not is_base64_sha256(password):
            return Response({'error': 'The password is not encrypted with Base64 and SHA.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # No necesitas decodificar y re-encriptar la contraseña aquí
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            if not email or not password:
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the user by email
            user = get_object_or_404(User, email=email)

            # Verify password format
            if not is_base64_sha256(password):
                return Response({'error': 'Invalid password format'}, status=status.HTTP_400_BAD_REQUEST)

            # Use check_password to compare hashed password with stored password
            if not check_password(password, user.password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # User authenticated successfully
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
def is_base64_sha256(s):
    try:
        decoded = base64.b64decode(s)
        return len(decoded) == 32
    except (TypeError, binascii.Error):
        return False

@receiver(pre_save, sender=User)
def encrypt_password(sender, instance, **kwargs):
    if instance.pk is None or instance._password != User.objects.get(pk=instance.pk).password:
        if not is_base64_sha256(instance.password) and not instance.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            raise ValueError('The password is not encrypted with Base64 and SHA.')