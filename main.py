import folium
import geopy


def read_file(path, year):
    """
    (str) -> (list)
    Return list of lines from file (path to file)
    """
    films = dict()
    with open(path, "r") as file:
        for i in range(14):
            file.readline()
        for i in file:
            if "(" + str(year) + ")" in i or "(" + str(year) + "/" in i:
                i = i.strip()
                if i.split("\t")[-1].startswith("("):
                    films[i.split("\t")[0]] = i.split("\t")[-2]
                else:
                    films[i.split("\t")[0]] = i.split("\t")[-1]
    return films


def make_coordinates(films):
    locat_coord = dict()
    geocoder = geopy.geocoders.ArcGIS()
    for film in films:
        loc = films[film]
        if loc not in locat_coord:
            try:
                film_loc = geocoder.geocode(loc)
                if film_loc:
                    locat_coord[loc] = (film_loc.latitude, film_loc.longitude)
            except:
                c = 0
    for film in films:
        if films[film] in locat_coord:
            films[film] = locat_coord[films[film]]
        else:
            del films[film]
    return films


def map_create(films):
    map = folium.Map()
    fg = folium.FeatureGroup("Films")
    for film in films:
        name = folium.Popup(film, parse_html=True)
        fg.add_child(folium.Marker(location=films[film]))
    map.add_child(fg)
    fg1 = folium.FeatureGroup(name="Dencity")
    fg1.add_child(folium.GeoJson(data=open("world.json", "r",
                                           encoding='utf-8-sig').read(),
                                 style_function=style_dencity))
    map.add_child(fg1)
    map.add_child(folium.LayerControl())
    map.save("map.html")


def style_dencity(x):
    pop = x["properties"]["POP2005"]
    area = x["properties"]["AREA"]
    if area == 0:
        area = 0.1
    if pop / area < 120:
        return {"fillColor": "green"}
    elif 120 <= pop / area < 2000:
        return {"fillColor": "orange"}
    else:
        return {"fillColor": "red"}


def main_func():
    films = read_file("locations.list", int(input()))
    films = make_coordinates(films)
    map_create(films)


main_func()
