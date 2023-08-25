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
    elif fpath.endswith(".db"):
        return process_sqlite(fpath)


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

    for activity_track in activity.tracks:
        for segment in activity_track.segments:
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

# process a cyclemeter database file.
def process_sqlite(path):
    '''Process a cyclemeter db file

    sqlite database, using the following fields of tables:

    coordinates (runid, sequenceid, timeOffset, latitude, longitude, distanceDelta)
    altitude (runid, sequenceid, timeOffset, distanceDelta, altitude)
    run (runid, startTime)


    timeOffset is an offset from the startTime in the run
    distanceDelta is the distance from the previous reading

    coordinates and altitude have the same runid, but the sequence ids
    are different, as are the time of capture. There are ~2x as many
    coordinates as altitude readings.
    '''

    import sqlite3
    import numpy as np

    with sqlite3.connect(path) as con:
        coords = pd.read_sql_query('''
            select
              runID,
              startTime,
              timeOffset,
              latitude as lat,
              longitude as lon,
              sum(distanceDelta) over(partition by runid order by sequenceId) as dist
            from coordinate
            inner join run using (runid)
        ''', con)
        altitudes = pd.read_sql_query('''
            select
              runID,
              timeOffset,
              altitude as ele
            from altitude
        ''', con)

    coords['ele'] = np.NaN

    ## Interpolating the elevation from the sparser altitude table to the denser coords table.

    # Need to do each 'run' (activity) separately, so that the interpolations don't leak between the activities.
    for runID in pd.unique(coords['runID']):
        _c = coords[['timeOffset', 'ele']][(coords['runID'] == runID)]
        _a = altitudes[['timeOffset', 'ele']][(altitudes['runID'] == runID)]
        # keys enable a multiindex, keeping track of which items come from which source
        both = pd.concat([_c, _a], keys=['c', 'a']).sort_values(['timeOffset']).interpolate(limit_direction='both')
        # .xs pulls out the coords from the multiindex
        coords.loc[coords['runID'] == runID, ['ele']] = both.xs('c')['ele']

    coords['time'] = pd.to_datetime(coords['startTime']) + pd.to_timedelta(coords['timeOffset'], unit='S')

    coords = coords.rename(columns={'runID': 'name'})

    return coords[['lon', 'lat', 'ele', 'time', 'name', 'dist']]



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
