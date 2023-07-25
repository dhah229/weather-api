from datetime import datetime
import pandas as pd
from typing import Union, Optional, Tuple
import xarray as xr
from .utils.dataframe import WeatherStationsDataframe
from .utils.url_handler import WeatherStationsUrlHandler

"""
https://api.weather.gc.ca/
https://api.weather.gc.ca/openapi?f=html
https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
https://climatedata.ca/
"""


class WeatherStations:
    """Weather station class for retrieving data from the Government of Canada's historical weather data API.

    Either one of `stn_id` or `bbox` must be specified. If both are specified, `bbox` will be used to populate `stn_id`.
    """

    def __init__(
        self,
        stn_id: Union[str, list] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bbox: Optional[list] = None,
        min_years: Optional[int] = None,
        last_date: Optional[datetime] = None,
    ):
        self.stn_id = stn_id
        self.bbox = bbox
        self.min_years = min_years
        self.last_date = last_date
        if start_date is None:
            self.start_date = datetime(1840, 3, 1)
        if end_date is None:
            end_date = datetime.now()
            self.end_date = end_date.replace(hour=0, minute=0, second=0)
        url_handler = WeatherStationsUrlHandler(self.start_date, self.end_date)
        self.url = url_handler.build_url(
            self.stn_id,
            self.bbox,
            self.min_years,
            self.last_date,
        )

    def to_dict_frame(self) -> Union[pd.DataFrame, dict]:
        wsdf = WeatherStationsDataframe(self.url)
        dict_frame = wsdf.to_dict_frame()
        return dict_frame

    @staticmethod
    def _get_unique_rowval(df: pd.DataFrame, col: str) -> str:
        return df[col].unique()[0]

    def _df_to_xr(self, df: pd.DataFrame) -> xr.Dataset:
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
        dict_frame = self.to_dict_frame()
        ds_list = []
        for _, df in dict_frame.items():
            ds = self._df_to_xr(df)
            ds_list.append(ds)
        ds = xr.concat(ds_list, dim="station")
        return ds
