from abc import ABC, abstractmethod
from typing import Union, List
from .url_builder import UrlBuilder
import pandas as pd
from datetime import datetime


class UrlHandler(ABC):
    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_bbox_url(self) -> List[str]:
        pass

    @abstractmethod
    def build_url(self) -> List[str]:
        pass


class WeatherStationsUrlHandler(UrlHandler):
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def get_bbox_url(
        self, bbox: list, min_years: int = None, last_date: datetime = None
    ) -> List[str]:
        # runs a climate-stations query to get the climate-identifiers
        # then builds the urls for each climate-identifier
        builder = UrlBuilder("climate-stations")
        builder.bbox = bbox
        builder.format = "csv"
        builder.limit = "1500000"
        builder.startindex = "0"
        response_url = builder.build()
        df = pd.read_csv(response_url)
        if min_years is not None:
            # only get stations that have data for at least min_years
            f_date = pd.to_datetime(df["FIRST_DATE"])
            l_date = pd.to_datetime(df["LAST_DATE"])
            df = df[(l_date - f_date).dt.days >= min_years * 365]
        if last_date is not None:
            # only get stations that have data past the last_date
            l_date = pd.to_datetime(df["LAST_DATE"])
            df = df[l_date >= last_date]

        self.stn_id = df["CLIMATE_IDENTIFIER"].unique().tolist()
        urls = []
        for id in self.stn_id:
            response_url = self.get_url(id)
            urls.append(response_url)
        return urls

    def get_url(self, stn_id: str = None) -> str:
        builder = UrlBuilder("climate-daily")
        builder.date_range = (self.start_date, self.end_date)
        builder.sortby = "PROVINCE_CODE,STN_ID,LOCAL_DATE"
        builder.format = "csv"
        builder.limit = "1500000"
        builder.startindex = "0"
        builder.climate_identifier = stn_id
        response_url = builder.build()
        return response_url

    def build_url(
        self,
        stn_id: Union[str, List[str]] = None,
        bbox: List[float] = None,
        min_years: int = None,
        last_date: datetime = None,
    ) -> List[str]:
        if bbox is None and stn_id is None:
            raise ValueError("Either bbox or stn_id must be specified.")
        if bbox is not None:
            return self.get_bbox_url(bbox, min_years, last_date)
        if isinstance(stn_id, list):
            return [self.get_url(id) for id in stn_id]
        else:
            return [self.get_url(stn_id)]


class HydrometricStationsUrlHandler(UrlHandler):
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def get_bbox_url(self):
        pass

    def get_url(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-daily-mean")
        builder.date_range_hydrometric = (self.start_date, self.end_date)
        builder.sortby = "DATE"
        builder.format = "csv"
        builder.limit = "1500000"
        builder.startindex = "0"
        builder.station_number = stn_id
        response_url = builder.build()
        return response_url

    def build_url(self, stn_id: Union[str, List[str]] = None):
        return [self.get_url(stn_id)]
