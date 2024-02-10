import pandas as pd
import xarray as xr
from typing import List, Dict
from abc import ABC, abstractmethod

# this script is used to handle the csv files that are downloaded from the weather api


def _get_unique_rowval(df: pd.DataFrame, col: str) -> str:
    return df[col].unique()[0]


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

    def df_to_xr(self, df: pd.DataFrame) -> xr.Dataset:
        x = _get_unique_rowval(df, "x")
        y = _get_unique_rowval(df, "y")
        station_name = _get_unique_rowval(df, "STATION_NAME")
        province_code = _get_unique_rowval(df, "PROVINCE_CODE")
        climate_identifier = _get_unique_rowval(df, "CLIMATE_IDENTIFIER")
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


class HydrometricStationsXArray(XArrayHandler):
    def __init__(self, dict_frame: Dict[str, pd.DataFrame]):
        self.dict_frame = dict_frame

    def df_to_xr(self, df: pd.DataFrame) -> xr.Dataset:
        x = _get_unique_rowval(df, "x")
        y = _get_unique_rowval(df, "y")
        station_name = _get_unique_rowval(df, "STATION_NAME")
        station_number = _get_unique_rowval(df, "STATION_NUMBER")
        province_code = _get_unique_rowval(df, "PROV_TERR_STATE_LOC")
        df = df.drop(
            columns=[
                "x",
                "y",
                "STATION_NAME",
                "STATION_NUMBER",
                "IDENTIFIER",
                "PROV_TERR_STATE_LOC",
                "DISCHARGE_SYMBOL_EN",
                "DISCHARGE_SYMBOL_FR",
                "LEVEL_SYMBOL_EN",
                "LEVEL_SYMBOL_FR",
            ]
        )
        ds = xr.Dataset.from_dataframe(df)
        ds = ds.rename({"DATE": "time"})
        ds = ds.assign_coords(
            {
                "x": x,
                "y": y,
                "station_number": station_number,
                "station_name": station_name,
                "province_code": province_code,
            }
        )
        ds['DISCHARGE'].attrs['units'] = "m^3/s"
        ds['LEVEL'].attrs['units'] = "m"
        return ds

    def to_xr(self) -> xr.Dataset:
        ds_list = []
        for _, df in self.dict_frame.items():
            ds = self.df_to_xr(df)
            ds_list.append(ds)
        ds = xr.concat(ds_list, dim="station_number")
        return ds
