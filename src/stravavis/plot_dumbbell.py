from __future__ import annotations

import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_rect,
    facet_grid,
    geom_point,
    geom_segment,
    ggplot,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_bw,
    xlab,
    ylab,
)


def plot_dumbbell(
    activities,
    year_min=None,
    year_max=None,
    local_timezone=None,
    fig_height=34,
    fig_width=34,
    output_file="dumbbell.png",
):
    # Convert activity start date to datetime
    activities = activities.assign(
        **{"Activity Date": pd.to_datetime(activities["Activity Date"], format="mixed")}
    )

    # Convert to local timezone (if given)
    if local_timezone:
        activities = activities.assign(
            **{
                "Activity Date": (
                    activities["Activity Date"]
                    .dt.tz_localize(tz="UTC", nonexistent="NaT", ambiguous="NaT")
                    .dt.tz_convert(local_timezone)
                )
            }
        )

    # Get activity start and end times
    activities = activities.assign(
        start=activities["Activity Date"],
        duration=pd.to_timedelta(activities["Elapsed Time"], unit="s"),
    )
    activities = activities.assign(
        end=pd.to_datetime(activities["start"] + activities["duration"]),
        year=activities["Activity Date"].dt.year,
    )

    if year_min:
        activities = activities[activities["year"] >= year_min].copy()

    if year_max:
        activities = activities[activities["year"] <= year_max].copy()

    # Get day of year and time of day data
    activities = activities.assign(
        dayofyear=activities["Activity Date"].dt.dayofyear,
        start_time=activities["start"].dt.time,
        end_time=activities["end"].dt.time,
        x=(
            activities["start"].dt.hour
            + activities["start"].dt.minute / 60
            + activities["start"].dt.second / 60 / 60
        ),
        xend=(
            activities["end"].dt.hour
            + activities["end"].dt.minute / 60
            + activities["end"].dt.second / 60 / 60
        ),
    )

    # Create plotnine / ggplot
    p = (
        ggplot(activities)
        + geom_segment(
            aes(x="x", y="dayofyear", xend="xend", yend="dayofyear"), size=0.1
        )
        + geom_point(aes("x", "dayofyear"), size=0.05)
        + geom_point(aes("xend", "dayofyear"), size=0.05)
        + facet_grid(".~year")
        + scale_x_continuous(
            breaks=[0, 6, 12, 18, 24], labels=["12am", "6am", "12pm", "6pm", ""]
        )
        + scale_y_continuous(breaks=[1, 100, 200, 300, 365])
        + xlab("Time of Day")
        + ylab("Day of Year")
        + theme_bw()
        + theme(
            plot_background=element_rect(fill="white"),
            panel_grid_major_y=element_blank(),
        )
    )

    # Save plot
    p.save(output_file, width=fig_width, height=fig_height, units="cm", dpi=600)
