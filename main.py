"""
This is our main script for generating maps based on
given coordinates and year of movie being published

Marko Ruzak, APPS_2021, CS-1
6.02.22
"""

import argparse

def argparser():
    parser = argparse.ArgumentParser(description='Process input parameters for generating'
                                                 'geo map script.')
    parser.add_argument('latitude', metavar='Latitude', type=float,
                        help='latitude for generating geo map.')
    parser.add_argument('longitude', metavar='Longitude', type=float,
                        help='longitude for generating geo map.')
    parser.add_argument('year', metavar='Year', type=int,
                        help='year of publishing for movies, for generating geo map.')
    parser.add_argument('path', metavar='Path to file', type=float,
                        help='Path to the film db file. '
                             'Contains coordinates and year of publishing')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

if __name__ == "__main__":
    argparser()