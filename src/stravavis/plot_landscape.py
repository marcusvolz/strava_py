import matplotlib.pyplot as plt
import pandas as pd
from rich.progress import track


def plot_landscape(df, output_file = 'landscape.png'):

    # Create a new figure
    plt.figure()

    # Convert ele to numeric
    df['ele'] = pd.to_numeric(df['ele'])
    
    # Create a list of activity names
    activities = df['name'].unique()

    # Normalize dist
    processed = []

    for activity in track(activities, "Processing tracks"):
        df_i = df[df['name'] == activity]
        df_i["dist_norm"] = (df_i["dist"] - df_i["dist"].min()) / (df_i["dist"].max() - df_i["dist"].min())
        processed.append(df_i)

    df = pd.concat(processed)

    # Plot activities one by one
    for activity in track(activities, "Plotting activities"):
        x = df[df['name'] == activity]['dist_norm']
        y = df[df['name'] == activity]['ele']
        plt.fill_between(x, y, color='black', alpha=0.03, linewidth=0)
        plt.plot(x, y, color='black', alpha=0.125, linewidth=0.25)

    # Update plot aesthetics
    plt.axis('off')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    plt.savefig(output_file, dpi = 600)
