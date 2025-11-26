# strava_py

Create artistic visualisations with your exercise data (Python version).

This is a port of the [R strava package](https://github.com/marcusvolz/strava) to
Python.

## Installation

Install via pip:

```sh
python3 -m pip install stravavis
```

For development:

```sh
git clone https://github.com/marcusvolz/strava_py
cd strava_py
pip install -e .
```

Then run from the terminal:

```sh
stravavis --help
```

## How to use

If your activity data is in a folder called `activities`, run the following command:

```sh
stravavis activities
```

By default, this will create output images prefixed `strava-`.

If you have an `activities.csv` file:

```sh
stravavis activities --activities_path activities.csv
```

To only map activities contained within a
[bounding box](https://boundingbox.klokantech.com/):

```sh
stravavis activities --bbox 24.782802,59.922486,25.254511,60.29785
```

Or as a shortcut, save bounding-box coordinates to a file:

```sh
echo 24.782802,59.922486,25.254511,60.29785 > helsinki.bbox
stravavis activities --bbox helsinki.bbox
```

To only plot certain visualisations:

```sh
stravavis activities --plot map facets landscape
```

## Examples

### Facets

A plot of activities as small multiples. The concept behind this plot was originally
inspired by [Sisu](https://twitter.com/madewithsisu).

![facets](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/facets001.png "Facets, showing activity outlines")

### Map

A map of activities viewed in plan.

![map](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/map001.png "A map of activities viewed in plan")

### Elevations

A plot of activity elevation profiles as small multiples.

![map](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/elevations001.png "A plot of activity elevation profiles as small multiples")

### Landscape

Elevation profiles superimposed.

![map](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/landscape001.png "Elevation profiles superimposed")

### Calendar

Calendar heatmap showing daily activity distance, using the
[calmap](https://pythonhosted.org/calmap/) package. Requires "activities.csv" from the
bulk Strava export.

![map](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/calendar001.png "Calendar heatmap")

### Dumbbell plot

Activities shown as horizontal lines by time of day and day of year, facetted by year.
Requires "activities.csv" from the bulk Strava export.

![map](https://raw.githubusercontent.com/marcusvolz/strava_py/main/plots/dumbbell001.png "Dumbbell plot")

## Bulk export from Strava

The process for downloading data is described on the Strava website here:
[https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk],
but in essence, do the following:

1. Log in to [Strava](https://www.strava.com/)
2. Select "[Settings](https://www.strava.com/settings/profile)" from the main drop-down
   menu at top right of the screen
3. Select "[My Account](https://www.strava.com/account)" from the navigation menu to the
   left of the screen.
4. Under the
   "[Download or Delete Your Account](https://www.strava.com/athlete/delete_your_account)"
   heading, click the "Get Started" button.
5. Under the "Download Request", heading, click the "Request Your Archive" button.
   **_Don't click anything else on that page, i.e. particularly not the "Request Account
   Deletion" button._**
6. Wait for an email to be sent
7. Click the link in email to download zipped folder containing activities
8. Unzip files

## Programmatic use

The package can also be used programmatically. The following code snippets demonstrate
how to use the package to create the visualisations.

The main function for importing and processing activity files expects a path to a
directory of unzipped GPX and / or FIT files. If required, the
[fit2gpx](https://github.com/dodo-saba/fit2gpx) package provides useful tools for
pre-processing bulk files exported from Strava, e.g. unzipping activity files (see Use
Case 3: Strava Bulk Export Tools).

```python
df = process_data("<path to folder with GPX and / or FIT files>")
```

Some plots use the "activities.csv" file from the Strava bulk export zip. For those
plots, create an "activities" dataframe using the following function:

```python
activities = process_activities("<path to activities.csv file>")
```

### Plot activities as small multiples

```python
plot_facets(df, output_file = 'plot.png')
```

### Plot activity map

```python
plot_map(df, lon_min=None, lon_max= None, lat_min=None, lat_max=None,
             alpha=0.3, linewidth=0.3, output_file="map.png")
```

### Plot elevations

```python
plot_elevations(df, output_file = 'elevations.png')
```

### Plot landscape

```python
plot_landscape(df, output_file = 'landscape.png')
```

### Plot calendar

```python
plot_calendar(activities, year_min=2015, year_max=2017, max_dist=50,
              fig_height=9, fig_width=15, output_file="calendar.png")
```

### Plot dumbbell

```python
plot_dumbbell(activities, year_min=2012, year_max=2015, local_timezone='Australia/Melbourne',
              fig_height=34, fig_width=34, output_file="dumbbell.png")
```
