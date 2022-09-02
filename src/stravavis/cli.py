import argparse
import os.path


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "path", help="Input path specification to folder with GPX and / or FIT files"
    )
    parser.add_argument(
        "-o", "--output_prefix", default="strava", help="Prefix for output PNG files"
    )
    parser.add_argument(
        "--lon_min",
        type=float,
        help="Minimum longitude for plot_map (values less than this are removed from the data)",
    )
    parser.add_argument(
        "--lon_max",
        type=float,
        help="Maximum longitude for plot_map (values greater than this are removed from the data)",
    )
    parser.add_argument(
        "--lat_min",
        type=float,
        help="Minimum latitude for plot_map (values less than this are removed from the data)",
    )
    parser.add_argument(
        "--lat_max",
        type=float,
        help="Maximum latitude for plot_map (values greater than this are removed from the data)",
    )
    parser.add_argument(
        "--bbox", help="Shortcut for comma-separated LON_MIN,LAT_MIN,LON_MAX,LAT_MAX"
    )
    parser.add_argument("--alpha", default=0.4, help="Line transparency. 0 = Fully transparent, 1 = No transparency")
    parser.add_argument("--linewidth", default=0.4, help="Line width")
    parser.add_argument("--activities_path", help="Path to activities.csv from Strava bulk export zip")
    parser.add_argument("--year_min", help="The minimum year to use for the calendar heatmap.")
    parser.add_argument("--year_max", help="The maximum year to use for the calendar heatmap.")
    parser.add_argument("--max_dist", help="Maximum daily distance for the calendar heatmap; values above this will be capped.")
    parser.add_argument("--fig_height", help="Figure height for the calendar heatmap.")
    parser.add_argument("--fig_width", help="Figure width for the calendar heatmap.")
    parser.add_argument("--local_timezone", help="Timezone for determining local times for activities. See pytz.all_timezones for a list of all timezones.")
    args = parser.parse_args()

    # Expand "~" or "~user"
    args.path = os.path.expanduser(args.path)

    if os.path.isdir(args.path):
        args.path = os.path.join(args.path, "*")

    if args.bbox:
        # Convert comma-separated string into floats
        args.lon_min, args.lat_min, args.lon_max, args.lat_max = (
            float(x) for x in args.bbox.split(",")
        )

    if args.activities_path and os.path.isdir(args.activities_path):
        args.activities_path = os.path.join(args.activities_path, "activities.csv")

    # Normally imports go at the top, but scientific libraries can be slow to import
    # so let's validate arguments first
    from stravavis.plot_calendar import plot_calendar
    from stravavis.plot_dumbbell import plot_dumbbell
    from stravavis.plot_elevations import plot_elevations
    from stravavis.plot_facets import plot_facets
    from stravavis.plot_landscape import plot_landscape
    from stravavis.plot_map import plot_map
    from stravavis.process_activities import process_activities
    from stravavis.process_data import process_data

    print("Processing data...")
    df = process_data(args.path)

    activities = None
    if args.activities_path:
        print("Processing activities...")
        activities = process_activities(args.activities_path)

    print("Plotting facets...")
    outfile = f"{args.output_prefix}-facets.png"
    plot_facets(df, output_file=outfile)
    print(f"Saved to {outfile}")

    print("Plotting map...")
    outfile = f"{args.output_prefix}-map.png"
    plot_map(
        df,
        args.lon_min,
        args.lon_max,
        args.lat_min,
        args.lat_max,
        args.alpha,
        args.linewidth,
        outfile,
    )
    print(f"Saved to {outfile}")

    print("Plotting elevations...")
    outfile = f"{args.output_prefix}-elevations.png"
    plot_elevations(df, output_file=outfile)
    print(f"Saved to {outfile}")

    print("Plotting landscape...")
    outfile = f"{args.output_prefix}-landscape.png"
    plot_landscape(df, output_file=outfile)
    print(f"Saved to {outfile}")

    if activities is not None:
        print("Plotting calendar...")
        outfile = f"{args.output_prefix}-calendar.png"
        plot_calendar(activities, output_file=outfile)
        print(f"Saved to {outfile}")
    
        print("Plotting dumbbell...")
        outfile = f"{args.output_prefix}-dumbbell.png"
        plot_dumbbell(activities, output_file=outfile)
        print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
