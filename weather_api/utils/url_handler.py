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
    def build_url(self) -> List[str]:
        pass


class WeatherStationsUrlHandler(UrlHandler):
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def get_bbox_url(self, bbox: list) -> List[str]:
        # runs a climate-stations query to get the climate-identifiers
        # then builds the urls for each climate-identifier
        builder = UrlBuilder("climate-stations")
        builder.bbox = bbox
        response_url = builder.build()
        df = pd.read_csv(response_url)
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
        builder.climate_identifier = stn_id
        response_url = builder.build()
        return response_url

    def build_url(
        self,
        stn_id: Union[str, List[str]] = None,
        bbox: List[float] = None,
    ) -> List[str]:
        if bbox is None and stn_id is None:
            raise ValueError("Either bbox or stn_id must be specified.")
        if bbox is not None:
            return self.get_bbox_url(bbox)
        if isinstance(stn_id, list):
            return [self.get_url(id) for id in stn_id]
        else:
            return [self.get_url(stn_id)]


class HydrometricStationsUrlHandler(UrlHandler):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        stn_id: Union[str, List[str]] = None,
        realtime: str = False,
        bbox: list = None,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.stn_id = stn_id
        self.realtime = realtime
        self.bbox = bbox

    def get_metadata(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-stations")
        if stn_id is not None:
            builder.station_number = stn_id
        else:
            builder.bbox = self.bbox
        response_url = builder.build()
        return response_url

    def get_bbox_url(self) -> List[str]:
        response_url = self.get_metadata()
        df = pd.read_csv(response_url)
        self.stn_id = df["STATION_NUMBER"].unique().tolist()
        urls = []
        for id in self.stn_id:
            response_url = self.get_url(id)
            urls.append(response_url)
        return urls

    def _url_realtime(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-realtime")
        builder.station_number = stn_id
        response_url = builder.build()
        return response_url

    def _url_daily(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-daily-mean")
        builder.date_range_hydrometric = (self.start_date, self.end_date)
        builder.sortby = "DATE"
        builder.station_number = stn_id
        response_url = builder.build()
        return response_url

    def get_url(self, stn_id: str = None) -> str:
        if self.realtime:
            response_url = self._url_realtime(stn_id)
        else:
            response_url = self._url_daily(stn_id)
        return response_url

    def build_url_metadata(self) -> List[str]:
        if isinstance(self.stn_id, list):
            return [self.get_metadata(id) for id in self.stn_id]
        elif isinstance(self.stn_id, str):
            return [self.get_metadata(self.stn_id)]
        else:
            return [self.get_metadata()]

    def build_url(self) -> List[str]:
        if self.bbox is not None:
            return self.get_bbox_url()
        if isinstance(self.stn_id, list):
            return [self.get_url(id) for id in self.stn_id]
        else:
            return [self.get_url(self.stn_id)]
