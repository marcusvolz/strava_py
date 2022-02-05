import argparse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("path", help="Input path to folder with GPX and / or FIT files")
    parser.add_argument(
        "-o", "--output_file", default="plot.png", help="Output PNG file"
    )
    args = parser.parse_args()

    # Normally imports go at the top, but scientific libraries can be slow to import
    # so let's validate arguments first
    from strava_py.plot_facets import plot_facets
    from strava_py.process_data import process_data

    print("Processing data...")
    df = process_data(args.path)

    print("Plotting facets...")
    plot_facets(df, output_file=args.output_file)
    print(f"Saved to {args.output_file}")


if __name__ == "__main__":
    main()
