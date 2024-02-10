import pandas as pd
from .data_types import WeatherStationsDataTypes, HydrometricStationsDataTypes
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from pandas.errors import EmptyDataError

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

    def __init__(self, paths: List[str], realtime: bool = False):
        self.paths = paths
        self.realtime = realtime

    def to_df(self, path: str) -> Union[pd.DataFrame, None]:
        date_column = "DATETIME" if self.realtime else "DATE"
        try:
            df = pd.read_csv(
                path, dtype=HydrometricStationsDataTypes.dtypes, parse_dates=[date_column]
            )
        except EmptyDataError:
            print(f"No data found for {path}")
            return None
        df = df.set_index(date_column)
        df.index.rename('DATE', inplace=True)
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
