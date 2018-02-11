import folium
import geopy


def read_file(path, year):
    """
    (str) -> (dict)
    Return dict with name of films as key and adress as value
    """
    films = dict()
    with open(path, "r", encoding='utf-8', errors='ignore') as file:
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


'''
# We can use this instead of make_coordinates2 (this variant is slower)
def make_coordinates1(films):
    """
    (dict) -> (dict)
    Transfer adress to tuple of coordinates for all films in list films
    """
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
'''


def make_coordinates(films):
    """
    (dict) -> (dict)
    Transfer adress to tuple of coordinates for all films in list films
    """
    films_loc = dict()
    with open("locations.tsv", "r", encoding='utf-8') as file:
        for i in range(1):
            file.readline()
        for i in file:
            lat = float(i.split("\t")[1])
            lon = float(i.split("\t")[2].strip())
            films_loc[i.split("\t")[0]] = (lat, lon)
    for film in films:
        if films[film] in films_loc:
            films[film] = films_loc[films[film]]
    return films


def map_create(films, year, markers):
    """
    (dict, int, int) -> None
    Create map with tree layers: films, dencity of country and urban areas
    """
    # create map
    map = folium.Map()
    # add films to map
    fg_films = folium.FeatureGroup("Films")
    for film in films:
        try:
            if markers == 0:
                break
            fg_films.add_child(folium.Marker(location=films[film]))
            markers-=1
        except:
            c=0
    map.add_child(fg_films)
    # add dencity to map
    fg_dencity = folium.FeatureGroup(name="Dencity")
    fg_dencity.add_child(folium.GeoJson(data=open("world.json", "r",
                                                  encoding='utf-8-sig').read(),
                                        style_function=style_dencity))
    map.add_child(fg_dencity)
    # add urban areas to map
    fg_urban = folium.FeatureGroup(name="Urban areas")
    fg_urban.add_child(folium.GeoJson(data=open(
        "urban_areas.geojson", "r",
        encoding='utf-8-sig').read()))
    map.add_child(fg_urban)
    # add layer control and save map to map.html
    map.add_child(folium.LayerControl())
    map.save("map_{}.html".format(year))


def style_dencity(x):
    """
    (dict) -> (dict)
    Return color for country depends to dencity in that country
    """
    # population in country
    pop = x["properties"]["POP2005"]
    # area of country
    area = x["properties"]["AREA"]
    if area == 0:
        return {"fillColor": "gray"}
    if pop / area < 120:
        return {"fillColor": "green"}
    elif 120 <= pop / area < 2000:
        return {"fillColor": "orange"}
    else:
        return {"fillColor": "red"}


def main_func():
    """
    For year create map with marker of film's location, dencity, urban years
    """
    year = int(input("For what year you want location of films: "))
    markers = int(input("How many markers of films do you want: "))
    films = read_file("locations.list", year)
    films = make_coordinates(films)
    map_create(films, year, markers)


main_func()
