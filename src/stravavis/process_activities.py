from __future__ import annotations

import pandas as pd


def process_activities(activities_path):
    # Import activities.csv from Strava bulk export zip
    activities = pd.read_csv(activities_path)

    # Further processing (to come)

    return activities
