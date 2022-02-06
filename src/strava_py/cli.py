import argparse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("path", help="Input path to folder with GPX and / or FIT files")
    parser.add_argument(
        "-o", "--output_file", default="plot.png", help="Output PNG file"
    )
    parser.add_argument("lon_min", default=None, help="Minimum longitude for plot_map (values less than this are removed from the data)")
    parser.add_argument("lon_max", default=None, help="Maximum longitude for plot_map (values greater than this are removed from the data)")
    parser.add_argument("lat_min", default=None, help="Minimum latitude for plot_map (values less than this are removed from the data)")
    parser.add_argument("lat_max", default=None, help="Maximum latitude for plot_map (values greater than this are removed from the data)")
    parser.add_argument("alpha", default=0.4, help="Line transparency. 0 = Fully transparent, 1 = No transparency")
    parser.add_argument("linewidth", default=0.4, help="Line width")
    args = parser.parse_args()

    # Normally imports go at the top, but scientific libraries can be slow to import
    # so let's validate arguments first
    from strava_py.plot_map import plot_map
    from strava_py.plot_facets import plot_facets
    from strava_py.process_data import process_data

    print("Processing data...")
    df = process_data(args.path)

    print("Plotting facets...")
    plot_facets(df, output_file=args.output_file)
    print(f"Saved to {args.output_file}")

    print("Plotting map...")
    plot_facets(df, output_file=args.output_file)
    print(f"Saved to {args.output_file}")


if __name__ == "__main__":
    main()
