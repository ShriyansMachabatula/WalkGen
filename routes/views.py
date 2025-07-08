from django.shortcuts import render
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx


def home(request):
    route_data = None
    if request.method == "POST":
        start = request.POST.get('start')
        end = request.POST.get('end')
        time_limit = request.POST.get('time_limit')

        geolocator = Nominatim(user_agent="walkgen_app")
        start_location = geolocator.geocode(start)
        end_location = geolocator.geocode(end)

        G = ox.graph_from_point((start_location.latitude, start_location.longitude), dist=3000, network_type="walk")
        start_node = ox.nearest_nodes(G, start_location.longitude, start_location.latitude)
        end_node = ox.nearest_nodes(G, end_location.longitude, end_location.latitude)

        route = nx.shortest_path(G, start_node, end_node, weight='length')

        route_length = nx.shortest_path_length(G, start_node, end_node, weight='length')

        walking_speed_mpm = 83.33
        estimated_time = route_length/walking_speed_mpm
        if not start_location or not end_location:
            route_data = {
                'error': 'Invalid start or end location'
            }
        else: 
            route_data = {
                'start': start,
                'start_coords': (start_location.latitude, start_location.longitude),
                'end': end,
                'end_coords': (end_location.latitude, end_location.longitude),
                'time_limit': time_limit,
                'route_length_m': round(route_length, 2),
                'estimated_time_min': round(estimated_time, 2),
                'walkable': float(time_limit) >= estimated_time
            }

    return render(request, "routes/home.html", {'route_data': route_data})