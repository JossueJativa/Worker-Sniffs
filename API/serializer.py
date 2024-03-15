from rest_framework import serializers
from .models import Manger, CallCenter, Certificate, Client, Comments, Problems, Problems_Tikets, Product, Stars, Tecnic, User

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class StarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = '__all__'

class Problems_TiketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems_Tikets
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="The email should be the data of the email of the user."
    )
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        help_text="The password should be the data of the password of the user."
    )

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True,
        help_text="The password should be encrypted using Base64 and SHA-256 for security reasons."
    )

    identity = serializers.CharField(
        required=False,
        help_text="The identity should be the data of the identity card or passport."
    )

    phone = serializers.CharField(
        required=False,
        help_text="The phone should be the data of the phone number."
    )

    is_blocked = serializers.BooleanField(
        write_only=True,
        required=False,
        help_text="The is_blocked should be the data of the status of the user if the user are blocked from the platform."
    )

    work_status = serializers.CharField(
        required=False,
        help_text="The work_status should be the data of the status of the user if the user are working."
    )
    
    class Meta:
        model = User
        fields = '__all__'

class TecnicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnic
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manger
        fields = '__all__'

class CallCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallCenter
        fields = '__all__'