import folium
import pymongo
from geopy.geocoders import Nominatim
import webbrowser
from geopy.distance import geodesic

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="mon_application")

# Demander l'adresse à l'utilisateur
adresse = input("Entrez une adresse avec la ville ou le code postal: ")

# Géocoder l'adresse
location = geolocator.geocode(adresse)

# Vérifier si une localisation a été trouvée
if location:
    print(f"Latitude : {location.latitude}")
    print(f"Longitude : {location.longitude}")

    m = folium.Map(location=[location.latitude, location.longitude], tiles="OpenStreetMap", zoom_start=16)
    street_view_url1 = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={location.latitude}, {location.longitude}"

    msg_html1 = f"""
                <div style="font-family: Arial, sans-serif; width: 250px;">
                    <h3 style="color: #4a4a4a; margin-bottom: 10px;">{adresse}</h3>
                    <img src="depart.jpg" style="width: 100%; margin-bottom: 10px;">   
                 
                    <a href="{street_view_url1}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 10px;">Voir dans Street View</a>
                </div>
                """
    folium.Marker([location.latitude, location.longitude], popup=folium.Popup(msg_html1, max_width=300), icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

    # connection au serveur mongodb
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["yutopiaDB"]
    mycol = mydb["velib-tr-collection"]
    Cursor = mycol.find()
    tablo_stations = list(Cursor)

    # liste des stations
    for station in tablo_stations:
        station_location = (station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon'])
        distance = geodesic((location.latitude, location.longitude), station_location).meters
        if distance < 500:
            msg1 = f"{station['ebike']} vélos électriques"
            msg2 = f"{station['mechanical']} vélos mécaniques"
            msg3 = f"{station['numdocksavailable']} docks disponibles"
            msg4 = f"Distance: {int(distance)} mètres"

            street_view_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={station['coordonnees_geo']['lat']},{station['coordonnees_geo']['lon']}"

            msg_html = f"""
            <div style="font-family: Arial, sans-serif; width: 250px;">
                <h3 style="color: #4a4a4a; margin-bottom: 10px;">{station['name']}</h3>
                <img src="velib.jpg" style="width: 100%; margin-bottom: 10px;">   
                <p style="color: #666; margin: 5px 0;">{msg1}</p>
                <p style="color: #666; margin: 5px 0;">{msg2}</p>
                <p style="color: #666; margin: 5px 0;">{msg3}</p>
                <p style="color: #666; margin: 5px 0; font-weight: bold;">{msg4}</p>
                <a href="{street_view_url}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 10px;">Voir dans Street View</a>
            </div>
            """

            folium.Marker([station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon']],
                          popup=folium.Popup(msg_html, max_width=300)).add_to(m)

    # save the map
    m.save("map.html")
    print("Map saved as map.html")
    # open the map
    webbrowser.open('map.html')

else:
    print("Adresse non trouvée.")
