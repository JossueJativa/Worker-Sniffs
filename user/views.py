from django.shortcuts import render
from API.models import Client, Tecnic

import folium
from geopy.geocoders import Nominatim

# Create your views here.
def index(request, identity):
    client = Client.objects.get(identity=identity)
    try:
        tecnic = Tecnic.objects.get(clients=client)
    except Tecnic.DoesNotExist:
        return render(request, 'user/index.html', {
            'client': client,
            'tecnic': '',
            'map': ''
        })
    lat = str(tecnic.location_lat)
    lon = str(tecnic.location_lon)

    lat = lat.replace(",", ".")
    lon = lon.replace(",", ".")

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
    return render(request, 'user/index.html', {
        'client': client,
        'tecnic': tecnic,
        'map': mapa_html_final,
        'lat': lat,
        'lon': lon
    })