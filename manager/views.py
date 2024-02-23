from django.shortcuts import render
from API.models import User, Tecnic, CallCenter, Manger, Client
from django.contrib.auth.hashers import make_password

# Create your views here.
import hashlib
import base64

def encrypt_password(password):
    password_bytes = password.encode('utf-8')
    sha256_result = hashlib.sha256(password_bytes)
    base64_hash = base64.b64encode(sha256_result.digest()).decode('utf-8')
    return base64_hash

def principal_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        identity = request.POST.get("identity")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        worker_type = request.POST.get("worker_type")
        image = request.FILES.get("image")

        worker_type = int(worker_type)

        if worker_type == 0:
            return render(request, "index.html", {"message": "Seleccione un tipo de usuario"})
        
        if not image:
            return render(request, "index.html", {"message": "Suba una imagen"})

        # Crear username
        username = first_name + "_" + last_name

        # Verificar que el email no exista
        if User.objects.filter(email=email).exists():
            return render(request, "index.html", {"message": "El email ya existe"})
        
        # Verificar que el username no exista
        if User.objects.filter(username=username).exists():
            username = username + "_" + User.objects.last().id

        # Verificar que las contraseñas sean iguales
        if password != confirm:
            return render(request, "index.html", {"message": "Las contraseñas no coinciden"})
        
        # Verificar que la cedula no este repetida
        if User.objects.filter(identity=identity).exists():
            return render(request, "index.html", {"message": "La cedula ya existe"})
        
        # Verificar que el telefono no este repetido
        if User.objects.filter(phone=phone).exists():
            return render(request, "index.html", {"message": "El telefono ya existe"})
        
        # Encriptar la contraseña
        password = make_password(encrypt_password(password))

        # Crear el usuario
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            identity=identity,
            username=username,
            password=password
        )

        user.save()

        if worker_type == 1:
            callcenter = CallCenter.objects.create(
                user=user,
                photo = image
            )
            callcenter.save()
        elif worker_type == 2:
            tecnic = Tecnic.objects.create(
                user=user,
                photo = image
            )
            tecnic.save()
        else:
            manager = Manger.objects.create(
                user=user,
                photo = image
            )
            manager.save()

        return render(request, "index.html", {
            "success": "Usuario creado correctamente",
            "username": username
        })
    else:
        return render(request, "index.html", {})
    
def workers(request):
    callcenters = CallCenter.objects.all()
    tecnic = Tecnic.objects.all()
    return render(request, "workers/trabajadores.html", {
        "callcenters": callcenters,
        "tecnics": tecnic,
    })

def delete_worker(request, id):
    try:
        callcenter = CallCenter.objects.get(id=id)
    except:
        callcenter = None
    
    try:
        tecnic = Tecnic.objects.get(id=id)
    except:
        tecnic = None

    if callcenter is None and tecnic is None:
        return render(request, "workers/trabajadores.html", {
            "message": "No se encontro el trabajador"
        })
    
    if callcenter is not None:
        User.objects.get(id=callcenter.user.id).delete()
    else:
        User.objects.get(id=tecnic.user.id).delete()

    return render(request, "workers/trabajadores.html", {
        "callcenter": callcenter,
        "tecnic": tecnic,
    })

def edit_worker(request):
    if request.method == "POST":
        id = request.POST.get("id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        identity = request.POST.get("identity")
        phone = request.POST.get("phone")
        status = request.POST.get("status")

        try:
            user = User.objects.get(id=id)

            username = first_name + "_" + last_name

            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.identity = identity
            user.phone = phone
            user.work_status = status

            user.save()

            callcenters = CallCenter.objects.all()
            tecnic = Tecnic.objects.all()
            return render(request, "workers/trabajadores.html", {
                "success": "Usuario actualizado correctamente",
                "callcenters": callcenters,
                "tecnics": tecnic
            })
        except:
            return render(request, "workers/trabajadores.html", {
                "message": "No se encontro el trabajador"
            })

def block_worker(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_blocked = True
        user.save()

        callcenters = CallCenter.objects.all()
        tecnic = Tecnic.objects.all()
        return render(request, "workers/trabajadores.html", {
            "success": "Usuario bloqueado correctamente",
            "callcenters": callcenters,
            "tecnics": tecnic
        })
    except:
        return render(request, "workers/trabajadores.html", {
            "message": "No se encontro el trabajador",
            'callcenters': callcenters,
            'tecnics': tecnic
        })
    
def unblock_worker(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_blocked = False
        user.save()

        callcenters = CallCenter.objects.all()
        tecnic = Tecnic.objects.all()
        return render(request, "workers/trabajadores.html", {
            "success": "Usuario desbloqueado correctamente",
            "callcenters": callcenters,
            "tecnics": tecnic
        })
    except:
        return render(request, "workers/trabajadores.html", {
            "message": "No se encontro el trabajador",
            "callcenters": callcenters,
            "tecnics": tecnic
        })
    
def clients(request):
    clients = Client.objects.all()
    return render(request, "clients/clients.html", {
        'clients': clients
    })

def accept_client(request, id):
    try:
        client = Client.objects.get(id=id)
        client.is_accepted_by_manager = "Aceptado"
        client.save()

        clients = Client.objects.all()

        # Sacar un tecnico que no tenga clientes
        try:
            tecnic = Tecnic.objects.filter(clients=None).first()
            tecnic.clients.add(client)
            tecnic.save()
        except:
            pass

        # Si no encuentra tecnico, encontrar el que menos clientes tenga
        if tecnic is None:
            tecnic = Tecnic.objects.all()
            tecnic = sorted(tecnic, key=lambda x: x.clients.count())
            tecnic = tecnic[0]
            tecnic.clients.add(client)
            tecnic.save()

        return render(request, "clients/clients.html", {
            "success": "Cliente aceptado correctamente",
            "clients": clients
        })
    except:
        return render(request, "clients/clients.html", {
            "message": "No se encontro el cliente",
            "clients": clients
        })
    
def reject_client(request, id):
    try:
        client = Client.objects.get(id=id)
        client.is_accepted_by_manager = "Rechazado"
        client.save()

        clients = Client.objects.all()
        return render(request, "clients/clients.html", {
            "success": "Cliente rechazado correctamente",
            "clients": clients
        })
    except:
        return render(request, "clients/clients.html", {
            "message": "No se encontro el cliente",
            "clients": clients
        })