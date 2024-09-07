from abc import ABC, abstractmethod

import folium
import pandas as pd
from folium.plugins import MarkerCluster


class PlottingHandler(ABC):
    @abstractmethod
    def plot_stations(self, meta: pd.DataFrame) -> folium.Map:
        pass


def _date_str(input_date: pd.Series) -> str:
    """Converts a date to a string.

    If the input date is null, returns "N/A".
    """
    if pd.isnull(input_date):
        return "N/A"
    else:
        return input_date.strftime("%Y-%m-%d")


class WeatherStationsPlottingHandler(PlottingHandler):
    def plot_stations(meta: pd.DataFrame) -> folium.Map:
        """Maps out the input meta data for weather stations.

        Returns a folium map object with markers for each weather station.
        """
        m = folium.Map(location=[60.5, -100.5], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)

        meta["DLY_FIRST_DATE"] = pd.to_datetime(
            meta["DLY_FIRST_DATE"], format="%Y-%m-%d %H:%M:%S"
        )
        meta["DLY_LAST_DATE"] = pd.to_datetime(
            meta["DLY_LAST_DATE"], format="%Y-%m-%d %H:%M:%S"
        )

        for _, row in meta.iterrows():
            first_date = _date_str(row["DLY_FIRST_DATE"])
            last_date = _date_str(row["DLY_LAST_DATE"])

            popup = f"""
            <div style="width: 200px; word-wrap: break-word;">
                <b>{row['STATION_NAME']}</b><br>
                Climate ID: {row['CLIMATE_IDENTIFIER']}<br>
                Date range: {first_date} to {last_date}<br>
            </div>
            """
            folium.Marker(
                location=[row["y"], row["x"]],
                popup=popup,
                icon=folium.Icon(icon="cloud"),
            ).add_to(marker_cluster)
        return m


class HydrometricStationsPlottingHandler(PlottingHandler):
    def plot_stations(meta: pd.DataFrame) -> folium.Map:
        """Maps out the input meta data for hydrometric stations.

        Returns a folium map object with markers for each hydrometric station.
        """
        m = folium.Map(location=[60.5, -100.5], zoom_start=4)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in meta.iterrows():
            popup = f"""
            <div style="width: 200px; word-wrap: break-word;">
                <b>{row['STATION_NAME']}</b><br>
                Station number: {row['STATION_NUMBER']}<br>
                Status: {row['STATUS_EN']}<br>
            </div>
            """
            folium.Marker(
                location=[row["y"], row["x"]],
                popup=popup,
                icon=folium.Icon(icon="tint"),
            ).add_to(marker_cluster)
        return m
