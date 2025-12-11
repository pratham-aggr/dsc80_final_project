## Predicting the Severity of Major Power Outages in the U.S.

## Introduction
Power outages disrupt millions of lives, which raises pressing issues like public safety and emergence response to economic stability. A power outage may seem like a simple inconvenience, like losing the chance to finish a show on Netflix, but its real impact goes far beyond that. In severe situations a power outage can  disable critical medical equipment, shut down heating or cooling during extreme weather, interrupt communication systems used by first responders, halt transportation services, and cause widespread economic losses for businesses and communities. Some of the major columns for the data and their description is shown below, for description about other columns please visit [here]('https://www.sciencedirect.com/science/article/pii/S2352340918307182'). 

<center>
    
| Column                                  | Description |
|-----------------------------------------|-------------|
| **dur_hours**                           | Duration of the power outage in hours (calculated from outage start and restoration times). |
| **customers.affected**                  | Number of customers impacted by the outage event. |
| **demand.loss.mw (megawatt)**           | Amount of electricity demand lost (in megawatts) during the outage. |
| **population**                          | Population of the state where the outage occurred. |
| **poppct_urban (%)**                    | Percent of the state population living in urban areas. |
| **res.price (cents/kWh)**               | Residential electricity price in cents per kilowatt-hour. |
| **pc.realgsp.state (usd)**              | Per-capita real gross state product (an economic indicator) in US dollars. |
</center>

Summary statistics of some variables which intuitively contribute most to the power outage are shown below. Note: `dur_hours` is calculate by taking in the difference between `outage_restore` and `outage_start`.

<center>

|       | dur_hours | customers.affected | demand.loss.mw (megawatt) | population | poppct_urban (%) | res.price (cents/kWh) | pc.realgsp.state (usd) |
|-------|-----------:|-------------------:|---------------------------:|------------:|------------------:|------------------------:|-------------------------:|
| count | 1476       | 1056               | 804                        | 1476        | 1476             | 1464                   | 1476                    |
| mean  | 43.7546    | 144117             | 543.399                    | 1.31474e+07 | 80.9457          | 11.971                 | 49387.5                 |
| std   | 99.0654    | 288110             | 2226.49                    | 1.14772e+07 | 11.8922          | 3.09008                | 11828                   |
| min   | 0          | 0                  | 0                          | 559851      | 38.66            | 5.65                   | 31111                   |
| 25%   | 1.70417    | 9700               | 4                          | 5.3109e+06  | 74.57            | 9.5775                 | 43056                   |
| 50%   | 11.6833    | 71661.5            | 175.5                      | 8.82341e+06 | 84.05            | 11.5                   | 48323                   |
| 75%   | 48         | 150000             | 400                        | 1.94029e+07 | 89.81            | 13.85                  | 53622                   |
| max   | 1811.88    | 3.24144e+06        | 41788                      | 3.92965e+07 | 100              | 34.58                  | 168377                  |

</center>

To better understand these events, this project uses the [Major Power Outage Events]('https://www.sciencedirect.com/science/article/pii/S2352340918307182') dataset which records **1,535** power outages occurring in the United States. Each outage has around **57** columns of information. This wide range of information makes us wonder about the severity of the power outages. Hence this project will explore the central question: **What factors influence how long a major power outage lasts, and can we predict outage duration using the available data?** This prediction problem will be useful for policymakers and the general community to according plan for the outage according to its severity. This will help them to allocate resources, and prepare for emergency needs.


## Data Cleaning and Exploratory Data Analysis
<iframe
  src="assets/univariate_analysis_cause.category.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<iframe
  src="assets/univariate_analysis_climate.region.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<iframe
  src="assets/bivariate_analysis_cause.category_vs_dur_hours_box_plot.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

<iframe
  src="assets/map.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

## Assessment of Missingness
Based on the dataset the column which is most likely to be **NMAR** (Not Missing at Random) is
`demand.loss (megawatt)` During large severe outages, reporting systems are often deprioritized which increases the likelihood that the larger (unobserved) values of outages are missing. This further means that missing may be directly related to the variable itself (the definition of NMAR).
To frame it as **MAR** (Missing at Random) further information on why the values are missing would be needed. This additional information could be wind speed, precipitation, some disaster report or reporting system failure is needed. If these factors can convey some correlation with the missingness in demand.loss (megawatt) then MAR can be justified. 

## Hypothesis Testing
<iframe
  src="assets/kde_is_normal_climate_True_False_dur_hours.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

## Framing a Prediction Problem

## Baseline Model

## Final Model

## Fairness Analysis
