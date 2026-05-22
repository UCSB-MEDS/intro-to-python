##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##                                    setup                                 ----
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#..........................load packages.........................
import pandas as pd
from plotnine import *

#..........................import data...........................
drought = pd.read_csv("data/drought.csv")

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##                            wrangle drought data                          ----
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

drought_clean = (
    drought
    .melt(id_vars=[c for c in drought.columns if c not in 
                   ["None", "D0", "D1", "D2", "D3", "D4"]],
          var_name="drought_lvl", value_name="area_pct")
    .rename(columns=str.lower)
    .rename(columns={"state_abbreviation": "state_abb", "valid_start": "date"})
    [["date", "state_abb", "drought_lvl", "area_pct"]]
    .assign(
        date=lambda df: pd.to_datetime(df["date"]),
        drought_lvl_long=lambda df: pd.Categorical(
            df["drought_lvl"].map({
                "D4": "D4 (Exceptional)",
                "D3": "D3 (Extreme)",
                "D2": "D2 (Severe)",
                "D1": "D1 (Moderate)",
                "D0": "D0 (Abnormally Dry)",
                "None": "No Drought"
            }),
            categories=["D4 (Exceptional)", "D3 (Extreme)", "D2 (Severe)",
                        "D1 (Moderate)", "D0 (Abnormally Dry)", "No Drought"],
            ordered=True
        )
    )
)

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##       create stacked area plot of CA drought conditions through time     ----
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

plot_data = drought_clean[
    (drought_clean["drought_lvl"] != "None") &
    (drought_clean["state_abb"] == "CA")
]

(
    ggplot(plot_data, aes(x="date", y="area_pct", fill="drought_lvl_long"))
    + geom_area(position=position_stack(reverse=True))
    + scale_fill_manual(values=["#853904", "#FF0000", "#FFC100", "#FFD965", "#FFFF00"])
    + scale_x_datetime(
        breaks=date_breaks("2 years"),
        limits=(pd.Timestamp("2000-01-01"), pd.Timestamp("2026-12-31")),
        labels=date_format("%Y"),
        expand=(0, 0)
    )
    + scale_y_continuous(
        breaks=range(0, 101, 10),
        expand=(0, 0),
        labels=lambda lst: [f"{v}%" for v in lst]
    )
    + labs(title="Drought area in California")
    + theme_minimal()
    + theme(
        axis_line=element_line(color="#5A9CD6"),
        axis_ticks=element_line(color="#5A9CD6"),
        axis_ticks_length=0.2,
        plot_title=element_text(ha="center", color="#686868", size=20,
                                margin={"t": 10, "b": 15}),
        axis_title=element_blank(),
        legend_title=element_blank(),
        axis_text=element_text(color="#686868", size=10),
        legend_text=element_text(color="#686868", size=10),
        legend_position="bottom",
        legend_direction="horizontal",
        legend_key_width=0.4,
        legend_key_height=0.25,
        plot_background=element_rect(color="#686868"),
        plot_margin=0.1
    )
)