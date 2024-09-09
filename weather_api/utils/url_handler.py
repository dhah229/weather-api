from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Union

import pandas as pd

from .url_builder import UrlBuilder


class UrlHandler(ABC):
    @abstractmethod
    def get_url(self) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def build_url(self) -> List[str]:  # pragma: no cover
        pass

    @abstractmethod
    def build_url_metadata(self) -> List[str]:  # pragma: no cover
        pass


class WeatherStationsUrlHandler(UrlHandler):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        stn_id: Union[str, List[str]] = None,
        hourly: bool = False,
        bbox: List[float] = None,
        properties: List[str] = None,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.stn_id = stn_id
        self.hourly = hourly
        self.bbox = bbox
        if isinstance(properties, str):
            properties = [properties]
        if properties is not None:
            properties = [p.upper() for p in properties]
            self._properties_check(properties)
        self.properties = properties

    def _properties_check(self, properties: List[str]) -> None:
        allowed_properties_hourly = [
            "CLIMATE_IDENTIFIER",
            "DEW_POINT_TEMP",
            "DEW_POINT_TEMP_FLAG",
            "HUMIDEX",
            "HUMIDEX_FLAG",
            "ID",
            "LATITUDE_DECIMAL_DEGREES",
            "LOCAL_DATE",
            "LOCAL_DAY",
            "LOCAL_HOUR",
            "LOCAL_MONTH",
            "LOCAL_YEAR",
            "LONGITUDE_DECIMAL_DEGREES",
            "PRECIP_AMOUNT",
            "PRECIP_AMOUNT_FLAG",
            "PROVINCE_CODE",
            "RELATIVE_HUMIDITY",
            "RELATIVE_HUMIDITY_FLAG",
            "STATION_NAME",
            "STATION_PRESSURE",
            "STATION_PRESSURE_FLAG",
            "STN_ID",
            "TEMP",
            "TEMP_FLAG",
            "UTC_DATE",
            "UTC_DAY",
            "UTC_MONTH",
            "UTC_YEAR",
            "VISIBILITY",
            "VISIBILITY_FLAG",
            "WEATHER_ENG_DESC",
            "WEATHER_FRE_DESC",
            "WINDCHILL",
            "WINDCHILL_FLAG",
            "WIND_DIRECTION",
            "WIND_DIRECTION_FLAG",
            "WIND_SPEED",
            "WIND_SPEED_FLAG",
        ]

        allowed_properties_daily = [
            "CLIMATE_IDENTIFIER",
            "COOLING_DEGREE_DAYS",
            "COOLING_DEGREE_DAYS_FLAG",
            "DIRECTION_MAX_GUST",
            "DIRECTION_MAX_GUST_FLAG",
            "HEATING_DEGREE_DAYS",
            "HEATING_DEGREE_DAYS_FLAG",
            "ID",
            "LOCAL_DATE",
            "LOCAL_DAY",
            "LOCAL_MONTH",
            "LOCAL_YEAR",
            "MAX_REL_HUMIDITY",
            "MAX_REL_HUMIDITY_FLAG",
            "MAX_TEMPERATURE",
            "MAX_TEMPERATURE_FLAG",
            "MEAN_TEMPERATURE",
            "MEAN_TEMPERATURE_FLAG",
            "MIN_REL_HUMIDITY",
            "MIN_REL_HUMIDITY_FLAG",
            "MIN_TEMPERATURE",
            "MIN_TEMPERATURE_FLAG",
            "PROVINCE_CODE",
            "SNOW_ON_GROUND",
            "SNOW_ON_GROUND_FLAG",
            "SOURCE",
            "SPEED_MAX_GUST",
            "SPEED_MAX_GUST_FLAG",
            "STATION_NAME",
            "STN_ID",
            "TOTAL_PRECIPITATION",
            "TOTAL_PRECIPITATION_FLAG",
            "TOTAL_RAIN",
            "TOTAL_RAIN_FLAG",
            "TOTAL_SNOW",
            "TOTAL_SNOW_FLAG",
        ]
        if self.hourly:
            for prop in properties:
                if prop not in allowed_properties_hourly:
                    raise ValueError(
                        f"{prop} is not a valid property for hourly data. "
                        + f"Valid properties are: {allowed_properties_hourly}"
                    )
        else:
            for prop in properties:
                if prop not in allowed_properties_daily:
                    raise ValueError(
                        f"{prop} is not a valid property for daily data. "
                        + f"Valid properties are: {allowed_properties_daily}"
                    )

    def get_metadata(self, stn_id: str = None) -> str:
        builder = UrlBuilder("climate-stations")
        if stn_id is not None:
            builder.climate_identifier = stn_id
        elif self.bbox is not None:
            builder.bbox = self.bbox
        response_url = builder.build()
        return response_url

    def get_bbox_url(self) -> List[str]:
        response_url = self.get_metadata()
        df = pd.read_csv(response_url)
        self.stn_id = df["CLIMATE_IDENTIFIER"].unique().tolist()
        urls = []
        for id in self.stn_id:
            response_url = self.get_url(id)
            urls.append(response_url)
        return urls

    def get_url(self, stn_id: str = None) -> str:
        if self.hourly:
            builder = UrlBuilder("climate-hourly")
        else:
            builder = UrlBuilder("climate-daily")
        builder.date_range = (self.start_date, self.end_date)
        builder.sortby = "PROVINCE_CODE,STN_ID,LOCAL_DATE"
        builder.climate_identifier = stn_id
        if self.properties is not None:
            if "LOCAL_DATE" not in self.properties:
                # if we don't add this, we may not get any dates.
                self.properties.append("LOCAL_DATE")
            builder.properties = self.properties
        response_url = builder.build()
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


class HydrometricStationsUrlHandler(UrlHandler):
    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        stn_id: Union[str, List[str]] = None,
        realtime: bool = False,
        bbox: list = None,
        properties: List[str] = None,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.stn_id = stn_id
        self.realtime = realtime
        self.bbox = bbox
        if isinstance(properties, str):
            properties = [properties]
        if properties is not None:
            properties = [p.upper() for p in properties]
            self._properties_check(properties)
        self.properties = properties

    def _properties_check(self, properties: List[str]) -> None:
        allowed_properties_realtime = [
            "DATETIME",
            "DATETIME_LST",
            "DISCHARGE",
            "DISCHARGE_SYMBOL_EN",
            "DISCHARGE_SYMBOL_FR",
            "IDENTIFIER",
            "LEVEL",
            "LEVEL_SYMBOL_EN",
            "LEVEL_SYMBOL_FR",
            "PROV_TERR_STATE_LOC",
            "STATION_NAME",
            "STATION_NUMBER",
        ]

        allowed_properties_daily = [
            "DATE",
            "DISCHARGE",
            "DISCHARGE_SYMBOL_EN",
            "DISCHARGE_SYMBOL_FR",
            "IDENTIFIER",
            "LEVEL",
            "LEVEL_SYMBOL_EN",
            "LEVEL_SYMBOL_FR",
            "PROV_TERR_STATE_LOC",
            "STATION_NAME",
            "STATION_NUMBER",
        ]
        if self.realtime:
            for prop in properties:
                if prop not in allowed_properties_realtime:
                    raise ValueError(
                        f"{prop} is not a valid property for realtime data. "
                        + f"Valid properties are: {allowed_properties_realtime}"
                    )
        else:
            for prop in properties:
                if prop not in allowed_properties_daily:
                    raise ValueError(
                        f"{prop} is not a valid property for daily data. "
                        + f"Valid properties are: {allowed_properties_daily}"
                    )

    def get_metadata(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-stations")
        if stn_id is not None:
            builder.station_number = stn_id
        elif self.bbox is not None:
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
        if self.properties is not None:
            if "DATETIME" not in self.properties:
                # if we don't add this, we may not get any dates.
                self.properties.append("DATETIME")
            builder.properties = self.properties
        response_url = builder.build()
        return response_url

    def _url_daily(self, stn_id: str = None) -> str:
        builder = UrlBuilder("hydrometric-daily-mean")
        builder.date_range_hydrometric = (self.start_date, self.end_date)
        builder.sortby = "DATE"
        builder.station_number = stn_id
        if self.properties is not None:
            if "DATE" not in self.properties:
                # if we don't add this, we may not get any dates.
                self.properties.append("DATE")
            builder.properties = self.properties
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
