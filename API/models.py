import hashlib
import base64
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password

from rest_framework.authtoken.models import Token

def encrypt_password(password):
    password_bytes = password.encode('utf-8')
    sha256_result = hashlib.sha256(password_bytes)
    base64_hash = base64.b64encode(sha256_result.digest()).decode('utf-8')
    return base64_hash

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    work_status = models.CharField(max_length=255, default="Disponible")
    identity = models.CharField(max_length=20, null=True)
    is_blocked = models.BooleanField(default=False)

    def check_password(self, raw_password):
        return check_password(encrypt_password(raw_password), self.password)

class Comments(models.Model):
    comment = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateField(blank=False, null=False)

class Stars(models.Model):
    star = models.IntegerField(blank=False, null=False)
    date = models.DateField(blank=False, null=False)

class Product(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)

class Problems(models.Model):
    title_description = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=20, default="Baja")

class Problems_Tikets(models.Model):
    description = models.CharField(max_length=200, blank=False, null=False)
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    user_with_problem = models.CharField(max_length= 50,blank=False, null=False)
    type_user = models.CharField(max_length=20, blank=False, null=False)
    photo = models.ImageField(upload_to='problems', blank=True, null=True)
    '''
    Usuarios con problemas pueden ser:
    - Tecnicos
    - Clientes
    - Call center
    - Manager
    '''

class Client(models.Model):
    products_bought = models.ManyToManyField(Product)
    username = models.CharField(max_length=20, blank=False, null=False)
    identity = models.CharField(max_length=20, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    total_price = models.FloatField(blank=False, null=False)
    date_instalation = models.DateField(blank=True, null=True)
    part_of_day = models.CharField(max_length=20, blank=True, null=True)
    status_instalation = models.CharField(max_length=15, blank=True, null=True)
    is_accepted_by_manager = models.CharField(max_length=20, default="Esperando Aprobación")
    options_to_give_instalation = models.CharField(max_length=20, default="Recoger")
    photo_reciept = models.ImageField(upload_to='reciepts', blank=False, null=False)

    def photo_reciept_url(self):
        if self.photo_reciept:
            return self.photo_reciept.url
        return None
    
    def set_products_bought_ids(self, ids):
        self.products_bought.set(ids)
    
class Certificate(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_instalation = models.DateField(blank=False, null=False)
    firm = models.CharField(max_length=20, blank=False, null=False)
    photo = models.ImageField(upload_to='certificates', blank=False, null=False)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None

class Tecnic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comments, blank=True)
    stars = models.ManyToManyField(Stars, blank=True)
    clients = models.ManyToManyField(Client, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    location_lat = models.FloatField(blank=True, null=True)
    location_lon = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='tecnic', blank=True, null=True)
    token_phone = models.CharField(max_length=200, blank=True, null=True)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, blank=True, null=True)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
class CallCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    '''
    Call center puede seleccionar el dia y la hora de la instalación del cliente
    Call center puede enviar el comprobante de pago del cliente
    Call center puede reasignar una fecha nueva de instalación del cliente

    '''
    photo = models.ImageField(upload_to='callcenter', blank=True, null=True)
    token_phone = models.CharField(max_length=200, blank=True, null=True)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None
    
class Manger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tecnic = models.ManyToManyField(Tecnic, blank=True)
    clients = models.ManyToManyField(Client, blank=True)
    photo = models.ImageField(upload_to='manager', blank=True, null=True)
    token_phone = models.CharField(max_length=200, blank=True, null=True)

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None