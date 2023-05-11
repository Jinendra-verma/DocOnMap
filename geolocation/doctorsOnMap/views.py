from django.shortcuts import render
import folium
import requests
from geopy.distance import distance

BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'



postcodes = ['474001' , '475110' , '475001' , '474003' , '474010' , '250004' , '247667']

# Create your views here.

def map_view(request):
    # retrieve latitude and longitude values from database

    postcode = '474011'
    # address = 'ravindra bhawan, IIT Roorkee, Roorkee, Uttarakhand, 247667, India'
    response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=India")
    data = response.json()
    Userlatitude = data[0].get('lat')
    Userlongitude = data[0].get('lon')
    print(Userlatitude,Userlongitude)

    # if request.method == "POST":
    #     Userlatitude = request.POST.get("latitude")
    #     Userlongitude = request.POST.get("longitude")
    #     print(Userlatitude,Userlongitude)
    
        
    Userlocation = (Userlatitude,Userlongitude)

    my_map = folium.Map(location=Userlocation, zoom_start=10)
    folium.Marker(location=Userlocation, icon=folium.Icon(color='red')).add_to(my_map) 

    for code in postcodes:
        response = requests.get(f"{BASE_URL}&postalcode={code}&country=India")
        data = response.json()
        Doclocation = (data[0].get('lat') , data[0].get('lon'))
        # latitude = data[0].get('lat')
        # longitude = data[0].get('lon')
        # folium.Marker(location=Doclocation).add_to(my_map)
        dis = distance(Userlocation,Doclocation)

        if dis<50.0 :
            popup = folium.Popup("<a href='https://www.cricbuzz.com/'><img src='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png' alt='profile pic' style='float:left; margin-right:10px;' width='50' height='50'><p style='float:right'>Dr. Alok Sharma</p><br><p style='color:black;'> Dermatologist</p></a>")
            folium.Marker(location=Doclocation, popup=popup, tooltip='<b>Dr. Alok Sharma</b>').add_to(my_map)   

            # icon_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
            # html = f"<div style='height:auto ; width:auto'><img src='{icon_url}' width='50' height='50' style='float: left; margin-right: 10px'><p style='float: left'><b>Dr. Alok Sharma</b><br>Dermatologist</p></div>"
            # popup = folium.Popup(html)
            
            # marker = folium.Marker(location=Doclocation, popup=popup, tooltip='<b>Dr. Alok Sharma</b>')
            # marker.add_to(my_map)
            
    
    map_html = my_map._repr_html_()
    return render(request, 'map.html', {'map_html': map_html})

