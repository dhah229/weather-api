from abc import ABC, abstractmethod
from typing import Dict, List, Union
from urllib.parse import parse_qs, urlparse

import pandas as pd
from pandas.errors import EmptyDataError

from .data_types import HydrometricStationsDataTypes, WeatherStationsDataTypes

# this script is used to handle the csv files that are downloaded from the weather api


class DataFrameHandler(ABC):
    @abstractmethod
    def to_df(self, path: str):
        pass

    @abstractmethod
    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        pass

    def get_station_from_path(self, path: str, station_key: str) -> Union[str, None]:
        """This method is used to get station from the URL"""
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        station = query_params.get(station_key, [None])[0]
        return station


class WeatherStationsDataframe(DataFrameHandler):
    """Class to read the weather station data from the Government of Canada's historical weather data API."""

    def __init__(self, paths: List[str], hourly: bool = False):
        self.paths = paths
        self.hourly = hourly

    def to_df(self, path: str) -> pd.DataFrame:
        if self.hourly:
            dtypes = WeatherStationsDataTypes.dtypes_hourly
        else:
            dtypes = WeatherStationsDataTypes.dtypes_daily
        df = pd.read_csv(path, dtype=dtypes, parse_dates=["LOCAL_DATE"])
        df = df.set_index("LOCAL_DATE")
        # Ensure the index is timezone-naive for xarray
        df.index = df.index.tz_localize(None)
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        dict_frame = {}
        for path in self.paths:
            df = self.to_df(path)
            stn_id = self.get_station_from_path(
                path=path,
                station_key="CLIMATE_IDENTIFIER",
            )
            if stn_id is None:
                raise ValueError(f"Could not determine station name from {path}")
            dict_frame[str(stn_id)] = df
        return dict_frame


class HydrometricStationsDataframe(DataFrameHandler):
    """Class to read the hydrometric data from the Government of Canada's historical weather data API."""

    def __init__(self, paths: List[str], realtime: bool = False):
        self.paths = paths
        self.realtime = realtime

    def to_df(self, path: str) -> Union[pd.DataFrame, None]:
        date_column = "DATETIME" if self.realtime else "DATE"
        try:
            df = pd.read_csv(
                path,
                dtype=HydrometricStationsDataTypes.dtypes,
                parse_dates=[date_column],
            )
        except EmptyDataError:
            print(f"No data found for {path}")
            return None
        df = df.set_index(date_column)
        df.index.rename("DATE", inplace=True)
        # Ensure the index is timezone-naive for xarray
        df.index = df.index.tz_localize(None)
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        dict_frame = {}
        for path in self.paths:
            df = self.to_df(path)
            if df is None:
                continue
            stn_id = self.get_station_from_path(
                path=path,
                station_key="STATION_NUMBER",
            )
            if stn_id is None:
                raise ValueError(f"Could not determine station name from {path}")
            dict_frame[str(stn_id)] = df
        return dict_frame
