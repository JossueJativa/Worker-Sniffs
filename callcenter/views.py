from django.http import HttpResponseRedirect
from django.shortcuts import render
from API.models import Client, Product

# Create your views here.
def index(request):
    clients = Client.objects.all()
    return render(request, 'callcenter/index.html', {
        'clients': clients
    })

def create_client(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        identity = request.POST.get('identity')
        phone = request.POST.get('phone')
        total_price = request.POST.get('total_price')
        date_instalation = request.POST.get('date_instalation')
        part_of_day = request.POST.get('part_of_day')
        options_to_give_instalation = request.POST.get('options_to_give_instalation')
        image = request.FILES.get('image')
        
        if part_of_day == "0":
            return render(request, 'callcenter/create_client.html', {
                'message': 'Seleccione una opción para la hora de instalación',
                'products': Product.objects.all()
            })
        
        if options_to_give_instalation == "0":
            return render(request, 'callcenter/create_client.html', {
                'message': 'Seleccione una opción para dar la instalación',
                'products': Product.objects.all()
            })

        # Obtener el estado de los productos seleccionados
        selected_products = request.POST.getlist('status')

        client = Client(
            username=username,
            identity=identity,
            phone=phone,
            total_price=total_price,
            date_instalation=date_instalation,
            part_of_day=part_of_day,
            photo_reciept=image,
            options_to_give_instalation=options_to_give_instalation
        )
        client.save()
        # Guardar los productos comprados
        client.products_bought.set(selected_products)
        client.save()
        
        # Continuar con el resto de la lógica de la vista
        return render(request, 'callcenter/create_client.html', {
            'products': Product.objects.all()
        })
    else:
        return render(request, 'callcenter/create_client.html', {
            'products': Product.objects.all()
        })

def update_client(request):
    if request.method == "POST":
        client_id = request.POST.get('id')
        username = request.POST.get('username')
        identity = request.POST.get('identity')
        phone = request.POST.get('phone')
        date_instalation = request.POST.get('date_instalation')
        part_of_day = request.POST.get('part_of_day')
        options_to_give_instalation = request.POST.get('options_to_give_instalation')

        # Obtener la instancia del cliente
        client = Client.objects.get(id=client_id)

        # Actualizar los campos del cliente
        client.username = username
        client.identity = identity
        client.phone = phone
        client.date_instalation = date_instalation
        client.part_of_day = part_of_day
        client.options_to_give_instalation = options_to_give_instalation

        # Guardar los cambios en la base de datos
        client.save()

        return render(request, 'callcenter/index.html', {
            'clients': Client.objects.all()
        })
    
def delete_client(request, id):
    client = Client.objects.get(id=id)
    client.delete()

    clients = Client.objects.all()
    return render(request, 'callcenter/index.html', {
        'clients': clients
    })