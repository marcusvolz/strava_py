import glob

import fit2gpx
import gpxpy
import pandas as pd
from rich.progress import track


# Function for processing (unzipped) GPX and FIT files in a directory (path)
def process_data(path):
    
    # Function for processing an individual GPX file
    # Ref: https://pypi.org/project/gpxpy/
    def process_gpx(gpxfile):
        
        activity = gpxpy.parse(open(gpxfile))

        lon = []
        lat = []
        ele = []
        time = []
        name = []

        for track in activity.tracks:
            for segment in track.segments:
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
        
        df = pd.DataFrame(
                list(zip(lon, lat, ele, time, name)),
                columns = ['lon', 'lat', 'ele', 'time', 'name']
            )
        
        return df
    
    # Function for processing an individual FIT file
    # Ref: https://github.com/dodo-saba/fit2gpx 
    def process_fit(fitfile):
        conv = fit2gpx.Converter()
        df_lap, df = conv.fit_to_dataframes(fname = fitfile)
        
        df['name'] = fitfile
        df = df[['longitude', 'latitude', 'altitude', 'timestamp', 'name']]
        df = df.rename(columns = {'longitude': 'lon', 'latitude': 'lat', 'altitude': 'ele', 'timestamp': 'time'})
        
        return df
    
    
    # Process all files (GPX or FIT)
    processed = []

    for fpath in track(glob.glob(path), description="Processing:"):
        if fpath.endswith('.gpx'):
            processed.append(process_gpx(fpath))
        elif fpath.endswith('.fit'):
            processed.append(process_fit(fpath))
        print('Processing: ' + fpath)

    df = pd.concat(processed)
    
    df['time'] = pd.to_datetime(df['time'], utc = True)
    
    return df
