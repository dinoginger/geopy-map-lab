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
    pass


if __name__ == "__main__":
    input_params = argparser().parse_args()
    print(input_params)
    map = folium.Map(location=[input_params.latitude, input_params.longitude], zoom_start=17)

    # <code>

    map.save("map.html")