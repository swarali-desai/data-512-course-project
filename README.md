# Data driven Analysis of Wildfire Impact on public health in Alexandria, VA

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

More details can be found in the [project report](https://docs.google.com/document/d/1MtXxm5HH9N6pU26YqGjnJ8PF4T9wXpMolHk6RiHlufg/edit?tab=t.0)

## API Documentation

#### 1. USGS Wildfire Dataset API

The Combined Wildland Fire Dataset API provides access to historical wildfire data across the United States from the 1800s to present.Dataset Access: https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81

#### 2. EPA Air Quality System (AQS) API

The EPA AQS API provides historical air quality data across the United States, with standardized measurements beginning in the 1980s: https://aqs.epa.gov/data/api/

This API will require you to sign up and authenticate details are added in the notebook: `epa_air_quality_history.ipynb`

#### Rate Limits

Please refer to [EPA's AirData FAQ](https://www.epa.gov/outdoor-air-quality-data/frequent-questions-about-airdata) for current rate limits

#### Packages

-   [geojson](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://geojson.org/&ved=2ahUKEwiF7rWr4oeKAxVqIDQIHVBoAlwQFnoECBYQAQ&usg=AOvVaw2lqEtsNVseeoxHbIVfRqrB), [pyproj](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pypi.org/project/pyproj/&ved=2ahUKEwiuj4i34oeKAxWYDjQIHc-OHQwQFnoECCAQAQ&usg=AOvVaw3pGA4k4CmIVp32vyCHuuAV): These packages are used to process and handle geographical data
-   [requests](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pypi.org/project/requests/&ved=2ahUKEwjTqs3B4oeKAxUWNjQIHaqsNbwQFnoECBQQAQ&usg=AOvVaw1-RuMU-5ZQL9xNuNrQ3jg4): This package is used to make requests to APIs
-   [pandas](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://pandas.pydata.org/&ved=2ahUKEwjB0ObM4oeKAxUQNzQIHX_2Bh8QFnoECBsQAQ&usg=AOvVaw3cD5ulu4AnZcNusojIyttY): These packages are used for loading data from files, processing different columns and writing data into a file
-   [sklearn](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://scikit-learn.org/&ved=2ahUKEwjc6-fU4oeKAxXQLTQIHRaLJ88QFnoECBgQAQ&usg=AOvVaw3pidYsGhglQXGDh_4GMetL), [statsmodels](https://www.statsmodels.org/stable/index.html), [scipy](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://scipy.org/&ved=2ahUKEwi4u-Lm4oeKAxWmGTQIHS7sMnAQFnoECA0QAQ&usg=AOvVaw1JwxlDaFnouRisaTkMOXjv): These packages are used in building a prediction model for smoke estimates and mortality or hospitalizations.

To install any of these libraries I have included the installation command using pip in the begininng of every notebook.

## Data source:

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

## Set-up required

## Usage

`estimate_wildfire_smoke_impacts.ipynb` : This notebook will calculate the smoke estimates and collect the wildfire data.
`epa_air_quality_history.ipynb` : This notebook will get the AQI data for monitoring stations near Alexandria.
`data_visualization_smoke_estimate.ipynb` : This notebook will create the data visualizations.

To run all of these notebooks we need to install a few packages which are included at the top of every notebook. Running every cell in these notebooks will result in creating intermediary files.

## Data Aquisition

I am analyzing forest fires in [Alexandria, VA](https://en.wikipedia.org/wiki/Alexandria,_Virginia). Alexandria is an independent city (not bound to any county), in the northern region of the Commonwealth of Virginia, United States. The latitude and longitude information is acquired from Wikipedia. Using the reference code provided I have gathered the wildfire data for places around Alexandria using the latitude and longitude information.

Note: The data aquisition process is very long and to optimize I have implemented multithreading which requires multiple cores to run the code thus the total time taken to process the code was about 40 minutes. I have added the code to run on single core in the appendix section of the `estimate_wildfire_smoke_impacts.ipynb` notebook.

Note: Every intermediary file generated is too large to upload on github. If one wishes to veiw these they can be found [here](https://drive.google.com/drive/folders/1dWt8MMqGIDIjCQV1C0WSVlquPa3h5bz_?usp=drive_link)

## Creating fire smoke estimates

The code to develop smoke estimate can be found within `src/estimate_wildfire_smoke_impacts.ipynb`

As part of part 1 - Common analysis I need to find annual estimate of smoke seen by Alexandria, VA during the fire season.

Smoke estimate should adhere to the following conditions:

-   The estimate only considers the last 60 years of wildland fire data (1961-2021).
-   The estimate only considers fires that are within 650 miles of your assigned city.
-   Defines the annual fire season as running from May 1st through October 31st.

Key factors:

-   Linear Decay of Impact by Distance: We assume that the smoke effect decreases linearly with distance.
-   Direct Proportionality to Fire Size: Larger fires produce more smoke, which affects the air quality more.
-   Cumulative Annual Smoke: A cumulative smoke effect for each year is initially used to give an aggregate yearly smoke estimate for simplicity.
-   Circleness_scale is used to represent the intensity of the fire with reference to [this](https://wfca.com/wildfire-articles/fire-intensity-an-in-depth-guide/)

My idea for smoke estimate to find the annual smoke estimates which is inversely propotional to the distance of the fire from the city and directly propotional to the size of the fire. The intensity of the fire is depended on the circleness_scale which determines how intense the fire was. Thus it is directly proportional in my estimate with some adjustment. The type of fire was encoded for calculation and was propotional to my smoke estimate. There could also be other factors like the wind conditions and seasons which might affect the smoke estimates but this information is not available to us right now, otherwise that could be used as factor to be multiplied.

### Smoke Estimate Calculation

Finally the `smoke_estimate` calculation is derived from several wildfire attributes, using the following formula:

`smoke_estimate = ((0.5 + circleness_scale) / 2) * fire_type_encoded * size * (1 / shortest_distance)`

#### Formula Components

-   **`circleness_scale`**: A shape factor, with values closer to 1 indicating more circular fires.
-   **`fire_type_encoded`**: Encoded numeric value for the fire type, allowing differentiation between fire types.
-   **`size`**: The size of the fire in acres.
-   **`shortest_distance`**: The closest distance of the fire to the target location, with closer fires having a more significant impact.

## Gathering AQI data

The code to gather data can be found within `/src/epa_air_quality_history.ipynb`

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

## Predictive time series model

The code for predictive model can be found within `src/estimate_wildfire_smoke_impacts.ipynb`

As the fire data is seasonal time series I have decided to implement a ARIMA model which takes the smoke estimate we have built and predicts till 2025.
In this analysis, I utilized an ARIMA (AutoRegressive Integrated Moving Average) model to forecast wildfire smoke impacts, incorporating wildfire data as external variables within a time-series forecasting framework. This approach combines the strengths of time series analysis and regression, allowing the model to capture both temporal patterns in smoke estimates and the influence of wildfires on air quality.

## Data Visualizations

The code data visuals can be found within `src/data_visualization_smoke_estimate.ipynb`
Reflection for the visuals can also be found [here](https://docs.google.com/document/d/1ZJ8EhwwrAwyVSU1loB1V98pQr32JTgW5a-nTIsWm5_I/edit?usp=sharing)

## Common Analysis - Reflection

https://docs.google.com/document/d/1ZJ8EhwwrAwyVSU1loB1V98pQr32JTgW5a-nTIsWm5_I/edit?usp=sharing

## License

Snippets from this code example was developed by Dr. David W. McDonald for use in DATA 512, a course in the UW MS Data Science degree program. This code is provided under the [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.1 - August 16, 2024 and [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.2 - August 16, 2024

Rest of the code is under MIT license

Note: ChatGPT was used to improve code efficiency

## References
