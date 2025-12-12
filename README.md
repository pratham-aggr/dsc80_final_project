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
  width="600"
  height="300"
  frameborder="0"
></iframe>
Missing values in the dataset were imputated using the preprocessing pipeline shown above. Numerical features like (`anomaly.level (numeric)`,`demand.loss.mw (megawatt)`,`customers.affected`) were passed through `sklearn.SimpleImputer` that replaced `NaNs` with median for each columns. We particularly replaced with median, because while doing Exploratory Data Analysis majority columns showed skewed towards right behavior, therefore median imputation became a better choice than mean imputation as median are less sensitive to outliers than mean.Later, the numerical varaibles are passed through `StandardScaler`data into z-score. This is an important step as this will ensure that higher values of one feature would not dominate the ones with numerical lower value, ensuring a consistent analysis.  Similarly categorical features were passed through `sklearn.SimpleImputer` that replaced `NaNs` with the most frequent category. Later OneHotEncoding was performed on categorical variables, essentially converting these categories into numbers. Note: Alternative imputation methods, including probabilistic and random sampling approaches, were explored. However, these techniques tended to inject noise and reduce predictive stability, so they were not used in the final preprocessing pipeline.

first five rows of our cleaned dataset looks like below:

|    | u.s._state   | nerc.region   | climate.region     |   anomaly.level (numeric) | climate.category   | cause.category     |   demand.loss.mw (megawatt) |   customers.affected |   res.price (cents / kilowatt-hour) |   com.price (cents / kilowatt-hour) |   ind.price (cents / kilowatt-hour) |   total.price (cents / kilowatt-hour) |   res.sales (megawatt-hour) |   com.sales (megawatt-hour) |   ind.sales (megawatt-hour) |   total.sales (megawatt-hour) |   res.percen (%) |   com.percen (%) |   ind.percen (%) |   res.customers |   com.customers |   ind.customers |   total.customers |   res.cust.pct (%) |   com.cust.pct (%) |   ind.cust.pct (%) |   pc.realgsp.state (usd) |   pc.realgsp.usa (usd) |   pc.realgsp.rel (fraction) |   pc.realgsp.change (%) |   util.realgsp (usd) |   total.realgsp (usd) |   util.contri (%) |   pi.util.ofusa (%) |   population |   poppct_urban (%) |   poppct_uc (%) |   popden_urban (persons per square mile) |   popden_uc (persons per square mile) |   popden_rural (persons per square mile) |   areapct_urban (%) |   areapct_uc (%) |   pct_land (%) |   pct_water_tot (%) |   pct_water_inland (%) |   dur_hours | urban_bin   |
|---:|:-------------|:--------------|:-------------------|--------------------------:|:-------------------|:-------------------|----------------------------:|---------------------:|------------------------------------:|------------------------------------:|------------------------------------:|--------------------------------------:|----------------------------:|----------------------------:|----------------------------:|------------------------------:|-----------------:|-----------------:|-----------------:|----------------:|----------------:|----------------:|------------------:|-------------------:|-------------------:|-------------------:|-------------------------:|-----------------------:|----------------------------:|------------------------:|---------------------:|----------------------:|------------------:|--------------------:|-------------:|-------------------:|----------------:|-----------------------------------------:|--------------------------------------:|-----------------------------------------:|--------------------:|-----------------:|---------------:|--------------------:|-----------------------:|------------:|:------------|
|  0 | Minnesota    | MRO           | East North Central |                      -0.3 | normal             | severe weather     |                         nan |                70000 |                               11.6  |                                9.18 |                                6.81 |                                  9.28 |                 2.33292e+06 |                 2.11477e+06 |                 2.11329e+06 |                   6.56252e+06 |          35.5491 |          32.225  |          32.2024 |     2.30874e+06 |          276286 |           10673 |       2.5957e+06  |            88.9448 |            10.644  |             0.4112 |                    51268 |                  47586 |                     1.07738 |                     1.6 |                 4802 |                274182 |           1.75139 |                 2.2 |  5.34812e+06 |              73.27 |           15.28 |                                     2279 |                                1700.5 |                                     18.2 |                2.14 |              0.6 |        91.5927 |             8.40733 |                5.47874 |  51         | Low         |
|  1 | Minnesota    | MRO           | East North Central |                      -0.1 | normal             | intentional attack |                         nan |                  nan |                               12.12 |                                9.71 |                                6.49 |                                  9.28 |                 1.58699e+06 |                 1.80776e+06 |                 1.88793e+06 |                   5.28423e+06 |          30.0325 |          34.2104 |          35.7276 |     2.34586e+06 |          284978 |            9898 |       2.64074e+06 |            88.8335 |            10.7916 |             0.3748 |                    53499 |                  49091 |                     1.08979 |                     1.9 |                 5226 |                291955 |           1.79    |                 2.2 |  5.45712e+06 |              73.27 |           15.28 |                                     2279 |                                1700.5 |                                     18.2 |                2.14 |              0.6 |        91.5927 |             8.40733 |                5.47874 |   0.0166667 | Low         |
|  2 | Minnesota    | MRO           | East North Central |                      -1.5 | cold               | severe weather     |                         nan |                70000 |                               10.87 |                                8.19 |                                6.07 |                                  8.15 |                 1.46729e+06 |                 1.80168e+06 |                 1.9513e+06  |                   5.22212e+06 |          28.0977 |          34.501  |          37.366  |     2.30029e+06 |          276463 |           10150 |       2.5869e+06  |            88.9206 |            10.687  |             0.3924 |                    50447 |                  47287 |                     1.06683 |                     2.7 |                 4571 |                267895 |           1.70627 |                 2.1 |  5.3109e+06  |              73.27 |           15.28 |                                     2279 |                                1700.5 |                                     18.2 |                2.14 |              0.6 |        91.5927 |             8.40733 |                5.47874 |  50         | Low         |
|  3 | Minnesota    | MRO           | East North Central |                      -0.1 | normal             | severe weather     |                         nan |                68200 |                               11.79 |                                9.25 |                                6.71 |                                  9.19 |                 1.85152e+06 |                 1.94117e+06 |                 1.99303e+06 |                   5.78706e+06 |          31.9941 |          33.5433 |          34.4393 |     2.31734e+06 |          278466 |           11010 |       2.60681e+06 |            88.8954 |            10.6822 |             0.4224 |                    51598 |                  48156 |                     1.07148 |                     0.6 |                 5364 |                277627 |           1.93209 |                 2.2 |  5.38044e+06 |              73.27 |           15.28 |                                     2279 |                                1700.5 |                                     18.2 |                2.14 |              0.6 |        91.5927 |             8.40733 |                5.47874 |  42.5       | Low         |
|  4 | Minnesota    | MRO           | East North Central |                       1.2 | warm               | severe weather     |                         250 |               250000 |                               13.07 |                               10.16 |                                7.74 |                                 10.43 |                 2.02888e+06 |                 2.16161e+06 |                 1.77794e+06 |                   5.97034e+06 |          33.9826 |          36.2059 |          29.7795 |     2.37467e+06 |          289044 |            9812 |       2.67353e+06 |            88.8216 |            10.8113 |             0.367  |                    54431 |                  49844 |                     1.09203 |                     1.7 |                 4873 |                292023 |           1.6687  |                 2.2 |  5.48959e+06 |              73.27 |           15.28 |                                     2279 |                                1700.5 |                                     18.2 |                2.14 |              0.6 |        91.5927 |             8.40733 |                5.47874 |  29         | Low         |

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
  height="500"
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
We test the following two hypothesis to for assessment of missingness in our data.

**Missingness Hypothesis 1**: 
- **H0**: missingness in `anomaly.level` is independent of total water percentage (`pct_water_tot (%)`)
- **H1**: missingness in `anomaly.level` is dependent on total water percentage (`pct_water_tot (%)`)
- **TS**: Kolmogorov-Smirnov statistic, since KDE of both categroies is very similar mean/median would'nt suffice. 
- **Result**: Failed to reject H0 (**pval = 0.8247** , alpha = 0.05)
Missingness appears to be random with respect to water percentage. Our general expectation says that it should be dependent on climate variable like anomally.level, but the analysis says the otherwise signaling a weaker effect of water percentage.

<iframe
  src="assets/hyp_pct_water_tot (%).html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

**Missingness Hypothesis 2**: 
- **H0**: missingness in `anomaly.level` is independent of commercial electricity sales (`com.sales (megawatt-hour)`)
- **H1**: missingness in `anomaly.level` is dependent on commercial electricity sales (`com.sales (megawatt-hour)`)
- **TS**: Kolmogorov-Smirnov statistic, since KDE of both categroies is very similar mean/median would'nt suffice. 
- **Result**: Reject H0  (**pval = 0.0** , alpha = 0.05)
Missingness appears to be random with respect to utility contribution, which is opposite to our general expectations, since commercial electricity sales would not influence climate anomally level. This appears to be more of a correlational result instead of causal outcome. 

<iframe
  src="assets/hyp_com.sales (megawatt-hour).html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

## Hypothesis Testing
<!-- <iframe
  src="assets/kde_is_normal_climate_True_False_dur_hours.html"
  width="800"
  height="600"
  frameborder="0"
></iframe> -->
We will perform Permutation Testing to investigate the following: 
- **H0**: outage duration is independent of climate category (using the encoding True if `climate.category` is normal)
- **H1**: outage duration is dependent on climate category.
- **TS**: Kolmogorov-Smirnov statistic, since KDE of both categroies is very similar mean/median would'nt suffice. 
- **Result**: Failed to reject H0 (**pval = 0.0557** , alpha = 0.05)
Hence we have no statistical evidence that climate category influences outage duration (suprising result, but acceptable since power outages depend on weather more than climate). This result must not be taken very seriously, because it is very close to alpha, if we had more information (less nans) we may yeild opposite result. 

## Framing a Prediction Problem
The project will predict the **duration (hours)** of a major power outage, framing as a **regression problem** where target variable is `dur_hours`. Duration was chosen because outage duration is the most pressing factor when it comes to operationalizing the "severity" of a power outage as it has direct strong implications for emergency planning, resource allocation etc. To evaluate the model performance, we will be using the **Mean Absolute Error** as the primary metric. MAE is selected because it very easy to interpret and it is robust to outliers relative to metrics like Root Mean Squared Error (RMSE). By focussing on MAE, our model would be used as a better day to day tool to predict the severity of general outages. 

## Baseline Model
The baseline model we used is multiple **linear regression** to predict the severity of power outage, operationalized by duration of outage in hours. Linear Regression would be a simple starting point to understand regression limitations and need for feature engineering. It would be a great benchmark for later more complicated models. As a review we have: for baseline model we will include all the features to predict outage duration. Specifically, dataset contains **6 nominal features (state and region/category variables)**, **0 ordinal features**, and **46 quantitative features (including anomaly.level, all numeric measures, percentages, economic indicators, population stats, densities, and duration)**.

As in data cleaning section we reiterate the following, Numerical features like (`anomaly.level (numeric)`,`demand.loss.mw (megawatt)`,`customers.affected`) were passed through `sklearn.SimpleImputer` that replaced `NaNs` with median for each columns and then it was passed through `StandardScaler` to convert them into z-scores.  This is an important step as this will ensure that higher values of one feature would not dominate the ones with numerical lower value, ensuring a consistent analysis. Similarly categorical features were passed through `sklearn.SimpleImputer` that replaced `NaNs` with the most frequent category. Later **OneHotEnoding** was performed on categorical variables. Baseline's objective would be understand the correlation between variables. 

After running the preprocessing pipeline and training the model, we obtain an **MAE of 37.5 on the training set** and **46.0 on the test set**. While these results are not ideal, the model still performs **better than a naïve mean baseline**, which produces **MAE = 47.5 (train)** and **MAE = 53.85 (test)**. Although the model improves upon the baseline, its overall performance remains weaker than desired. This suggests that additional feature engineering, hyperparameter tuning, or exploring alternative model architectures may be needed to achieve stronger predictive accuracy.

## Final Model

## Fairness Analysis
