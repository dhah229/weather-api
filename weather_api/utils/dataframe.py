from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict, List, Union
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from urllib.request import urlopen

import pandas as pd
from pandas.errors import EmptyDataError

from .data_types import HydrometricStationsDataTypes, WeatherStationsDataTypes

# this script is used to handle the csv files that are downloaded from the weather api


class DataFrameHandler(ABC):
    MAX_PAGE_SIZE = 10000

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

    def _page_url(self, path: str, offset: int, limit: int) -> str:
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)
        query_params["limit"] = [str(limit)]
        query_params["offset"] = [str(offset)]
        query_params.pop("startindex", None)
        paged_query = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=paged_query))

    def _read_csv_paginated(self, path: str, **kwargs) -> pd.DataFrame:
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        requested_limit = int(query_params.get("limit", [self.MAX_PAGE_SIZE])[0])
        page_size = min(requested_limit, self.MAX_PAGE_SIZE)
        start_offset = int(
            query_params.get(
                "offset",
                query_params.get("startindex", [0]),
            )[0]
        )

        frames = []
        offset = start_offset
        while True:
            paged_url = self._page_url(path=path, offset=offset, limit=page_size)
            with urlopen(paged_url) as response:
                payload = response.read().decode("utf-8")
            try:
                df = pd.read_csv(StringIO(payload), **kwargs)
            except EmptyDataError:
                break
            if df.empty:
                break
            frames.append(df)
            if len(df) < page_size:
                break
            offset += page_size

        if not frames:
            raise EmptyDataError(f"No columns to parse from {path}")
        return pd.concat(frames, ignore_index=True)


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
        df = self._read_csv_paginated(
            path,
            dtype=dtypes,
            parse_dates=["LOCAL_DATE"],
        )
        df = df.set_index("LOCAL_DATE")
        # Ensure the index is timezone-naive for xarray
        df.index = df.index.tz_localize(None)
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        dict_frame = {}
        for path in self.paths:
            try:
                df = self.to_df(path)
            except EmptyDataError:
                continue
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
            df = self._read_csv_paginated(
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
