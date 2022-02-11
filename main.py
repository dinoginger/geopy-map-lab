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
    counter = 0
    for line in lines:
        try:
            name = re.search("\"(.*?)\"", line).group()  # selects text inside ""
            year = re.search("([0-9]{4})", line).group()  # selects groups of 4 numbers in a row
            location = re.search("(?<=\(([0-9]{4})\)).*", line).group().strip() # selects all text after 4 digits in a row excluded            print(year)
            location = re.search("(?<=}).*", location).group().strip()
            new_df = pd.DataFrame({
                "Name": [name],
                "Year": [year],
                "Location": [location]
            })
            df = pd.concat([df, new_df], ignore_index=True)
            counter += 1
            if counter == 100:
                 break

        except AttributeError:
            pass
    return df


def get_top_coordinates(df: pd.DataFrame, year: int, latitude, longitude):
    top_coord = {0: 100000}
    locator = Nominatim(user_agent="webmap_lab")
    a = df.loc[dataframe["Year"] == str(year)]
    for index, row in df.iterrows():
        try:
            location = row["Location"]
            coordinates = locator.geocode(location)
            print(coordinates)
            if coordinates is None:
                print("HERE")
                if location.find("(") != -1: # if parentheses found, remove
                    print("IN IF")
                    location = re.sub("[\(].*?[\)]", "", location) # to remove "()"
                    coordinates = locator.geocode(location)

            pl_lat = coordinates.latitude
            pl_long = coordinates.longitude
        except AttributeError:
            # print("found a mistake ", location)
            parts = location.split(",")  # remove first part of location
            parts.pop(0)
            location = ", ".join(parts)
            coordinates = locator.geocode(location)
            # print("finised, ", coordinates.latitude, coordinates.longitude)


        distance = haversine((latitude, longitude),
                             (pl_lat, pl_long), unit="km")
        if len(top_coord.values()) < 10:
            top_coord[index] = distance
            continue

        if distance < max(top_coord.values()):
            if len(top_coord.values()) == 10:
                key_to_delete = max(top_coord, key=lambda k: top_coord[k])
                del top_coord[key_to_delete]
                top_coord[index] = distance
            else:
                top_coord[index] = distance
    return top_coord


    #results = a.apply(locator.geocode(a.Location))
    #print(results)


if __name__ == "__main__":
    input_params = argparser().parse_args()
    print(input_params)
    map = folium.Map(location=[input_params.latitude, input_params.longitude], zoom_start=17)
    dataframe = file_parse(input_params.path)
    print(input_params.year)
    a = dataframe.loc[dataframe["Year"] == str(input_params.year)]
    print(a)
    try:
        top_coordinates = get_top_coordinates(dataframe, input_params.year,
                   input_params.latitude, input_params.longitude)
        print(top_coordinates)

    except AttributeError:
        pass
    map.save("map.html")
