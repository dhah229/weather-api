from datetime import datetime
from typing import Optional, Union

from .base import GeoMetAPI
from .utils.handlers import HydrometricStationsDataHandler

"""
https://api.weather.gc.ca/openapi?f=html
"""


class HydrometricStations(GeoMetAPI):
    """Hydrometric station class for retrieving data from the Government of Canada's historical weather data API.

    Attributes
    ----------
    stn_id : Union[str, list]
        The station number(s) to retrieve data for. If `bbox` is not specified, `stn_id` must be specified.
    start_date : Optional[datetime]
        The start date of the data to retrieve. If not specified, the default is 1840, 3, 1.
    end_date : Optional[datetime]
        The end date of the data to retrieve. If not specified, the default is the current date at midnight.
    bbox : Optional[list]
        The bounding box to retrieve data for (left, bottom, right, top).
        If `stn_id` is not specified, `bbox` must be specified.
    realtime : bool
        If True, retrieve the realtime-data. If False, retrieve historical data.
    """

    def __init__(
        self,
        stn_id: Optional[Union[str, list]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bbox: Optional[list] = None,
        realtime: bool = False,
    ):
        super().__init__(
            stn_id=stn_id,
            start_date=start_date,
            end_date=end_date,
            bbox=bbox,
            realtime=realtime,
            data_handler=HydrometricStationsDataHandler,
        )
