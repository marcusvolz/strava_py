from __future__ import annotations

import argparse
import glob
import os.path
import sys

VISUALISATIONS = {
    "all",
    "calendar",
    "dumbbell",
    "elevations",
    "facets",
    "landscape",
    "map",
}


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "path", help="Input path specification to folder with GPX and / or FIT files"
    )
    parser.add_argument(
        "--plot",
        default="all",
        choices=VISUALISATIONS,
        nargs="+",
        help="Which visualisations to plot",
    )
    parser.add_argument(
        "-o", "--output_prefix", default="strava", help="Prefix for output PNG files"
    )
    parser.add_argument(
        "--lon_min",
        type=float,
        help="Minimum longitude for plot_map "
        "(values less than this are removed from the data)",
    )
    parser.add_argument(
        "--lon_max",
        type=float,
        help="Maximum longitude for plot_map "
        "(values greater than this are removed from the data)",
    )
    parser.add_argument(
        "--lat_min",
        type=float,
        help="Minimum latitude for plot_map "
        "(values less than this are removed from the data)",
    )
    parser.add_argument(
        "--lat_max",
        type=float,
        help="Maximum latitude for plot_map "
        "(values greater than this are removed from the data)",
    )
    parser.add_argument(
        "--bbox", help="Shortcut for comma-separated LON_MIN,LAT_MIN,LON_MAX,LAT_MAX"
    )
    parser.add_argument(
        "--alpha",
        default=0.4,
        help="Line transparency. 0 = Fully transparent, 1 = No transparency",
    )
    parser.add_argument("--linewidth", default=0.4, help="Line width")
    parser.add_argument(
        "--activities_path", help="Path to activities.csv from Strava bulk export zip"
    )
    parser.add_argument(
        "--year_min",
        type=int,
        help="The minimum year to use for the calendar heatmap and dumbbell.",
    )
    parser.add_argument(
        "--year_max",
        type=int,
        help="The maximum year to use for the calendar heatmap and dumbbell.",
    )
    parser.add_argument(
        "--max_dist",
        type=float,
        help="Maximum daily distance for the calendar heatmap; "
        "values above this will be capped.",
    )
    parser.add_argument(
        "--fig_height",
        type=float,
        help="Figure height for the calendar heatmap and dumbbell.",
    )
    parser.add_argument(
        "--fig_width",
        type=float,
        help="Figure width for the calendar heatmap and dumbbell.",
    )
    parser.add_argument(
        "--local_timezone",
        help="Timezone for determining local times for activities. "
        "See pytz.all_timezones for a list of all timezones.",
    )
    args = parser.parse_args()

    if "all" in args.plot:
        args.plot = VISUALISATIONS

    # Expand "~" or "~user"
    args.path = os.path.expanduser(args.path)

    if os.path.isdir(args.path):
        args.path = os.path.join(args.path, "*")

    filenames = sorted(glob.glob(args.path))
    if not filenames:
        sys.exit(f"No files found matching {args.path}")

    if args.bbox:
        try:
            bbox_values = args.bbox.split(",")
            if len(bbox_values) == 1:
                with open(args.bbox) as f:
                    bbox_values = f.readline().split(",")
            args.lon_min, args.lat_min, args.lon_max, args.lat_max = map(
                float, bbox_values
            )
        except ValueError:
            sys.exit(
                f"Bounding box '{args.bbox}' must be four comma-separated coordinates "
                "or a file containing them"
            )

    if args.activities_path and os.path.isdir(args.activities_path):
        args.activities_path = os.path.join(args.activities_path, "activities.csv")

    # Normally imports go at the top, but scientific libraries can be slow to import
    # so let's validate arguments first
    from .process_data import process_data

    print("Processing data...")
    df = process_data(filenames)
    if df.empty:
        sys.exit("No data to plot")

    activities = None
    if args.activities_path:
        from .process_activities import process_activities

        print("Processing activities...")
        activities = process_activities(args.activities_path)

    if "facets" in args.plot:
        from .plot_facets import plot_facets

        print("Plotting facets...")
        outfile = f"{args.output_prefix}-facets.png"
        plot_facets(df, output_file=outfile)
        print(f"Saved to {outfile}")

    if "map" in args.plot:
        from .plot_map import plot_map

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

    if "elevations" in args.plot:
        from .plot_elevations import plot_elevations

        print("Plotting elevations...")
        outfile = f"{args.output_prefix}-elevations.png"
        plot_elevations(df, output_file=outfile)
        print(f"Saved to {outfile}")

    if "landscape" in args.plot:
        from .plot_landscape import plot_landscape

        print("Plotting landscape...")
        outfile = f"{args.output_prefix}-landscape.png"
        plot_landscape(df, output_file=outfile)
        print(f"Saved to {outfile}")

    if activities is not None:
        if "calendar" in args.plot:
            from .plot_calendar import plot_calendar

            print("Plotting calendar...")
            outfile = f"{args.output_prefix}-calendar.png"
            fig_height = args.fig_height or 15
            fig_width = args.fig_width or 9
            plot_calendar(
                activities,
                args.year_min,
                args.year_max,
                args.max_dist,
                fig_height,
                fig_width,
                outfile,
            )
            print(f"Saved to {outfile}")

        if "dumbbell" in args.plot:
            from .plot_dumbbell import plot_dumbbell

            print("Plotting dumbbell...")
            outfile = f"{args.output_prefix}-dumbbell.png"
            fig_height = args.fig_height or 34
            fig_width = args.fig_width or 34
            plot_dumbbell(
                activities,
                args.year_min,
                args.year_max,
                args.local_timezone,
                fig_height,
                fig_width,
                outfile,
            )
            print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
