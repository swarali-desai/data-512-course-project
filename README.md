# Data driven Analysis: Wildfire Impact on public health in Alexandria, VA

[DATA-512 | Final Course Project](https://docs.google.com/document/d/1_L8X2sDR868-MLbiqVYBIJ20xy79-YWfyIneePloN6U/edit?tab=t.0)

## Background

More and more frequently summers in the western US have been characterized by wildfires with smoke billowing across multiple western states. There are many proposed causes for this: climate change, US Forestry policy, growing awareness, just to name a few. Regardless of the cause, the impact of wildland fires is widespread as wildfire smoke reduces the air quality of many cities. There is a growing body of work pointing to the negative impacts of smoke on health, tourism, property, and other aspects of society.

Everyone has been assigned one US city that will form the basis for our individual analysis. Source for individual [US city assignment](https://docs.google.com/spreadsheets/d/1pHLA9XzXoy9nJTaiNkgThGPQjVEa0tfeH203I6FA238/edit?gid=0#gid=0) from a Google spreadsheet.

City assigned to me:
|UWNetID |LastName |FirstName |Email |City |State |2023 Estimate |2020 Census |2020 density(mi2)| Location |
|--------|---------|----------|------|----------|-------|--------------|------------|-----------------|----------|
swarali |Desai |Swarali |swarali@uw.edu |Alexandria |VA |155,230 |159,467 |10,702 |38.82°N 77.08°W

## Goal

In this course project I will focus on analyzing the health impact of wildfire smoke on the city of Alexandria, Virginia. I will look at the mortality rate and hospitalizations and find correlation with the smoke estimates because of wildfires. My end goal is to be able to inform policy makers, city managers, city councils, or other civic institutions, to make an informed plan for how they could or whether they should make plans to mitigate future impacts from wildfires.

A secondary goal of this work is to develop the reproducibility & professionalism skills required for real-world data-driven analysis as part of the Fall 2024 DATA 512 course at the University of Washington.

More details can be found in the [project report](Finalreport_data512.pdf)

## API Documentation

#### 1. USGS Wildfire Dataset API

The Combined Wildland Fire Dataset API provides access to historical wildfire data across the United States from the 1800s to present.Dataset Access: https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81

#### 2. EPA Air Quality System (AQS) API

The EPA AQS API provides historical air quality data across the United States, with standardized measurements beginning in the 1980s: https://aqs.epa.gov/data/api/

This API will require you to sign up and authenticate details are added in the notebook: [2_generate_AQI_data.ipynb](src/2_generate_AQI_data.ipynb)

Note:
_Rate Limits_

_Please refer to [EPA's AirData FAQ](https://www.epa.gov/outdoor-air-quality-data/frequent-questions-about-airdata) for current rate limits_

#### Packages

-   [geojson](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://geojson.org/&ved=2ahUKEwiF7rWr4oeKAxVqIDQIHVBoAlwQFnoECBYQAQ&usg=AOvVaw2lqEtsNVseeoxHbIVfRqrB), [pyproj](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pypi.org/project/pyproj/&ved=2ahUKEwiuj4i34oeKAxWYDjQIHc-OHQwQFnoECCAQAQ&usg=AOvVaw3pGA4k4CmIVp32vyCHuuAV): These packages are used to process and handle geographical data
-   [requests](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pypi.org/project/requests/&ved=2ahUKEwjTqs3B4oeKAxUWNjQIHaqsNbwQFnoECBQQAQ&usg=AOvVaw1-RuMU-5ZQL9xNuNrQ3jg4): This package is used to make requests to APIs
-   [pandas](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pandas.pydata.org/&ved=2ahUKEwjB0ObM4oeKAxUQNzQIHX_2Bh8QFnoECBsQAQ&usg=AOvVaw3cD5ulu4AnZcNusojIyttY): These packages are used for loading data from files, processing different columns and writing data into a file
-   [sklearn](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://scikit-learn.org/&ved=2ahUKEwjc6-fU4oeKAxXQLTQIHRaLJ88QFnoECBgQAQ&usg=AOvVaw3pidYsGhglQXGDh_4GMetL), [statsmodels](https://www.statsmodels.org/stable/index.html), [scipy](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://scipy.org/&ved=2ahUKEwi4u-Lm4oeKAxWmGTQIHS7sMnAQFnoECA0QAQ&usg=AOvVaw1JwxlDaFnouRisaTkMOXjv): These packages are used in building a prediction model for smoke estimates and mortality or hospitalizations.

To install any of these libraries I have included the installation command using pip in the begininng of every notebook.

## Data

#### sources:

[Combined wildland fire datasets for the United States and certain territories, 1800s-Present (combined wildland fire polygons)](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81) dataset is used for analysis. You will need to download the data and place it under this location `raw_data/USGS_Wildland_Fire_Combined_Dataset.json`.This file is not committed to the repository since its size exceeds the allowed limits of git. It takes about 7-8 minutes to download the data which is 2.7GB.

[Air Quality Index (AQI) Data from U.S. Environmental Protection Agency's (EPA)](https://aqs.epa.gov/aqsweb/documents/data_api.html) is the air quality index data used in this project was retrieved from the US Environmental Protection Agency (EPA) Air Quality Service (AQS) API. The documentation outlines the available call parameters and includes sample requests. I opted for the bounding box approach, collecting data within a 50-mile radius around Alexandria City for both particulate and gaseous pollutants. These values were then averaged over the years to produce the final smoke estimate.

[IHME chronic respiratory disease mortality data](https://ghdx.healthdata.org/record/ihme-data/united-states-chronic-respiratory-disease-mortality-rates-county-1980-2014) dataset provides age-standardized mortality estimates for chronic respiratory diseases by county, based on de-identified death records, population data, and disease classifications from the Global Burden of Disease Study. I have used this data to get the mortality rate for Asthma and Chronic Obstructive Pulmonary Disease in Alexandria City from the years 2010 to 2021.

| **Column Name**   | **Description**                                                                     |
| ----------------- | ----------------------------------------------------------------------------------- |
| **measure_id**    | Identifier for the specific measure being recorded (e.g., 1 = Deaths).              |
| **measure_name**  | Name of the measure (e.g., Deaths).                                                 |
| **location_id**   | Unique identifier for the location.                                                 |
| **location_name** | Name of the location (e.g., Alexandria City).                                       |
| **FIPS**          | Federal Information Processing Standards code for the location.                     |
| **cause_id**      | Identifier for the cause being measured (e.g., 508 = Chronic respiratory diseases). |
| **cause_name**    | Name of the cause (e.g., Chronic respiratory diseases).                             |
| **sex_id**        | Identifier for sex (e.g., 1 = Male).                                                |
| **sex**           | Sex of the population (e.g., Male).                                                 |
| **age_id**        | Identifier for age group (e.g., 27 = Age-standardized).                             |
| **age_name**      | Name of the age group (e.g., Age-standardized).                                     |
| **year_id**       | Year of the data record (e.g., 1980, 1981).                                         |
| **metric**        | Type of metric being recorded (e.g., Rate).                                         |
| **mx**            | Recorded value for the metric (e.g., 71.639314).                                    |
| **lower**         | Lower confidence interval for the metric value.                                     |
| **upper**         | Upper confidence interval for the metric value.                                     |

[Asthma and COPD hospitalization data](https://ephtracking.cdc.gov/DataExplorer/) data is an extract for Alexandria city from the Centers for Disease Control and Prevention's (CDC) Environmental Public Health Tracking Network. I filtered the data to track positive cases identified in various public health laboratories and included demographic breakdowns such as age groups.

Age-adjusted Rate of Hospitalizations for Asthma/COPD per 10,000 Population for the years 2010-22 divide based on gender. Both Asthma and COPD data have the same format.

| **Column Name** | **Description**                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| **StateFIPS**   | Federal Information Processing Standards (FIPS) code for the state.                                     |
| **State**       | Name of the state (e.g., Virginia).                                                                     |
| **CountyFIPS**  | FIPS code for the county.                                                                               |
| **County**      | Name of the county (e.g., Alexandria).                                                                  |
| **Year**        | Year of the data record (e.g., 2010, 2011).                                                             |
| **Value**       | Recorded value for the metric being analyzed (e.g., asthma hospitalization rate per 10,000 population). |
| **Gender**      | Gender associated with the recorded value (e.g., Male, Female).                                         |

[Census Data](https://data.census.gov/table/ACSST1Y2023.S1301?g=050XX00US51510$1400000_160XX00US5101000) Contains the demographic information from the U.S. Census Bureau will be used to identify demographic populations and death rate for years 2010 to 2021 in Virginia. I have scaled the death rate to Alexanderia city based on its population.

| **Column Name**           | **Description**                                    |
| ------------------------- | -------------------------------------------------- |
| **Year**                  | The year of the data record.                       |
| **Alexandria_Population** | Total population of Alexandria for the given year. |
| **Alexandria_Deaths**     | Total deaths in Alexandria for the given year.     |
| **Virginia_Population**   | Total population of Virginia for the given year.   |
| **Virginia_Deaths**       | Total deaths in Virginia for the given year.       |

[CO poisoning data](https://ephtracking.cdc.gov/DataExplorer) Centers for Disease Control and Prevention. Environmental Public Health Tracking Network.Carbon Monoxide Poisoning Hospitalizations.

| **Column Name**  | **Description**                                                                                                  |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| **StateFIPS**    | Federal Information Processing Standards (FIPS) code for the state.                                              |
| **State**        | Name of the state (e.g., Virginia).                                                                              |
| **Year**         | Year of the data record (e.g., 2010, 2011).                                                                      |
| **Value**        | Recorded value for the metric being analyzed (e.g., percentage or rate of occurrences).                          |
| **Data Comment** | Additional comments or notes about the data (e.g., stability or reliability of the data).                        |
| **Unnamed: 5**   | Placeholder for missing or unused data; typically blank (e.g., NaN).                                             |
| **Cause**        | Identifies the cause associated with the recorded value (e.g., Cause: Fire, Cause: Unknown Mechanism or Intent). |

#### Aquisition and processing

I am analyzing forest fires in [Alexandria, VA](https://en.wikipedia.org/wiki/Alexandria,_Virginia). Alexandria is an independent city (not bound to any county), in the northern region of the Commonwealth of Virginia, United States. The latitude and longitude information is acquired from Wikipedia. Using the reference code provided I have gathered the wildfire data for places around Alexandria using the latitude and longitude information.

The data aquisition process for wildfire is very long and to optimize I have implemented multithreading which requires multiple cores to run the code thus the total time taken to process the code was about 40 minutes. I have added the code to run on single core in the appendix section of the [1_generate_smoke_estimates.ipynb](/src/1_generate_smoke_estimates.ipynb) notebook.

The code to gather data can be found within [2_generate_AQI_data.ipynb](/src/2_generate_AQI_data.ipynb)

We need to get the actual AQI data from the monitoring stations around Alexandria. For this I have implemented the bounding box approach which requires about 50 minutes to run to get the particulate and gaseous particle data.

The final dataframe has the following structure which is resulted by joining the particulate and gaseous AQI parameter data.

| Column Name          | Description                                 | Example Value       |
| -------------------- | ------------------------------------------- | ------------------- |
| **state_code**       | The state FIPS code                         | `08`                |
| **county_code**      | The county FIPS code                        | `005`               |
| **site_number**      | Unique identifier for the site              | `0002`              |
| **parameter_code**   | Code identifying the air quality parameter  | `42101`             |
| **latitude**         | Latitude of the monitoring site             | `39.567887`         |
| **longitude**        | Longitude of the monitoring site            | `-104.957193`       |
| **parameter**        | Name of the monitored air quality parameter | `Carbon monoxide`   |
| **sample_duration**  | Duration over which the sample was taken    | `1 HOUR`            |
| **date_local**       | Date of the measurement                     | `1978-09-16`        |
| **units_of_measure** | Units used for measurement                  | `Parts per million` |
| **arithmetic_mean**  | Arithmetic mean of the measurement values   | `0.000000`          |
| **first_max_value**  | Maximum recorded value in the time period   | `0.0`               |
| **aqi**              | Air Quality Index                           | `NaN` or `0.0`      |

## Set-up required

This work assumes that users have a working Jupyter Notebook & Python 3 setup. Instructions on installing them can be found [here](https://docs.jupyter.org/en/latest/install/notebook-classic.html). Rest of the required libraries and their installation is handlled in the individual notebooks using the pip command.

## Usage

It is preffered to run the notebooks in the following order in the src folder

`1_generate_smoke_estimates.ipynb`  
 Generates historical smoke estimates for Alexandria, Virginia, using wildfire data. The notebook processes raw wildfire datasets, calculates proximity and fire size, and applies a smoke estimation formula to quantify smoke levels based on distance and fire characteristics.

`2_generate_AQI_data.ipynb`  
 Retrieves historical Air Quality Index (AQI) data for Alexandria, VA, using the EPA's AQS API. The notebook processes raw API data for monitoring stations within a 50-mile radius and computes annual average AQI values.

`3_smoke_estimate_forecasting.ipynb`  
 Forecasts future smoke estimates for Alexandria based on historical trends using the ARIMA time-series model. The notebook integrates smoke estimates with AQI data to analyze correlations and predict future smoke levels.

`4_data_visualization_smoke_estimate.ipynb`  
 Visualizes wildfire smoke estimates and their trends through histograms and time-series plots. The notebook highlights spatial distribution, annual trends, and the relationship between smoke estimates and AQI values.

`5_health_data_exploration.ipynb`  
 Explores health-related data, including asthma and COPD hospitalizations and mortality rates. The notebook analyzes trends over time, investigates gender disparities, and assesses correlations with wildfire smoke estimates.

`6_health_impact_forecast.ipynb`  
 Forecasts the future impact of wildfire smoke on health outcomes, specifically asthma and COPD hospitalizations and mortality. The notebook uses SARIMAX models to predict long-term health trends based on smoke exposure and demographic factors.

Running every cell in these notebooks will result in creating intermediary files.

Note: Every intermediary file generated is too large to upload on github. If one wishes to veiw these they can be found [here](https://drive.google.com/drive/folders/1dWt8MMqGIDIjCQV1C0WSVlquPa3h5bz_?usp=drive_link)

## Calculating fire smoke estimates

The code to develop smoke estimate can be found within `src/1_generate_smoke_estimates.ipynb`

As part of part 1 - Common analysis I had to find annual estimate of smoke seen by Alexandria, VA during the fire season.

Smoke estimate should adhere to the following conditions:

-   The estimate only considers the last 60 years of wildland fire data (1961-2021).
-   The estimate only considers fires that are within 650 miles of your assigned city.
-   Defines the annual fire season as running from May 1st through October 31st.

Key factors:

-   Linear Decay of Impact by Distance: We assume that the smoke effect decreases linearly with distance.
-   Direct Proportionality to Fire Size: Larger fires produce more smoke, which affects the air quality more.
-   Cumulative Annual Smoke: A cumulative smoke effect for each year is initially used to give an aggregate yearly smoke estimate for simplicity.
-   Circleness_scale is used to represent the intensity of the fire with reference to [this](https://wfca.com/wildfire-articles/fire-intensity-an-in-depth-guide/)

**Rationale**

My idea for smoke estimate to find the annual smoke estimates which is inversely propotional to the distance of the fire from the city and directly propotional to the size of the fire. The intensity of the fire is depended on the circleness_scale which determines how intense the fire was. Thus it is directly proportional in my estimate with some adjustment. The type of fire was encoded for calculation and was propotional to my smoke estimate. There could also be other factors like the wind conditions and seasons which might affect the smoke estimates but this information is not available to us right now, otherwise that could be used as factor to be multiplied.

Finally the `smoke_estimate` calculation is derived from several wildfire attributes, using the following formula:

`smoke_estimate = ((0.5 + circleness_scale) / 2) * fire_type_encoded * size * (1 / shortest_distance)`

-   **`circleness_scale`**: A shape factor, with values closer to 1 indicating more circular fires.
-   **`fire_type_encoded`**: Encoded numeric value for the fire type, allowing differentiation between fire types.
-   **`size`**: The size of the fire in acres.
-   **`shortest_distance`**: The closest distance of the fire to the target location, with closer fires having a more significant impact.

## Forecasting models

**1. Smoke estimate forecast**

The code for predictive model can be found within `src/3_smoke_estimate_forecasting.ipynb`

In this analysis, I utilized an ARIMA (AutoRegressive Integrated Moving Average) model to forecast wildfire smoke impacts, incorporating wildfire data as external variables within a time-series forecasting framework. This approach combines the strengths of time series analysis and regression, allowing the model to capture both temporal patterns in smoke estimates and the influence of wildfires on air quality.

**2. Health impact forecast**

The code for the model can be found within `src/6_health_impact_forecast.ipynb`

I chose to use an ARIMAX model for its ability to handle exogenous factors which were smoke estimates in my case, enabling robust forecasts of health impacts over a 30-year for Alexandria.
I have built separate models to analyse the effect of smoke on hospitalization and mortality for men and women.

## Generated intermediary files

`hospitalization_asthma_copd.csv` : This contains hospitalization processed data for ALexandria

| Column Name        | Data Type | Description                                                               |
| ------------------ | --------- | ------------------------------------------------------------------------- |
| `year`             | Integer   | The year of the recorded hospitalizations.                                |
| `sex`              | String    | Gender of the population (e.g., Male, Female, Both).                      |
| `age_group`        | String    | Age group of the population (e.g., 0-17, 18-44, 45-64, 65+).              |
| `diagnosis`        | String    | The condition being reported (e.g., Asthma, COPD).                        |
| `hospitalizations` | Integer   | Total number of hospitalizations for the given demographic and condition. |
| `rate`             | Float     | Age-adjusted rate of hospitalizations per 10,000 population.              |

---

`mortality_asthma_copd.csv` : This contains mortality processed data for ALexandria

| Column Name | Data Type | Description                                                     |
| ----------- | --------- | --------------------------------------------------------------- |
| `year`      | Integer   | The year of the recorded mortality data.                        |
| `sex`       | String    | Gender of the population (e.g., Male, Female, Both).            |
| `diagnosis` | String    | The condition being reported (e.g., Asthma, COPD).              |
| `mortality` | Integer   | Total number of deaths for the given demographic and condition. |
| `rate`      | Float     | Age-adjusted rate of mortality per 10,000 population.           |

---

`smoke_estimates_with_forecast.csv` : Smoke estimates forecasted by the ARIMA model

| Column Name                | Data Type | Description                                                  |
| -------------------------- | --------- | ------------------------------------------------------------ |
| `year`                     | Integer   | The year of the smoke estimate or forecast.                  |
| `smoke_estimate`           | Float     | The calculated smoke estimate for the year.                  |
| `forecast`                 | Float     | The forecasted smoke estimate for the year.                  |
| `confidence_interval_low`  | Float     | The lower bound of the confidence interval for the forecast. |
| `confidence_interval_high` | Float     | The upper bound of the confidence interval for the forecast. |

---

`fire_dist_info.csv`: Wildfire information with the following required columns with a 650 miles radius

| Column Name | Data Type | Description                                         |
| ----------- | --------- | --------------------------------------------------- |
| `fire_id`   | String    | Unique identifier for each fire.                    |
| `distance`  | Float     | Distance of the fire from Alexandria, VA, in miles. |
| `fire_type` | String    | The type of fire (e.g., wildfire, prescribed fire). |
| `size`      | Float     | The size of the fire in acres.                      |

---

`fire_error_info.csv`: The fire which had some errors while running.

| Column Name   | Data Type | Description                                                   |
| ------------- | --------- | ------------------------------------------------------------- |
| `fire_id`     | String    | Unique identifier for each fire.                              |
| `error_type`  | String    | Type of error encountered for this fire (e.g., missing data). |
| `description` | String    | Description of the error.                                     |

---

`smoke_estimates.csv`: All the smoke estimates till 2022.

| Column Name      | Data Type | Description                                 |
| ---------------- | --------- | ------------------------------------------- |
| `year`           | Integer   | The year of the smoke estimate.             |
| `smoke_estimate` | Float     | The calculated smoke estimate for the year. |

## Limitations

1. **Data Availability**: The study was limited by incomplete mortality data before 2010 and the inability to access Virginia Respiratory Diseases Data, which restricted the scope of the analysis on smoke-related respiratory impacts.

2. **Dependence on Historical Data**: Variations in reporting practices and methodologies in historical data introduce inconsistencies, impacting the reliability of conclusions.

3. **Simplified Smoke Model**: The smoke model excluded critical factors like wind patterns, fire intensity, and cross-border wildfire contributions, limiting its comprehensiveness and accuracy.

4. **Scope of Wildfire Data**: The analysis focused only on US wildfires, overlooking contributions from Canadian fires, which are known to impact Alexandria's air quality.

5. **Observational Study Design**: As an observational study, the analysis identifies associations but cannot establish causation. The effect size remains uncertain due to the limitations in metric estimation.

## Findings and Conclusion

This study explored the impact of wildfire smoke on respiratory health in Alexandria, Virginia, focusing on asthma and COPD. The findings revealed a weak correlation between smoke exposure and mortality but a moderate link to COPD hospitalizations, particularly among females, highlighting gender disparities. Forecasts showed stable smoke exposure and hospitalization trends over the next three decades, suggesting no significant changes under current conditions.

The analysis highlights the need for targeted public health measures, improved air quality monitoring, and enhanced healthcare infrastructure. Limitations in data and model accuracy underscore the need for future research to refine predictions, integrate real-time data, and address cross-border wildfire contributions. This study demonstrates the value of data-driven approaches in informing public health strategies.

## License

Snippets from this code example was developed by Dr. David W. McDonald for use in DATA 512, a course in the UW MS Data Science degree program. This code is provided under the [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.1 - August 16, 2024 and [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.2 - August 16, 2024

Rest of the code is under [MIT license](LICENSE)

**Data license**

Data pertaining to Wildland Fires, provided by the USGS, are [publicly available](https://www.sciencebase.gov/catalog/item/53f6271fe4b09d12e0e9bd03) and not subject to copyright restrictions. However they can be cited as below.

```
Welty, J.L., and Jeffries, M.I., 2021, Combined wildland fire datasets for the United States and certain territories, 1800s-Present: U.S. Geological Survey data release, https://doi.org/10.5066/P9ZXGFY3.
```

AQI data accessed through the EPA API lies in the [public domain](https://edg.epa.gov/epa_data_license.html) and is not subject to domestic copyright protection under 17 U.S.C. § 105.

Mortality data obtained from Institute for Health Metrics and Evaluation (IHME) is free for [non-commercial research purposes](https://www.healthdata.org/Data-tools-practices/data-practices/ihme-free-charge-non-commercial-user-agreement) but must be cited as below

```
Global Burden of Disease Collaborative Network. Global Burden of Disease Study 2021 (GBD 2021) Results. Seattle, United States: Institute for Health Metrics and Evaluation (IHME), 2022.
https://vizhub.healthdata.org/gbd-results/.
```

## References

-   https://www.epa.gov/wildfire-smoke-course/health-effects-attributed-wildfire-smoke

-   https://ecology.wa.gov/air-climate/air-quality/smoke-fire/health-effects

-   https://www.epa.gov/wildfire-smoke-course/why-wildfire-smoke-health-concern

-   https://www.lung.org/blog/how-wildfires-affect-health

-   https://www.alexandriava.gov/health-department/ahd-publications-reports

-   https://usafacts.org/data/topics/people-society/population-and-demographics/our-changing-population/state/virginia/county/alexandria-city/
-   Alexandria climate data to study confounding factors:
    https://climatecheck.com/virginia/alexandria

-   Alexandria wildfire risk data:
    https://firststreet.org/city/alexandria-va/5101000_fsid/fire?utm_source=redfin

-   canadian wildfires June 7 2023 impact of Alexandria:
    https://www.cnn.com/us/live-news/us-air-quality-canadian-wildfires-06-07-23/index.html
    https://www.alexandriava.gov/news-tes/2023-06-07/air-quality-action-day-notice

-   https://climatecheck.com/virginia/alexandria

Note: ChatGPT was used to improve code efficiency
