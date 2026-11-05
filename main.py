import sys
from datetime import date

import matplotlib.pyplot as plt

from gtfs import read, timetable


def draw_network(ax):
    routes = read("routes.txt")
    trips = read("trips.txt")
    stops = read("stops.txt")
    shapes = read("shapes.txt")

    lines = trips[["route_id", "shape_id"]].drop_duplicates().merge(routes, on="route_id")
    paths = dict(tuple(shapes.groupby("shape_id")))
    colors = plt.get_cmap("tab20")

    for i, (_, group) in enumerate(lines.groupby("route_short_name")):
        for shape_id in group.shape_id:
            path = paths[shape_id]
            ax.plot(path.shape_pt_lon, path.shape_pt_lat, color=colors(i % 20), linewidth=1, zorder=1)
    ax.scatter(stops.stop_lon, stops.stop_lat, s=5, color="black", zorder=2)


def positions(times, second):
    following = times.groupby("trip_id").shift(-1)
    moving = times[(times.departure <= second) & (following.arrival > second)]
    following = following.loc[moving.index]
    ratio = (second - moving.departure) / (following.arrival - moving.departure)
    lat = moving.stop_lat + ratio * (following.stop_lat - moving.stop_lat)
    lon = moving.stop_lon + ratio * (following.stop_lon - moving.stop_lon)
    return lon, lat, moving.route_short_name


def main():
    clock = sys.argv[1] if len(sys.argv) > 1 else "08:00"
    day = date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else date.today()
    hours, minutes = map(int, clock.split(":"))

    fig, ax = plt.subplots(figsize=(10, 8))
    draw_network(ax)

    lon, lat, names = positions(timetable(day), hours * 3600 + minutes * 60)
    ax.scatter(lon, lat, s=40, color="red", edgecolor="white", zorder=3)
    for x, y, name in zip(lon, lat, names):
        ax.annotate(str(name), (x, y), fontsize=7, xytext=(3, 3), textcoords="offset points", zorder=4)

    ax.set_title(f"Tramwaje w Krakowie {day} {clock}: {len(lon)} w ruchu")
    ax.set_aspect(1.55)
    plt.show()


if __name__ == "__main__":
    main()