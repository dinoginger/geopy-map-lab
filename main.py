"""
This is our main script for generating maps based on
given coordinates and year of movie being published

Marko Ruzak, APPS_2021, CS-1
6.02.22
"""
import haversine
import pandas
import folium
import argparse
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


def file_parse(path: str):
    """
    Parses file into pandas db
    COMPLETE!
    :param path:
    :return:
    """
    file = open(path, "r", encoding="ISO-8859-1")
    lines = file.readlines()
    file.close()
    for line in lines:
        try:
            name = re.search("\"(.*?)\"", line).group()  # selects text inside ""
            year = re.search("([0-9]{4})", line).group()  # selects groups of 4 numbers in a row
            location = re.search("(?<=\(([0-9]{4})\)).*", line).group() # selects all text after 4 digits in a row excluded            print(year)
            # TODO: <create pd DataFrame and check columns for duplicate names>
        except AttributeError:
            pass



if __name__ == "__main__":
    input_params = argparser().parse_args()
    print(input_params)
    map = folium.Map(location=[input_params.latitude, input_params.longitude], zoom_start=17)
    file_parse(input_params.path)
    # <code>

    map.save("map.html")