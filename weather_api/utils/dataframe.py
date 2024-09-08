from abc import ABC, abstractmethod
from typing import Dict, List, Union

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
            stn_id = df["CLIMATE_IDENTIFIER"].unique()[0]
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
            stn_id = df["STATION_NUMBER"].unique()[0]
            dict_frame[str(stn_id)] = df
        return dict_frame
