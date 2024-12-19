import webbrowser
import folium
import pymongo
from branca.element import IFrame

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["YutopiaDB"]
mycol = mydb["velib"]
Cursor = mycol.find()
tablo_stations = list(Cursor)

m = folium.Map(location=[48.821270, 2.311693], tiles="OpenStreetMap", zoom_start=15)

i = 0
for station in tablo_stations:
    print(station['coordonnees_geo']['lat'])
    lat = station['coordonnees_geo']['lat']
    lon = station['coordonnees_geo']['lon']
#    except (KeyError, TypeError):
 #       print(f"Coordonnées manquantes ou incorrectes pour la station : {station['name']}")
  #      continue

    print(station)
    print(station['coordonnees_geo'])
    print(station['name'])
    print("il reste ", station['ebike'], "vélos électrique à la station ", station['name'])
    print("il reste ", station['mechanical'], "vélos mécaniques à la station ", station['name'])
    #     nb de docks dispo
    print("il reste ", station['numdocksavailable'], "docks disponibles à la station ", station['name'])

    msg1 = f"{station['ebike']} vélos électriques"
    msg2 = f"{station['mechanical']} vélos mécaniques"
    msg3 = f"{station['numdocksavailable']} docks disponibles"

    html = f"""
    <html>
    <head>
        <style>
            .station-popup {{
                font-family: Arial, sans-serif;
                padding: 10px;
                max-width: 200px;
                box-shadow: 8px 8px 12px #aaa;
            }}
            .station-name {{
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }}
            .station-info {{
                font-size: 14px;
                color: #666;
                margin-bottom: 5px;
            }}
            .street-view-link {{
                display: inline-block;
                margin-top: 10px;
                padding: 5px 10px;
                background-color: #4285F4;
                color: white;
                text-decoration: none;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body>
        <div class="station-popup">
            <div class="station-name">{station['name']}</div>
            <div class="station-info">{msg1}</div>
            <div class="station-info">{msg2}</div>
            <div class="station-info">{msg3}</div>
            <a href="https://www.google.com/maps?layer=c&cbll={station['coordonnees_geo']['lat']},{station['coordonnees_geo']['lon']}" target="_blank" class="street-view-link">View in Street View</a>
        </div>
    </body>
    </html>
    """

    iframe = IFrame(html=html, width=220, height=150)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(
        [station['coordonnees_geo']['lat'], station['coordonnees_geo']['lon']],
        popup=popup
    ).add_to(m)

    i += 1
    if i == 10:
        break

m.save("velib_map.html")
webbrowser.open('velib_map.html')
