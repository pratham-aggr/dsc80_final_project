## Predicting the Severity of Major Power Outages in the U.S.
**Analysis by Pratham Aggarwal**

## Introduction
Power outages disrupt millions of lives, which raises pressing issues like public safety and emergency response to economic stability. A power outage may seem like a simple inconvenience—like losing the chance to finish a show on Netflix—but its real impact goes far beyond that. In severe situations, a power outage can disable critical medical equipment, shut down heating or cooling during extreme weather, interrupt communication systems used by first responders, halt transportation services, and cause widespread economic losses for businesses and communities.

Some of the major columns for the data and their descriptions are shown below. For descriptions of all other columns, please visit [here](https://www.sciencedirect.com/science/article/pii/S2352340918307182).

| Column                                  | Description |
|-----------------------------------------|-------------|
| **dur_hours**                           | Duration of the power outage in hours (calculated from outage start and restoration times). |
| **customers.affected**                  | Number of customers impacted by the outage event. |
| **demand.loss.mw (megawatt)**           | Amount of electricity demand lost (in megawatts) during the outage. |
| **population**                          | Population of the state where the outage occurred. |
| **poppct_urban (%)**                    | Percent of the state population living in urban areas. |
| **res.price (cents/kWh)**               | Residential electricity price in cents per kilowatt-hour. |
| **pc.realgsp.state (usd)**              | Per-capita real gross state product (an economic indicator) in US dollars. |

Summary statistics of some variables that intuitively contribute most to the power outage are shown below.  
**Note:** `dur_hours` is calculated by taking the difference between `outage_restore` and `outage_start`.

|       | dur_hours | customers.affected | demand.loss.mw (megawatt) | population | poppct_urban (%) | res.price (cents/kWh) | pc.realgsp.state (usd) |
|-------|-----------|-------------------|---------------------------|------------|------------------|------------------------|-------------------------|
| count | 1476       | 1056               | 804                        | 1476        | 1476             | 1464                   | 1476                    |
| mean  | 43.7546    | 144117             | 543.399                    | 1.31474e+07 | 80.9457          | 11.971                 | 49387.5                 |
| std   | 99.0654    | 288110             | 2226.49                    | 1.14772e+07 | 11.8922          | 3.09008                | 11828                   |
| min   | 0          | 0                  | 0                          | 559851      | 38.66            | 5.65                   | 31111                   |
| 25%   | 1.70417    | 9700               | 4                          | 5.3109e+06  | 74.57            | 9.5775                 | 43056                   |
| 50%   | 11.6833    | 71661.5            | 175.5                      | 8.82341e+06 | 84.05            | 11.5                   | 48323                   |
| 75%   | 48         | 150000             | 400                        | 1.94029e+07 | 89.81            | 13.85                  | 53622                   |
| max   | 1811.88    | 3.24144e+06        | 41788                      | 3.92965e+07 | 100              | 34.58                  | 168377                  |

To better understand these events, this project uses the [Major Power Outage Events](https://www.sciencedirect.com/science/article/pii/S2352340918307182) dataset, which records **1,535** power outages in the United States. Each outage has around **57** columns of information. This wide range of information motivates the central question of this project:  
**What factors influence how long a major power outage lasts, and can we predict outage duration using the available data?**

Understanding and predicting outage duration can help policymakers and the general public prepare for emergency needs, allocate resources effectively, and plan according to outage severity.

## Data Cleaning and Exploratory Data Analysis
To prepare the data for analysis several cleaning steps were taken to clean and standardize the data. First goal was to convert units properly, fix columns names, handel how date and time are stored and remove redundant information in the dataset. Since data was in `.xlxs` format it was converted to `.csv` using google sheets. Then we created a deep copy of the data to preserve the orginal raw information. First five rows were deleted because they contained some metadata, which was disrupting tabular data expectations for our analysis. Since units are crucial to this analysis, we drop the unit column and merge it with the header following the format: `<col_name> (<unit>)` (provided the units exist for the columns). Column names were converted into lowercase letters for convenience To keep our analysis handy we divided the variables into three major categories: categorical, numeric and datetime variables. All numeric variable were converted to float to avoid typecasting issues during model preperation. Moreover datetime variables like month, year, time were conveted to pandas datetime format using `pd.to_datetime()`. Therefore all datetime variables were merged into two unique columns called `outage_start` and `outage_restore`.Target variable (`dur_hours`) was prepared by taking the difference between `outage_restore` and `outage_start` further dividing by 3600 to convert into hours. 

`hurricane.names` is not useful information for our analysis hence we drop that columns. Since other columns like `cause.category` and `cause.category.detail` tell us why outage happened, dropping `hurricane.names` won't affect our model performance. `obs` was just an index columns hence we dropped it as well. `variable (units)` was dropped since we merged this information with columns headers. `postal.codes` was just US state names written in abbreviation, so we drop it.  
<iframe
  src="assets/imputation.png"
  width="300"
  height="400"
  frameborder="0"
></iframe>
Missing values in the dataset were imputated using the preprocessing pipeline shown above. Numerical features like (`anomaly.level (numeric)`,`demand.loss.mw (megawatt)`,`customers.affected`) were passed through `sklearn.SimpleImputer` that replaced `NaNs` with median for each columns. We particularly replaced with median, because while doing Exploratory Data Analysis majority columns showed skewed towards right behavior, therefore median imputation became a better choice than mean imputation as median are less sensitive to outliers than mean. Later, the numerical varaibles are passed through `StandardScaler`data into z-score. This is an important step as this will ensure that higher values of one feature would not dominate the ones with numerical lower value, ensuring a consistent analysis. Similarly categorical features were passed through `sklearn.SimpleImputer' that replaced `NaNs` with the most frequent category. Later OrdinalEncoding was performed on categorical variables, essentially converting these categories into numbers (Example: `['Low','Medium','High'] ->  [0,1,2]`. Note: Alternative imputation methods, including probabilistic and random sampling approaches, were explored. However, these techniques tended to inject noise and reduce predictive stability, so they were not used in the final preprocessing pipeline.


### Univariate Analysis 
<!-- <iframe
  src="assets/univariate_analysis_cause.category.html"
  width="800"
  height="600"
  frameborder="0"
></iframe> -->
The below choropleth map shows the average duration of power outages in hours by U.S states. Darker regions indicate longer periods of power outage while lighter ones indicate on regions which recover power quicker than darker ones. The map shows diverse avergae otage durations across US states. The states in Northeast and Midwest tend to have higher and persistent power outages whereas Southern and Western states on average show shorter power outage durations. This observation is driven by various factors like climate exposure, infrastructure of the states, population density and other confounding variables not found in the dataset. 
<iframe
  src="assets/map.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

### Bivariate Analysis 
<!-- <iframe
  src="assets/univariate_analysis_climate.region.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>
 -->
The boxplot below compares outage duration across different cause.categories, which explains us about how severity of power outage when depending on severity of the cause. Severe weather and fuel supply emergencies tend to produce longest an most variable outages, having many outliers. In contrast the intentional attacks and islanding generally shows lower outage duration. This analysis shows that cause of an outage plays an important role in determining how long the outage would last, hence making it an important feature to include. 
<iframe
  src="assets/bivariate_analysis_cause.category_vs_dur_hours_box_plot.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

### Interesting Aggregates

| urban_bin | count | mean  | median |
|-----------|-------|-------|--------|
| Very Low  | 296   | 41.36 | 9.43   |
| Low       | 319   | 59.55 | 35.00  |
| Medium    | 276   | 29.53 | 6.32   |
| High      | 315   | 51.39 | 12.00  |
| Very High | 270   | 33.36 | 5.74   |

The aggregation tables paints a good picture of how outage severity varies across different levels of urbanizaton, which reveals some important patterns. States with lower urabanization experience longer periods of power outage. This supports our general understanding, since less urabanized places have inadequate infrastructure and limited urgency of restoration. On the contrary urabanized places, though have frequent outages, however they restore back quicker than lower urabanized places. This gives us a solid context on how urbanization influences power outage durations. 

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
