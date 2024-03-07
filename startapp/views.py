from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from API.models import Manger, CallCenter, Tecnic, User

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Obtener el usuario por su email
        user = User.objects.filter(email=email).first()

        if user is not None:
            # Autenticar con el campo username
            user = authenticate(request, username=user.username, password=password)
            print(user)

            if user is not None:
                login(request, user)

                # Buscar qué tipo de usuario es y redirigirlo a su página
                if Manger.objects.filter(user=user).exists():
                    return redirect("manager:principal_page")
                elif CallCenter.objects.filter(user=user).exists():
                    return redirect("callcenter:index")
                elif Tecnic.objects.filter(user=user).exists():
                    return redirect("tecnic:intro")
                else:
                    return render(request, "startapp/login_view.html", {"message": "Tipo de usuario no válido"})
            else:
                return render(request, "startapp/login_view.html", {"message": "Credenciales incorrectas"})
        else:
            return render(request, "startapp/login_view.html", {"message": "Usuario no encontrado"})
    else:
        return render(request, "startapp/login_view.html")

def logout_view(request):
    logout(request)
    return render(request, "startapp/login_view.html", {"message": "Logged out"})