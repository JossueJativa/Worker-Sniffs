from django.shortcuts import get_object_or_404, render
from API.models import Tecnic, Client
import folium
from geopy.geocoders import Nominatim

# Create your views here.
def intro(request):
    return render(request, 'tecnic/intro.html',{
        'tecnic': Tecnic.objects.get(user=request.user)
    })

def client(request, id):
    return render(request, 'tecnic/client.html',{
        'tecnic': Tecnic.objects.get(user=request.user),
        'client': Client.objects.get(id=id)
    })

def change_status(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        client.status_instalation = status
        client.save()

    return render(request, 'tecnic/client.html', {
        'tecnic': Tecnic.objects.get(user=request.user),
        'client': client
    })

def configuration(request):
    tecnic = Tecnic.objects.get(user=request.user)
    geolocator = Nominatim(user_agent="mi_aplicacion")
    if request.method == 'POST':
        city = request.POST.get('city')
        country = request.POST.get('country')
        business_name = request.POST.get('business_name')

        location = geolocator.geocode(f"{business_name}, {city}, {country}")
        latitud = location.latitude
        longitud = location.longitude

        print(latitud, longitud)

        tecnic.location_lat = latitud
        tecnic.location_lon = longitud
        tecnic.business_name = business_name
        tecnic.city = city
        tecnic.country = country

        tecnic.save()

        mapa_final = folium.Map(location=[latitud, longitud], zoom_start=15)
        folium.Marker([latitud, longitud], popup=business_name).add_to(mapa_final)

        # Convertir el mapa a HTML
        mapa_html_final = mapa_final._repr_html_()

        return render(request, 'tecnic/configuration.html', {
            'tecnic': Tecnic.objects.get(user=request.user),
            'map': mapa_html_final
        })

    try:
        mapa_final = folium.Map(location=[str(tecnic.location_lat), str(tecnic.location_lon)], zoom_start=15)
        folium.Marker([tecnic.location_lat, tecnic.location_lon], popup="Tecnico").add_to(mapa_final)

        # Convertir el mapa a HTML
        mapa_html_final = mapa_final._repr_html_()
    except folium.errors.LocationError:
        return render(request, 'tecnic/configuration.html', {
            'tecnic': Tecnic.objects.get(user=request.user),
            'map': ''
        })
    return render(request, 'tecnic/configuration.html', {
        'tecnic': Tecnic.objects.get(user=request.user),
        'map': mapa_html_final
    })