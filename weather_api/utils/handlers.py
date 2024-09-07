from abc import ABC

from .dataframe import (
    DataFrameHandler,
    HydrometricStationsDataframe,
    WeatherStationsDataframe,
)
from .plotting_handler import (
    HydrometricStationsPlottingHandler,
    PlottingHandler,
    WeatherStationsPlottingHandler,
)
from .url_handler import (
    HydrometricStationsUrlHandler,
    UrlHandler,
    WeatherStationsUrlHandler,
)
from .xarray import HydrometricStationsXArray, WeatherStationsXArray, XArrayHandler

"""Script to contain the handlers for the API endpoints."""


class DataHandler(ABC):
    url_handler: UrlHandler
    dataframe_handler: DataFrameHandler
    xarray_handler: XArrayHandler
    plotting_handler: PlottingHandler


class WeatherStationsDataHandler(DataHandler):
    url_handler = WeatherStationsUrlHandler
    dataframe_handler = WeatherStationsDataframe
    xarray_handler = WeatherStationsXArray
    plotting_handler = WeatherStationsPlottingHandler


class HydrometricStationsDataHandler(DataHandler):
    url_handler = HydrometricStationsUrlHandler
    dataframe_handler = HydrometricStationsDataframe
    xarray_handler = HydrometricStationsXArray
    plotting_handler = HydrometricStationsPlottingHandler
