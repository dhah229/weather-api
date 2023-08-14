from datetime import datetime
import pandas as pd
from typing import Union, Optional, Dict
import xarray as xr
from .utils.dataframe import HydrometricStationsDataframe
from .utils.url_handler import HydrometricStationsUrlHandler
from .utils.xarray import HydrometricStationsXArray

"""
https://api.weather.gc.ca/
https://api.weather.gc.ca/openapi?f=html
https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
https://climatedata.ca/
"""


class HydrometricStations:
    """Weather station class for retrieving data from the Government of Canada's historical weather data API.

    Either one of `stn_id` or `bbox` must be specified. If both are specified, `bbox` will be used to populate `stn_id`.
    """

    def __init__(
        self,
        stn_id: Union[str, list] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bbox: Optional[list] = None,
    ):
        self.stn_id = stn_id
        self.bbox = bbox
        if start_date is None:
            self.start_date = datetime(1840, 3, 1)
        if end_date is None:
            end_date = datetime.now()
            self.end_date = end_date.replace(hour=0, minute=0, second=0)
        self.url = self.get_url()
        self.dict_frame = None
        self.ds = None

    def get_url(self) -> str:
        url_handler = HydrometricStationsUrlHandler(self.start_date, self.end_date)
        url = url_handler.build_url(
            self.stn_id
        )
        return url

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        wsdf = HydrometricStationsDataframe(self.url)
        self.dict_frame = wsdf.to_dict_frame()
        return self.dict_frame

    def to_xr(self) -> xr.Dataset:
        if self.dict_frame is None:
            self.dict_frame = self.to_dict_frame()
        wsxr = HydrometricStationsXArray(self.dict_frame)
        ds = wsxr.to_xr()
        return ds
