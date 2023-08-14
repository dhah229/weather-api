from typing import Tuple
from datetime import datetime
import urllib.parse


class UrlBuilder:
    """Class to build the url for the Government of Canada's weather data API."""

    def __init__(self, route: str):
        self.url = f"https://api.weather.gc.ca/collections/{route}/items"
        self.params = {}

    @property
    def date_range(self):
        return self.params.get("datetime")

    @date_range.setter
    def date_range(self, value: Tuple[datetime, datetime]):
        start_date_str = value[0].strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = value[1].strftime("%Y-%m-%d %H:%M:%S")
        self.params["datetime"] = f"{start_date_str}/{end_date_str}"

    @property
    def date_range_hydrometric(self):
        return self.params.get("datetime")
    
    @date_range_hydrometric.setter
    def date_range_hydrometric(self, value: Tuple[datetime, datetime]):
        start_date_str = value[0].strftime("%Y-%m-%d")
        end_date_str = value[1].strftime("%Y-%m-%d")
        self.params["datetime"] = f"{start_date_str}/{end_date_str}"

    @property
    def sortby(self):
        return self.params.get("sortby")

    @sortby.setter
    def sortby(self, value):
        self.params["sortby"] = value

    @property
    def format(self):
        return self.params.get("f")

    @format.setter
    def format(self, value):
        self.params["f"] = value

    @property
    def limit(self):
        return self.params.get("limit")

    @limit.setter
    def limit(self, value):
        self.params["limit"] = value

    @property
    def startindex(self):
        return self.params.get("startindex")

    @startindex.setter
    def startindex(self, value):
        self.params["startindex"] = value

    @property
    def bbox(self):
        return self.params.get("bbox")

    @bbox.setter
    def bbox(self, value):
        self.params["bbox"] = ",".join([str(x) for x in value])

    @property
    def climate_identifier(self):
        return self.params.get("CLIMATE_IDENTIFIER")

    @climate_identifier.setter
    def climate_identifier(self, value):
        self.params["CLIMATE_IDENTIFIER"] = value

    @property
    def station_number(self):
        return self.params.get("STATION_NUMBER")
    
    @station_number.setter
    def station_number(self, value):
        self.params["STATION_NUMBER"] = value

    def build(self) -> str:
        query_string = urllib.parse.urlencode(self.params)
        response_url = f"{self.url}?{query_string}"
        return response_url
