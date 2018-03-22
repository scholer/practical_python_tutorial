
"""

Refs:
* https://developers.google.com/transit/gtfs-realtime/guides/vehicle-positions
* https://github.com/luqmaan/awesome-transit
* https://transloc.desk.com/customer/en/portal/articles/2768207-navigating-the-manager-map


Regarding speed:
* GPFS spec is in m/s, and 1 m/s = 3.6 KPH = 2.24 MPH.
* But that doens't seem right for transloc.
* The following source seems to think it is likely in KPH:
  https://github.com/Transitime/core/blob/master/transitime/src/main/java/org/transitime/avl/TranslocAvlModule.java
*

"""
import sys
import os
import requests
from pprint import pprint
import yaml
try:
    from practical_python.utils.geo_utils import haversine as gps_dist
except ImportError:
    print("WARNING: `practical_python` package not installed. Will try to fix by modifying PATH...")
    _project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    sys.path.insert(0, _project_root)
    print(_project_root)
    from practical_python.utils.geo_utils import haversine as gps_dist

# The M2 LMA bus stop is at GPS coordinate (42.3378699, -71.1024789) - found e.g. using Google Maps.
lma_pos = (42.3378699, -71.1024789)  # lat, lon
# The corner of Luis Pasteur and Fenway is at (42.3389477, -71.1018647)

# Output options:
bus_header = "Route, Bus ID \t   Position    \tHeading\tSpeed\tStop\tSegment"
bus_linefmt = ("{route_id}, {call_name}\t{position[0]:0.03f}, {position[1]:0.03f}\t{heading:>7}\t{speed:>4.01f}"
               "\t{current_stop_id}\t{segment_id}")


def get_masco_id():
    # Get Transloc agencies:
    agencies_res = requests.get("https://feeds.transloc.com/3/agencies")

    # Parse json-formatted response:
    agencies_data = agencies_res.json()

    # The response data contains two entries, 'success' and 'agencies'. Get the 'agencies' entry:
    agencies = agencies_data['agencies']

    # `agencies` is a list of dicts, each dict detailing a given agency.
    # For fun, lets see all agencies in Massachusetts:
    agencies_in_ma = [agency for agency in agencies if agency['location'].endswith(", MA")]
    print("Number of agencies in MA:", len(agencies_in_ma))
    for agency in agencies_in_ma:
        print(" - %s, %s, %s" % (agency['long_name'], agency['short_name'], agency['name']))

    # Lets get the "MASCO" agency:
    masco = next(agency for agency in agencies if agency['short_name'] == "MASCO")
    pprint(masco)

    # The only important info we need is the "id":
    masco_id = masco['id']
    print("MASCO agency id:", masco_id)  # 64
    return masco_id


def get_m2_shuttle_id(masco_id):
    # Get all routes for the given agency (i.e. MASCO):
    routes_res = requests.get("https://feeds.transloc.com/3/routes", params=dict(agencies=masco_id))

    # Parse the json-formatted data:
    routes_data = routes_res.json()

    # Again, the response data has two entries, 'success' and 'routes'. Get the 'routes' entry:
    routes = routes_data['routes']

    # Print all MASCO routes:
    for route in routes:
        print(route['long_name'])

    # Get the M2 shuttle route:
    m2_shuttle = next(route for route in routes if route['long_name'] == "M2")
    pprint(m2_shuttle)

    # Again, we just need the 'id' for the M2 shuttle:
    m2_id = m2_shuttle['id']
    print("M2 shuttle route id:", m2_id)  # 4008182
    return m2_id


def get_m2_buses(masco_id, m2_id):
    # Lets get the real time data:
    # We retrieve data on a per-agency basis:
    vehicles_res = requests.get("https://feeds.transloc.com/3/vehicle_statuses", params=dict(agencies=masco_id))

    # Parse the json-formatted data:
    vehicles_data = vehicles_res.json()

    # Again, the response data has two entries, 'success' and 'routes'. Get the 'routes' entry:
    vehicles = vehicles_data['vehicles']

    # Note: heading vs course vs bearing:
    # * heading: direction you are facing/heading, in degrees clockwise from grid north. heading 45 = North East.
    # * course:  direction of travel, relative to true/grid north.
    # * bearing: direction to target, often relative to magnetic north (although grid north is technically correct).

    # Print all M2 buses:
    m2_buses = [bus for bus in vehicles if bus['route_id'] == m2_id]

    print("\n\nM2 buses: %s\n" % len(m2_buses))
    print(bus_header)
    for bus in m2_buses:
        print(bus_linefmt.format(**bus))
    return m2_buses


def bus_near_location(m2_buses, near_pos=lma_pos, radius=1.0):
    # There are three ways to determine the position of a Transloc vehicle: gps position, current stop, and segment.
    # * GPS position is the most precise and intuitive.
    # * current stop and segment are convenient, if you know the IDs of these.

    # Find buses within 1 km of the LMA bus stop:
    m2_at_lma = [bus for bus in m2_buses if gps_dist(bus['position'], near_pos) < radius]

    print("\n\nM2 buses at LMA: %s\n" % len(m2_at_lma))
    print(bus_header)
    for bus in m2_at_lma:
        print(bus_linefmt.format(**bus))

    # Note: We could also have used e.g. a square [(xmin, xmax), (ymin, ymax)] to evaluate the location of the bus.
    return m2_at_lma


def main():
    # OBS: We generally wouldn't expect the ID values of the MASCO agency and the M2 route to change.
    # Thus, we should save (cache) these so we can re-use them again next time we need them.
    # We can either save all the data we have requested, or just the specific MASCO/M2 IDs. We do the latter:
    try:
        configfn = "config.yaml"
        config = yaml.load(open(configfn))
        print("config loaded from file:", configfn)
        masco_id = config['agency']
        m2_id = config['route']
    except OSError:
        print("\nObtaining MASCO agency id...")
        masco_id = get_masco_id()
        print("\nObtaining M2 shuttle route id...")
        m2_id = get_m2_shuttle_id(masco_id)
        config = dict(agency=masco_id, route=m2_id)
        yaml.dump(config, stream=open("config.yaml", 'w'))

    buses = get_m2_buses(masco_id=masco_id, m2_id=m2_id)
    m2_at_lma = bus_near_location(buses)
    return len(m2_at_lma)


if __name__ == '__main__':
    main()
