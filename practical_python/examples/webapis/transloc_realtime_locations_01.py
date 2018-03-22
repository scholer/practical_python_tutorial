

import requests
from pprint import pprint
import yaml


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


# Next, lets see all the MASCO routes:
routes_res = requests.get("https://feeds.transloc.com/3/routes", params=dict(agencies=masco_id))

# Parse the json-formatted data:
routes_data = routes_res.json()

# Again, the response data has two entries, 'success' and 'routes'. Get the 'routes' entry:
routes = routes_data['routes']

# Print all MASCO routes:
for route in routes:
    print(route['long_name'])
    # print(" - %s, %s, %s" % (route['long_name'], route['short_name'], route['name']))

# Get the M2 shuttle route:
m2_shuttle = next(route for route in routes if route['long_name'] == "M2")
pprint(m2_shuttle)

# Again, we just need the 'id' for the shuttle:
m2_id = m2_shuttle['id']
print("M2 shuttle route id:", m2_id)

# OBS: We generally wouldn't expect the ID values of the MASCO agency and the M2 route to change.
# Thus, we should save (cache) these so we can re-use them again next time we need them.
# We can either save all the data we have requested, or just the specific MASCO/M2 IDs. We do the latter:
yaml.dump(dict(agency=masco_id, route=m2_id), stream=open("config.yaml", 'w'))

# Lets get the real time data:
# We retrieve data on a per-agency basis:

vehicles_res = requests.get("https://feeds.transloc.com/3/vehicle_statuses", params=dict(agencies=masco_id))

# Parse the json-formatted data:
vehicles_data = vehicles_res.json()

# Again, the response data has two entries, 'success' and 'routes'. Get the 'routes' entry:
vehicles = vehicles_data['vehicles']

# Print all MASCO vehicles:
print("\n\nMASCO vehicles: %s\n" % len(vehicles))
print("Route, Bus id \t   Position      \tHeading\tSpeed")
linefmt = "{route_id}, {call_name} \t {position[0]:0.03f}, {position[1]:0.03f} \t{heading:8}\t{speed:>5.01f}"
for bus in vehicles:
    print(linefmt.format(**bus))

# Print all M2 buses:
m2_buses = [bus for bus in vehicles if bus['route_id'] == m2_id]

print("\n\nM2 buses: %s\n" % len(m2_buses))
print("Route, Bus ID \t   Position    \tHeading\tSpeed\tStop\tSegment")
linefmt = ("{route_id}, {call_name}\t{position[0]:0.03f}, {position[1]:0.03f}\t{heading:>7}\t{speed:>4.01f}"
           "\t{current_stop_id}\t{segment_id}")
for bus in m2_buses:
    print(linefmt.format(**bus))

# There are three ways to determine the position of a Transloc vehicle: gps position, current stop, and segment.
# * GPS position is the most precise and intuitive.
# * current stop and segment are convenient, if you know the IDs of these.

# The M2 LMA bus stop is at GPS coordinate (42.3378699, -71.1024789) - found e.g. using Google Maps.
lma_pos = (42.3378699, -71.1024789)
# The corner of Luis Pasteur and Fenway is at (42.3389477, -71.1018647)
# One degree of lat/lon is about 110 km (approximately, since the earth is not a sphere)
# A 500 m radius corresponds to 0.5 km / (110 km / degree) = 0.0045... degree
# 0.01 lat/lon degree is approx. 1 km:
radius = 0.01


def is_near_lma(bus):
    """Returns True if bus is within `radius` of `lma_pos`."""
    return (bus['position'][0] - lma_pos[0])**2 + (bus['position'][1] - lma_pos[1])**2 < radius**2

# Find buses within 1 km of the LMA bus stop:
m2_at_lma = [
    bus for bus in m2_buses
    if (bus['position'][0] - lma_pos[0])**2 + (bus['position'][1] - lma_pos[1])**2 < radius**2
]

print("\n\nM2 buses at LMA: %s\n" % len(m2_at_lma))
print("Route, Bus ID \t   Position    \tHeading\tSpeed\tStop\tSegment")
for bus in m2_at_lma:
    print(linefmt.format(**bus))

# Note: We could also have used e.g. a square [(xmin, xmax), (ymin, ymax)] to evaluate the location of the bus.




