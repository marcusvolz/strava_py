import pandas as pd
from .plot_calendar import ACTIVITY_FORMAT

def process_activities(activities_path):
    # Import activities.csv from Strava bulk export zip
    activities = pd.read_csv(activities_path)

    # Further processing (to come)

    return activities



def process_sqlite_activities(path):
    import sqlite3

    with sqlite3.connect(path) as con:
        activities = pd.read_sql_query('''
            select
              runID,
              startTime as "Activity Date",
              startTimeZone,
              distance as "Distance",
              runTime as "Elapsed Time"
            from run
        ''', con)

    activities['Activity Date'] = pd.to_datetime(activities['Activity Date'])
    for (ix, row) in activities.iterrows():
        activities.loc[ix, ['Activity Date']] = row['Activity Date'].tz_localize(row['startTimeZone'])

    activities['Activity Date'] = pd.to_datetime(activities['Activity Date'], utc=True).dt.strftime(date_format=ACTIVITY_FORMAT)

    return activities
