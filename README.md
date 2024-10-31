# DATA 512 : Course Project

[DATA-512 | Common Analysis - Part 1](https://docs.google.com/document/d/1DRchxt4-mGkQ__zQe-7yif-XvU31s8zMePa82oBz3ek/edit)

## Goal

More and more frequently summers in the western US have been characterized by wildfires with smoke billowing across multiple western states. There are many proposed causes for this: climate change, US Forestry policy, growing awareness, just to name a few. Regardless of the cause, the impact of wildland fires is widespread as wildfire smoke reduces the air quality of many cities. There is a growing body of work pointing to the negative impacts of smoke on health, tourism, property, and other aspects of society.
The course project will require that you analyze wildfire impacts on a specific city in the US. The end goal is to be able to inform policy makers, city managers, city councils, or other civic institutions, to make an informed plan for how they could or whether they should make plans to mitigate future impacts from wildfires.

## License

Snippets from this code example was developed by Dr. David W. McDonald for use in DATA 512, a course in the UW MS Data Science degree program. This code is provided under the [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.1 - August 16, 2024 and [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.2 - August 16, 2024

Rest of the code is under MIT license

Note: ChatGPT was used to make the initial code more efficient.

## API Documentation

#### 1. USGS Wildfire Dataset API

The Combined Wildland Fire Dataset API provides access to historical wildfire data across the United States from the 1800s to present.Dataset Access: https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81

#### 2. EPA Air Quality System (AQS) API

The EPA AQS API provides historical air quality data across the United States, with standardized measurements beginning in the 1980s: https://aqs.epa.gov/data/api/

#### Authentication

Requires API key
[Request API key here](https://aqs.epa.gov/data/api/signup)
Key must be included in all requests

#### Rate Limits

Please refer to [EPA's AirData FAQ](https://www.epa.gov/outdoor-air-quality-data/frequent-questions-about-airdata) for current rate limits

## Data source:

[Combined wildland fire datasets for the United States and certain territories, 1800s-Present (combined wildland fire polygons)](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81) dataset is used for analysis. The combined dataset downloaded has only one fire per year in a given area with one set of attributes. This dataset is intended to create a more comprehensive fire dataset than the existing datasets while eliminating duplication of fire polygons and attributes. It takes about 7-8 minutes to download the data.

Everyone has been assigned one US city that will form the basis for our individual analysis. Source for individual [US city assignment](https://docs.google.com/spreadsheets/d/1pHLA9XzXoy9nJTaiNkgThGPQjVEa0tfeH203I6FA238/edit?gid=0#gid=0) from a Google spreadsheet.

City assigned to me:
|UWNetID |LastName |FirstName |Email |City |State |2023 Estimate |2020 Census |2020 density(mi2)| Location |
|--------|---------|----------|------|----------|-------|--------------|------------|-----------------|----------|
swarali |Desai |Swarali |swarali@uw.edu |Alexandria |VA |155,230 |159,467 |10,702 |38.82°N 77.08°W

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
