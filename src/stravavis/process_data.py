from __future__ import annotations

import hashlib
import math
import tempfile
from multiprocessing import Pool
from pathlib import Path

import fit2gpx
import gpxpy
import pandas as pd
from rich.progress import track


def process_file(fpath: str) -> pd.DataFrame | None:
    if fpath.endswith(".gpx"):
        df = process_gpx(fpath)
    elif fpath.endswith(".fit"):
        df = process_fit(fpath)
    else:
        return None

    if df is not None and not df.empty:
        # Convert to UTC then strip timezone to avoid concat issues with
        # incompatible timezone types (gpxpy's SimpleTZ vs datetime.timezone)
        df = df.assign(time=pd.to_datetime(df["time"], utc=True).dt.tz_localize(None))

    return df


# Function for processing an individual GPX file
# Ref: https://pypi.org/project/gpxpy/
def process_gpx(gpxfile: str) -> pd.DataFrame | None:
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

    for activity_track in activity.tracks:
        for segment in activity_track.segments:
            if not segment.points:
                continue

            x0 = segment.points[0].longitude
            y0 = segment.points[0].latitude
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
def process_fit(fitfile: str) -> pd.DataFrame:
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


def load_cache(filenames: list[str]) -> tuple[Path, pd.DataFrame | None]:
    # Create a cache key from the filenames
    key = hashlib.md5("".join(filenames).encode("utf-8")).hexdigest()

    # Create a cache directory
    dir_name = Path(tempfile.gettempdir()) / "stravavis"
    dir_name.mkdir(parents=True, exist_ok=True)
    cache_filename = dir_name / f"cached_activities_{key}.pkl"
    print(f"Cache filename: {cache_filename}")

    # Load cache if it exists
    try:
        df = pd.read_pickle(cache_filename)
        print("Loaded cached activities")
        return cache_filename, df
    except FileNotFoundError:
        print("Cache not found")
        return cache_filename, None


# Function for processing (unzipped) GPX and FIT files in a directory (path)
def process_data(filenames: list[str]) -> pd.DataFrame:
    # Process all files (GPX or FIT)
    cache_filename, df = load_cache(filenames)
    if df is not None:
        return df

    with Pool() as pool:
        try:
            it = pool.imap_unordered(process_file, filenames)
            it = track(it, total=len(filenames), description="Processing")
            processed = list(it)
        finally:
            pool.close()
            pool.join()

    # Filter out None and empty DataFrames before concatenating
    processed = [p for p in processed if p is not None and not p.empty]

    df = pd.concat(processed)

    # Add UTC timezone back (was stripped in process_file to allow concat)
    df = df.assign(time=df["time"].dt.tz_localize("UTC"))

    # Save cache
    df.to_pickle(cache_filename)

    return df
