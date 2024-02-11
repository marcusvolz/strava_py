from __future__ import annotations

from math import log, pi, tan

import matplotlib.pyplot as plt
from rich.progress import track

# Dummy units
MAP_WIDTH = 1
MAP_HEIGHT = 1


def convert_x(lon):
    # Get x value
    x = (lon + 180) * (MAP_WIDTH / 360)
    return x


def convert_y(lat):
    # Convert from degrees to radians
    lat_rad = lat * pi / 180

    # Get y value
    mercator_n = log(tan((pi / 4) + (lat_rad / 2)))
    y = (MAP_HEIGHT / 2) + (MAP_WIDTH * mercator_n / (2 * pi))
    return y


def plot_map(
    df,
    lon_min=None,
    lon_max=None,
    lat_min=None,
    lat_max=None,
    alpha=0.3,
    linewidth=0.3,
    output_file="map.png",
):
    # Create a new figure
    plt.figure()

    # Remove data outside the input ranges for lon / lat
    if lon_min is not None:
        df = df[df["lon"] >= lon_min]

    if lon_max is not None:
        df = df[df["lon"] <= lon_max]

    if lat_min is not None:
        df = df[df["lat"] >= lat_min]

    if lat_max is not None:
        df = df[df["lat"] <= lat_max]

    # Create a list of activity names
    activities = df["name"].unique()

    # Plot activities one by one
    for activity in track(activities, "Plotting activities"):
        x = df[df["name"] == activity]["lon"]
        y = df[df["name"] == activity]["lat"]

        # Transform to Mercator projection so maps aren't squashed away from equator
        x = x.transform(convert_x)
        y = y.transform(convert_y)

        plt.plot(x, y, color="black", alpha=alpha, linewidth=linewidth)

    # Update plot aesthetics
    plt.axis("off")
    plt.axis("equal")
    plt.margins(0)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
    plt.savefig(output_file, dpi=600)
