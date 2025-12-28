from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from rich.progress import track


def plot_landscape(df, output_file="landscape.png"):
    # Create a new figure
    plt.figure()

    # Convert ele to numeric and normalise dist using vectorised groupby
    df = df.assign(
        ele=pd.to_numeric(df["ele"]),
        dist_norm=df.groupby("name")["dist"].transform(
            lambda x: (x - x.min()) / (x.max() - x.min())
        ),
    )

    # Process and plot activities
    for activity in track(df["name"].unique(), "Plotting activities"):
        activity_data = df[df["name"] == activity]
        x = activity_data["dist_norm"]
        y = activity_data["ele"]
        plt.fill_between(x, y, color="black", alpha=0.03, linewidth=0)
        plt.plot(x, y, color="black", alpha=0.125, linewidth=0.25)

    # Update plot aesthetics
    plt.axis("off")
    plt.margins(0)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
    plt.savefig(output_file, dpi=600)
