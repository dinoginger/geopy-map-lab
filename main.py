"""
This is our main script for generating maps based on
given coordinates and year of movie being published

Marko Ruzak, APPS_2021, CS-1
6.02.22
"""
from haversine import haversine
import pandas as pd
import folium
import argparse
from geopy.geocoders import Nominatim
import re


def argparser():
    parser = argparse.ArgumentParser(description='Process input parameters for generating'
                                                 ' geo map script.')
    parser.add_argument('latitude', metavar='Latitude', type=float,
                        help='latitude for generating geo map.')
    parser.add_argument('longitude', metavar='Longitude', type=float,
                        help='longitude for generating geo map.')
    parser.add_argument('year', metavar='Year', type=int,
                        help='year of publishing for movies, for generating geo map.')
    parser.add_argument('path', metavar='Path', type=str,
                        help='Path to the film db file. '
                             'Contains coordinates and year of publishing')
    return parser


def file_parse(path: str) -> pd.DataFrame:
    """
    Parses file (using regular expressions) into pandas db
    COMPLETE!
    :param path:
    :return:
    """
    df = pd.DataFrame(columns=["Name", "Year", "Location"])
    file = open(path, "r", encoding="ISO-8859-1")  # Change if needed
    lines = file.readlines()
    file.close()
    for line in lines:
        try:
            name = re.search("\"(.*?)\"", line).group()  # selects text inside ""
            year = re.search("([0-9]{4})", line).group()  # selects groups of 4 numbers in a row
            location = re.search("(?<=\(([0-9]{4})\)).*",
                                 line).group().strip()  # selects all text after 4 digits in a row excluded
            location = re.search("(?<=}).*", location).group().strip()
            new_df = pd.DataFrame({
                "Name": [name],
                "Year": [year],
                "Location": [location]
            })
            df = pd.concat([df, new_df], ignore_index=True)
        except AttributeError:
            pass
    return df


def get_top_coordinates(df: pd.DataFrame, year: int, latitude, longitude):
    top_distances = {0: 100000}
    top_coord = {}
    locator = Nominatim(user_agent="webmap_lab")
    this_years = df.loc[df["Year"] == str(year)]
    for index, row in this_years.iterrows():
        try:
            location = row["Location"]
            coordinates = locator.geocode(location)
            if coordinates is None:
                if location.find("(") != -1:  # if parentheses found, remove
                    location = re.sub("[\(].*?[\)]", "", location)  # to remove "()"
                    coordinates = locator.geocode(location)

            pl_lat = coordinates.latitude
            pl_long = coordinates.longitude
        except AttributeError:
            parts = location.split(",")  # remove first part of location
            parts.pop(0)
            location = ", ".join(parts)
            coordinates = locator.geocode(location)

        distance = haversine((latitude, longitude),
                             (pl_lat, pl_long), unit="km")
        if len(top_distances.values()) < 10:
            top_distances[index] = distance
            top_coord[index] = (pl_lat, pl_long)
            continue

        if distance < max(top_distances.values()):
            if len(top_distances.values()) == 10:
                key_to_delete = max(top_distances, key=lambda k: top_distances[k])
                del top_distances[key_to_delete]
                del top_coord[key_to_delete]
                top_distances[index] = distance
                top_coord[index] = (pl_lat, pl_long)
            else:
                top_distances[index] = distance
                top_coord[index] = (pl_lat, pl_long)
    return top_coord


def create_map(mapp: folium.Map, top_10: dict, df: pd.DataFrame, year: int):
    locations = folium.FeatureGroup(name=f"All {year}'s Movie Locations")
    for movie in top_10:
        name = df.loc[movie]["Name"]
        location = top_10[movie]
        popup = df.loc[movie]["Name"]
        locations.add_child(folium.Marker(name=name, location=location, popup=popup))
    mapp.add_child(locations)
    return mapp


def main():
    input_params = argparser().parse_args()
    mapp = folium.Map(location=[input_params.latitude, input_params.longitude], zoom_start=3)
    folium.CircleMarker(location=(input_params.latitude, input_params.longitude),
                        radius=5, popup='I am here!',
                        color='red', fill=True, fill_color='red').add_to(mapp)
    dataframe = file_parse(input_params.path)
    try:
        top_coordinates = get_top_coordinates(dataframe, input_params.year,
                                              input_params.latitude, input_params.longitude)
    except AttributeError:
        pass
    mapp = create_map(mapp, top_coordinates, dataframe, input_params.year)
    mapp.save("map.html")


if __name__ == "__main__":
    main()
