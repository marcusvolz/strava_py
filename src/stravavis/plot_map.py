import matplotlib.pyplot as plt
from rich.progress import track


def plot_map(df, lon_min=None, lon_max= None, lat_min=None, lat_max=None,
             alpha=0.3, linewidth=0.3, output_file="map.png"):

    # Create a new figure
    plt.figure()

    # Remove data outside the input ranges for lon / lat
    if lon_min is not None:
        df = df[df['lon'] >= lon_min]
    
    if lon_max is not None:
        df = df[df['lon'] <= lon_max]
    
    if lat_min is not None:
        df = df[df['lat'] >= lat_min]
    
    if lat_max is not None:
        df = df[df['lat'] <= lat_max]

    # Create a list of activity names
    activities = df['name'].unique()

    # Plot activities one by one
    for activity in track(activities, "Plotting activities"):
        x = df[df['name'] == activity]['lon']
        y = df[df['name'] == activity]['lat']
        plt.plot(x, y, color='black', alpha=alpha, linewidth=linewidth)

    # Update plot aesthetics
    plt.axis('off')
    plt.axis('equal')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    plt.savefig(output_file, dpi = 600)
