import zipfile
from pathlib import Path

import pandas as pd
import requests

URL = "https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip"
PATH = Path(__file__).parent / "data" / "GTFS_KRK_T.zip"
COLUMNS = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"]


def download():
    if not PATH.exists():
        PATH.parent.mkdir(exist_ok=True)
        PATH.write_bytes(requests.get(URL, timeout=60).content)
    return PATH


def read(name, **kwargs):
    with zipfile.ZipFile(download()) as archive:
        return pd.read_csv(archive.open(name), **kwargs)


def to_seconds(times):
    parts = times.str.split(":", expand=True).astype(int)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def services(day):
    dates = read("calendar_dates.txt")
    dates = dates[dates.date == int(day.strftime("%Y%m%d"))]
    return set(dates.loc[dates.exception_type == 1, "service_id"])


def timetable(day):
    trips = read("trips.txt").merge(read("routes.txt"), on="route_id")
    trips = trips[trips.service_id.isin(services(day))]
    times = read("stop_times.txt", usecols=COLUMNS)
    times = times[times.trip_id.isin(trips.trip_id)]
    times = times.merge(read("stops.txt"), on="stop_id").merge(trips[["trip_id", "route_short_name"]], on="trip_id")
    times["arrival"] = to_seconds(times.arrival_time)
    times["departure"] = to_seconds(times.departure_time)
    return times.sort_values(["trip_id", "stop_sequence"]).reset_index(drop=True)