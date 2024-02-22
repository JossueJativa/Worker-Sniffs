from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from API.models import Manger, CallCenter, Tecnic, User

# Create your views here.

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        username = User.objects.get(email=email).username
        
        user = authenticate(request, username=username, password=password)

        # Verificamos la contraseña utilizando el método check_password personalizado
        if user is not None:
            login(request, user)

            # Buscar que tipo de usuario es y redirigirlo a su pagina
            if Manger.objects.filter(user=user).exists():
                return redirect("manager:principal_page")
            elif CallCenter.objects.filter(user=user).exists():
                return redirect("callcenter:index")
            elif Tecnic.objects.filter(user=user).exists():
                return redirect("tecnic:intro")
            else:
                return render(request, "startapp/login_view.html", {"message": "Tipo de usuario no valido"})
        else:
            return render(request, "startapp/login_view.html", {"message": "Credenciales incorrectas"})
    else:
        return render(request, "startapp/login_view.html")

def logout_view(request):
    logout(request)
    return render(request, "startapp/login_view.html", {"message": "Logged out"})