# Importaciones externas
import base64
import binascii
import json
import os

# Importaciones del programa
from .models import Manger, CallCenter, Certificate, Client, Comments, Problems, Problems_Tikets, Product, Stars, Tecnic, User
from .serializer import CallCenterSerializer, CommentsSerializer, LoginSerializer, StarsSerializer, ProductSerializer, ProblemsSerializer, Problems_TiketsSerializer, ClientSerializer, CertificateSerializer, UserSerializer, TecnicSerializer, ManagerSerializer

# Django
from django.db.models.signals import pre_save
from django.db.models import Count
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

# Rest Framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

# Firebase
from firebase_admin import messaging

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

    def create(self, request, *args, **kwargs):
        # Verificar si el cliente ya existe
        identity = request.data.get('identity')
        client = Client.objects.filter(identity=identity).first()
        if client:
            return Response({'error': 'El cliente ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Sacamos todos los datos del request
            username = request.data.get('username')
            identity = request.data.get('identity')
            phone = request.data.get('phone')
            total_price = request.data.get('total_price')
            date_instalation = request.data.get('date_instalation')
            part_of_day = request.data.get('part_of_day')
            options_to_give_instalation = request.data.get('options_to_give_instalation')
            products_bought = request.data.get('products_bought')
            photo_reciept = request.FILES.get('photo_reciept')
            # Convertir esto: [4, 6, 8] que es un String a esto: [4, 6, 8] que es una lista
            products_bought = json.loads(products_bought)

            # Convertir a lista de objetos
            products_bought = Product.objects.filter(pk__in=products_bought)

            # Creamos el cliente
            client = Client.objects.create(
                username=username, 
                identity=identity, 
                phone=phone, 
                total_price=total_price, 
                date_instalation=date_instalation, 
                part_of_day=part_of_day, 
                options_to_give_instalation=options_to_give_instalation, 
                photo_reciept=photo_reciept
            )
            client.set_products_bought_ids(products_bought)

            # Retornamos el serializer
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='search-by-identity/(?P<identity>[^/.]+)', url_name='search-by-identity')
    def search_by_identity(self, request, *args, **kwargs):
        identity = kwargs.get('identity')
        client = Client.objects.filter(identity=identity).first()  # Obtener el primer cliente que coincida
        if not client:
            return Response({'error': 'No se encontró ningún cliente con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(client)  # No usar many=False
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if user:
            tecnic = Tecnic.objects.filter(user=user)
            if not tecnic:
                return Response({'error': 'No se encontró ningún técnico con el usuario proporcionado.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(tecnic, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontró ningún usuario con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['POST'], url_path='assign-client-to-tecnic/(?P<client_id>[^/.]+)', url_name='assign-client-to-tecnic')
    def assign_client_to_tecnic(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_id)
        
        # Obtener un técnico que no tenga clientes
        tecnic = Tecnic.objects.annotate(num_clients=Count('clients')).filter(num_clients=0).first()

        # Si no hay técnicos sin clientes, obtener el que tenga menos clientes
        if not tecnic:
            tecnic = Tecnic.objects.annotate(num_clients=Count('clients')).order_by('num_clients').first()

        if tecnic:
            tecnic.clients.add(client)
            return Response({'success': 'Cliente asignado al técnico correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No hay técnicos disponibles para asignar el cliente.'}, status=status.HTTP_404_NOT_FOUND)

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manger.objects.all()
    serializer_class = ManagerSerializer

    @action(detail=False, methods=['GET'], url_path='search-by-user/(?P<user>[^/.]+)', url_name='search-by-user')
    def search_by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        user = get_object_or_404(User, pk=user_id)
        if user:
            manager = Manger.objects.filter(user=user)
            if not manager:
                return Response({'error': 'No se encontró ningún usuario con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(manager, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
class CallCenterViewSet(viewsets.ModelViewSet):
    queryset = CallCenter.objects.all()
    serializer_class = CallCenterSerializer

    @action(detail=False, methods=['GET'], url_path='search-by-user/(?P<user>[^/.]+)', url_name='search-by-user')
    def search_by_user(self, request, *args, **kwargs):
        user_id = kwargs.get('user')
        user = get_object_or_404(User, pk=user_id)
        if user:
            callcenter = CallCenter.objects.filter(user=user)
            if not callcenter:
                return Response({'error': 'No se encontró ningún usuario con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(callcenter, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontró ningún usuario con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
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
        
    @action(detail=False, methods=['GET'], url_path='search-by-identity/(?P<identity>[^/.]+)', url_name='search-by-identity')
    def search_by_identity(self, request, *args, **kwargs):
        identity = kwargs.get('identity')
        user = User.objects.filter(identity=identity).first()  # Utilizar first() en lugar de filter()
        if user:
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se encontró ningún usuario con la identidad proporcionada.'}, status=status.HTTP_404_NOT_FOUND)
        
# Notificacion de FCM para el cliente
class PushNotificationAPIView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        type_user = request.data.get('type_user')
        title = request.data.get('title')
        body = request.data.get('body')

        if not type_user or not title or not body:
            return Response({'error': 'Type user, title, and body are required'}, status=status.HTTP_400_BAD_REQUEST)

        tokens = []
        if type_user.lower() == 'callcenter':
            tokens = list(CallCenter.objects.values_list('token_phone', flat=True))
        elif type_user.lower() == 'tecnic':
            tokens = list(Tecnic.objects.values_list('token_phone', flat=True))
        elif type_user.lower() == 'manager':
            tokens = list(Manger.objects.values_list('token_phone', flat=True))
        else:
            return Response({'error': 'Invalid user type. The valid types are "manager", "tecnic", "callcenter"'}, status=status.HTTP_400_BAD_REQUEST)
        
        for token in tokens:
            response = self.send_push_message(token, title, body)
            if not response:
                return Response({'error': 'The push notification could not be sent'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'success': 'The push notification was sent successfully'}, status=status.HTTP_200_OK)
        
    
    def send_push_message(self, token, title, body):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token
        )

        response = messaging.send(message)
        return response

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