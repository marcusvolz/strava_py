import math
import matplotlib.pyplot as plt
import seaborn as sns

def plot_facets(df, output_file = 'plot.png'):

    # Create a new figure
    plt.figure()

    # Compute activity start times (for facet ordering)
    start_times = df.groupby('name').agg({'time': 'min'}).reset_index().sort_values('time')
    ncol = math.ceil(math.sqrt(len(start_times)))
    
    # Create facets
    p = sns.FacetGrid(
        data = df,
        col = 'name',
        col_wrap = ncol,
        col_order = start_times['name'],
        sharex = False,
        sharey = False,
        )

    def eplt(x, y, **kws):
        ax = plt.gca()
        ax.plot(x, y, **kws)
        ax.set_aspect('equal', adjustable='box')

    # Add activities
    p = p.map(
        eplt, "lon", "lat", color = 'black', linewidth = 4
        )

    # Update plot aesthetics
    p.set(xlabel = None)
    p.set(ylabel = None)
    p.set(xticks = [])
    p.set(yticks = [])
    p.set(xticklabels = [])
    p.set(yticklabels = [])
    p.set_titles(col_template = '', row_template = '')
    sns.despine(left = True, bottom = True)
    plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95)
    plt.savefig(output_file)
