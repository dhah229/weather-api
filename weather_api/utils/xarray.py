import pandas as pd
import xarray as xr
from typing import List, Dict
from abc import ABC, abstractmethod

# this script is used to handle the csv files that are downloaded from the weather api


class XArrayHandler(ABC):
    @abstractmethod
    def to_xr(self, path: str):
        pass

    @abstractmethod
    def df_to_xr(self) -> Dict[str, pd.DataFrame]:
        pass


class WeatherStationsXArray(XArrayHandler):
    """Class to convert weather station dataframes to an xarray dataset"""

    def __init__(self, dict_frame: Dict[str, pd.DataFrame]):
        self.dict_frame = dict_frame

    @staticmethod
    def _get_unique_rowval(df: pd.DataFrame, col: str) -> str:
        return df[col].unique()[0]

    def df_to_xr(self, df: pd.DataFrame) -> xr.Dataset:
        x = self._get_unique_rowval(df, "x")
        y = self._get_unique_rowval(df, "y")
        station_name = self._get_unique_rowval(df, "STATION_NAME")
        province_code = self._get_unique_rowval(df, "PROVINCE_CODE")
        climate_identifier = self._get_unique_rowval(df, "CLIMATE_IDENTIFIER")
        df = df.drop(
            columns=[
                "x",
                "y",
                "STATION_NAME",
                "CLIMATE_IDENTIFIER",
                "ID",
                "PROVINCE_CODE",
                "LOCAL_YEAR",
                "LOCAL_MONTH",
                "LOCAL_DAY",
            ]
        )
        ds = xr.Dataset.from_dataframe(df)
        ds = ds.rename({"LOCAL_DATE": "time"})
        ds = ds.assign_coords(
            {
                "x": x,
                "y": y,
                "station": climate_identifier,
                "station_name": station_name,
                "province_code": province_code,
            }
        )
        return ds

    def to_xr(self) -> xr.Dataset:
        ds_list = []
        for _, df in self.dict_frame.items():
            ds = self.df_to_xr(df)
            ds_list.append(ds)
        ds = xr.concat(ds_list, dim="station")
        return ds
