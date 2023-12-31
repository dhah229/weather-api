class WeatherStationsDataTypes:
    """Used for handling weather station data to pandas dataframes."""

    dtypes = {
        "x": "float32",
        "y": "float32",
        "STATION_NAME": "str",
        "CLIMATE_IDENTIFIER": "str",
        "ID": "str",
        "PROVINCE_CODE": "str",
        "LOCAL_YEAR": "int16",
        "LOCAL_MONTH": "int8",
        "LOCAL_DAY": "int8",
        "MEAN_TEMPERATURE": "float32",
        "MEAN_TEMPERATURE_FLAG": "category",
        "MIN_TEMPERATURE": "float32",
        "MIN_TEMPERATURE_FLAG": "category",
        "MAX_TEMPERATURE": "float32",
        "MAX_TEMPERATURE_FLAG": "category",
        "TOTAL_PRECIPITATION": "float32",
        "TOTAL_PRECIPITATION_FLAG": "category",
        "TOTAL_RAIN": "float32",
        "TOTAL_RAIN_FLAG": "category",
        "TOTAL_SNOW": "float32",
        "TOTAL_SNOW_FLAG": "category",
        "SNOW_ON_GROUND": "float32",
        "SNOW_ON_GROUND_FLAG": "category",
        "DIRECTION_MAX_GUST": "float32",
        "DIRECTION_MAX_GUST_FLAG": "category",
        "SPEED_MAX_GUST": "float32",
        "SPEED_MAX_GUST_FLAG": "category",
        "COOLING_DEGREE_DAYS": "float32",
        "COOLING_DEGREE_DAYS_FLAG": "category",
        "HEATING_DEGREE_DAYS": "float32",
        "HEATING_DEGREE_DAYS_FLAG": "category",
        "MIN_REL_HUMIDITY": "float32",
        "MIN_REL_HUMIDITY_FLAG": "category",
        "MAX_REL_HUMIDITY": "float32",
        "MAX_REL_HUMIDITY_FLAG": "category",
    }


class HydrometricStationsDataTypes:
    """Used for handling hydrometric station data to pandas dataframes."""

    dtypes = {
        "x": "float32",
        "y": "float32",
        "STATION_NAME": "str",
        "STATION_NUMBER": "str",
        "IDENTIFIER": "str",
        "PROV_TERR_STATE_LOC": "str",
        "LEVEL": "float32",
        "DISCHARGE": "float32",
        "DISCHARGE_SYMBOL_EN": "category",
        "DISCHARGE_SYMBOL_FR": "category",
        "LEVEL_SYMBOL_EN": "category",
        "LEVEL_SYMBOL_FR": "category",
    }
