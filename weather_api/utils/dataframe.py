import pandas as pd
from .data_types import WeatherStationsDataTypes, HydrometricStationsDataTypes
from typing import List, Dict
from abc import ABC, abstractmethod

# this script is used to handle the csv files that are downloaded from the weather api


class DataframeHandler(ABC):
    @abstractmethod
    def to_df(self, path: str):
        pass

    @abstractmethod
    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        pass


class WeatherStationsDataframe(DataframeHandler):
    """Class to read the weather station data from the Government of Canada's historical weather data API."""

    def __init__(self, paths: List[str]):
        self.paths = paths

    @staticmethod
    def to_df(path: str) -> pd.DataFrame:
        df = pd.read_csv(
            path, dtype=WeatherStationsDataTypes.dtypes, parse_dates=["LOCAL_DATE"]
        )
        df = df.set_index("LOCAL_DATE")
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        dict_frame = {}
        for path in self.paths:
            df = self.to_df(path)
            stn_id = df["CLIMATE_IDENTIFIER"].unique()[0]
            dict_frame[str(stn_id)] = df
        return dict_frame


class HydrometricStationsDataframe(DataframeHandler):
    """Class to read the hydrometric data from the Government of Canada's historical weather data API."""

    def __init__(self, paths: List[str]):
        self.paths = paths

    @staticmethod
    def to_df(path: str) -> pd.DataFrame:
        df = pd.read_csv(
            path, dtype=HydrometricStationsDataTypes.dtypes, parse_dates=["DATE"]
        )
        df = df.set_index("DATE")
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        dict_frame = {}
        for path in self.paths:
            df = self.to_df(path)
            stn_id = df["STATION_NUMBER"].unique()[0]
            dict_frame[str(stn_id)] = df
        return dict_frame
