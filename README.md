# strava_py
Create artistic visualisations with your exercise data (Python version).

This is a port of the [R strava package](https://github.com/marcusvolz/strava) to Python.

## Examples

### Facets

A plot of activities as small multiples. The concept behind this plot was originally inspired by [Sisu](https://twitter.com/madewithsisu).

![facets](https://github.com/marcusvolz/strava_py/blob/main/plots/facets001.png "Facets, showing activity outlines")

### Map

A map of activities viewed in plan.

![map](https://github.com/marcusvolz/strava_py/blob/main/plots/map001.png "A map of activities viewed in plan.")

### Elevations

A plot of activity elevation profiles as small multiples.

![map](https://github.com/marcusvolz/strava_py/blob/main/plots/elevations001.png "A plot of activity elevation profiles as small multiples.")

## How to use

### Bulk export from Strava
The process for downloading data is described on the Strava website here: [https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk], but in essence, do the following:
                                                                           
1. Log in to [Strava](https://www.strava.com/)
2. Select "[Settings](https://www.strava.com/settings/profile)" from the main drop-down menu at top right of the screen
3. Select "[My Account](https://www.strava.com/account)" from the navigation menu to the left of the screen.
4. Under the "[Download or Delete Your Account](https://www.strava.com/athlete/delete_your_account)" heading, click the "Get Started" button.
5. Under the "Download Request", heading, click the "Request Your Archive" button. ***Don't click anything else on that page, i.e. particularly not the "Request Account Deletion" button.***
6. Wait for an email to be sent
7. Click the link in email to download zipped folder containing activities
8. Unzip files

### Process the data

The main function for importing and processing activity files expects a path to a directory of unzipped GPX and / or FIT files. If required, the [fit2gpx](https://github.com/dodo-saba/fit2gpx) package provides useful tools for pre-processing bulk files exported from Strava, e.g. unzipping activity files (see Use Case 3: Strava Bulk Export Tools).

```python
df = process_data(<path to folder with GPX and / or FIT files>)
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
plot_facets(df, output_file = 'elevations.png')
```
