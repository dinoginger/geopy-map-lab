"""
This is our main script for generating maps based on
given coordinates and year of movie being published

Marko Ruzak, APPS_2021, CS-1
6.02.22
"""
import haversine
import pandas as pd
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
            # counter += 1
            # if counter == 5:
            #     break

        except AttributeError:
            pass
    return df


if __name__ == "__main__":
    input_params = argparser().parse_args()
    print(input_params)
    # map = folium.Map(location=[input_params.latitude, input_params.longitude], zoom_start=17)
    dataframe = file_parse(input_params.path)
    print(input_params.year)
    a = dataframe.loc[dataframe["Year"] == str(input_params.year)]
    print(a)
    # <code>
    # map.save("map.html")
