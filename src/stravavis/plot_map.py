import matplotlib.pyplot as plt

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
    n = len(activities)

    # Plot activities one by one
    for i in range(n):
        X = df[df['name'] == activities[i]]['lon']
        Y = df[df['name'] == activities[i]]['lat']
        plt.plot(X, Y, color = 'black', alpha = alpha, linewidth = linewidth)

    # Update plot aesthetics
    plt.axis('off')
    plt.axis('equal')
    plt.margins(0)
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
    plt.savefig(output_file, dpi = 600)
