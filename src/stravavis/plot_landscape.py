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
    n = len(activities)

    # Normalize dist
    processed = []

    for i in track(range(n), "Processing tracks"):
        df_i = df[df['name'] == activities[i]]
        df_i["dist_norm"] = (df_i["dist"] - df_i["dist"].min()) / (df_i["dist"].max() - df_i["dist"].min())
        processed.append(df_i)

    df = pd.concat(processed)

    # Plot activities one by one
    for i in track(range(n), "Plotting activities"):
        X = df[df['name'] == activities[i]]['dist_norm']
        Y = df[df['name'] == activities[i]]['ele']
        plt.fill_between(X, Y, color = 'black', alpha = 0.03, linewidth = 0)
        plt.plot(X, Y, color = 'black', alpha = 0.125, linewidth = 0.25)

    # Update plot aesthetics
    plt.axis('off')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    plt.savefig(output_file, dpi = 600)
