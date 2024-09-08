from abc import ABC, abstractmethod
from typing import Dict, List

import pandas as pd
import xarray as xr

# this script is used to handle the csv files that are downloaded from the weather api


def _get_unique_rowval(df: pd.DataFrame, col: str) -> str:
    if col in df.columns:
        return df[col].unique()[0]
    else:
        return None


def _candidate_columns_to_drop(df: pd.DataFrame, columns: List[str]) -> List[str]:
    cols = [col for col in columns if col in df.columns]
    return cols


def _candidate_coords_to_assign(coords: dict) -> dict:
    coordinates = {key: item for key, item in coords.items() if item is not None}
    return coordinates


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

    def df_to_xr(self, df: pd.DataFrame, stn_id: str) -> xr.Dataset:
        x = _get_unique_rowval(df, "x")
        y = _get_unique_rowval(df, "y")
        station_name = _get_unique_rowval(df, "STATION_NAME")
        province_code = _get_unique_rowval(df, "PROVINCE_CODE")
        columns = [
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
        columns = _candidate_columns_to_drop(df=df, columns=columns)
        df = df.drop(columns=columns)
        ds = xr.Dataset.from_dataframe(df)
        ds = ds.rename({"LOCAL_DATE": "time"})
        coords = {
            "x": x,
            "y": y,
            "climate_identifier": stn_id,
            "station_name": station_name,
            "province_code": province_code,
        }
        coords = _candidate_coords_to_assign(coords=coords)
        ds = ds.assign_coords(coords=coords)
        return ds

    def to_xr(self) -> xr.Dataset:
        ds_list = []
        for stn_id, df in self.dict_frame.items():
            ds = self.df_to_xr(df=df, stn_id=stn_id)
            ds_list.append(ds)
        ds = xr.concat(ds_list, dim="climate_identifier")
        return ds


class HydrometricStationsXArray(XArrayHandler):
    def __init__(self, dict_frame: Dict[str, pd.DataFrame]):
        self.dict_frame = dict_frame

    @staticmethod
    def _assign_units(ds: xr.Dataset) -> xr.Dataset:
        if "DISCHARGE" in ds.data_vars:
            ds["DISCHARGE"].attrs["units"] = "m3 s-1"
            ds["DISCHARGE"].attrs[
                "standard_name"
            ] = "water_volume_transport_in_river_channel"
            ds["DISCHARGE"].attrs["long_name"] = "River discharge"
        if "LEVEL" in ds.data_vars:
            ds["LEVEL"].attrs["units"] = "m"
            ds["LEVEL"].attrs["standard_name"] = "water_level_in_river_channel"
            ds["LEVEL"].attrs["long_name"] = "River level"
        return ds

    def df_to_xr(self, df: pd.DataFrame, stn_id: str) -> xr.Dataset:
        x = _get_unique_rowval(df, "x")
        y = _get_unique_rowval(df, "y")
        station_name = _get_unique_rowval(df, "STATION_NAME")
        province_code = _get_unique_rowval(df, "PROV_TERR_STATE_LOC")
        columns = [
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
        columns = _candidate_columns_to_drop(df=df, columns=columns)
        df = df.drop(columns=columns)
        ds = xr.Dataset.from_dataframe(df)
        ds = ds.rename({"DATE": "time"})
        coords = {
            "x": x,
            "y": y,
            "station_number": stn_id,
            "station_name": station_name,
            "province_code": province_code,
        }
        coords = _candidate_coords_to_assign(coords=coords)
        ds = ds.assign_coords(coords=coords)
        ds = self._assign_units(ds=ds)
        return ds

    def to_xr(self) -> xr.Dataset:
        ds_list = []
        for stn_id, df in self.dict_frame.items():
            ds = self.df_to_xr(df=df, stn_id=stn_id)
            ds_list.append(ds)
        ds = xr.concat(ds_list, dim="station_number")
        return ds
