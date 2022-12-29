import glob
import math
from multiprocessing import Pool

import fit2gpx
import gpxpy
import pandas as pd
from rich.progress import track


def process_file(fpath):
    if fpath.endswith(".gpx"):
        return process_gpx(fpath)
    elif fpath.endswith(".fit"):
        return process_fit(fpath)


# Function for processing an individual GPX file
# Ref: https://pypi.org/project/gpxpy/
def process_gpx(gpxfile):
    with open(gpxfile, encoding="utf-8") as f:
        try:
            activity = gpxpy.parse(f)
        except gpxpy.mod_gpx.GPXException as e:
            print(f"\nSkipping {gpxfile}: {type(e).__name__}: {e}")
            return None

    lon = []
    lat = []
    ele = []
    time = []
    name = []
    dist = []

    for track in activity.tracks:
        for segment in track.segments:
            x0 = activity.tracks[0].segments[0].points[0].longitude
            y0 = activity.tracks[0].segments[0].points[0].latitude
            d0 = 0
            for point in segment.points:
                x = point.longitude
                y = point.latitude
                z = point.elevation
                t = point.time
                lon.append(x)
                lat.append(y)
                ele.append(z)
                time.append(t)
                name.append(gpxfile)
                d = d0 + math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2))
                dist.append(d)
                x0 = x
                y0 = y
                d0 = d

    df = pd.DataFrame(
        list(zip(lon, lat, ele, time, name, dist)),
        columns=["lon", "lat", "ele", "time", "name", "dist"],
    )

    return df


# Function for processing an individual FIT file
# Ref: https://github.com/dodo-saba/fit2gpx
def process_fit(fitfile):
    conv = fit2gpx.Converter()
    df_lap, df = conv.fit_to_dataframes(fname=fitfile)

    df["name"] = fitfile

    dist = []

    for i in range(len(df.index)):
        if i < 1:
            x0 = df["longitude"][0]
            y0 = df["latitude"][0]
            d0 = 0
            dist.append(d0)
        else:
            x = df["longitude"][i]
            y = df["latitude"][i]
            d = d0 + math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2))
            dist.append(d)
            x0 = x
            y0 = y
            d0 = d

    df = df.join(pd.DataFrame({"dist": dist}))
    df = df[["longitude", "latitude", "altitude", "timestamp", "name", "dist"]]
    df = df.rename(
        columns={
            "longitude": "lon",
            "latitude": "lat",
            "altitude": "ele",
            "timestamp": "time",
        }
    )

    return df


# Function for processing (unzipped) GPX and FIT files in a directory (path)
def process_data(path):

    # Process all files (GPX or FIT)
    filenames = glob.glob(path)

    with Pool() as pool:
        try:
            it = pool.imap_unordered(process_file, filenames)
            it = track(it, total=len(filenames), description="Processing")
            processed = list(it)
        finally:
            pool.close()
            pool.join()

    df = pd.concat(processed)

    df["time"] = pd.to_datetime(df["time"], utc=True)

    return df
