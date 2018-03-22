
from math import cos, sqrt, pi, radians, sin, asin
import numpy as np
try:
    # Haversine ("great circle") formula for converting difference in lat/lon coordinates to distance in km:
    from haversine import haversine
    # Methods, in order of precision: Vincenty's > Haversine
    # Note: The differences are insignificant for distances less than 100 km.
    # Packages: geopy, haversine, geographiclib
except ImportError:
    try:
        from geopy.distance import great_circle as haversine
    except ImportError:
        def haversine(pos1, pos2):
            """From https://stackoverflow.com/a/4913653/3241277"""
            (lon1, lat1), (lon2, lat2) = pos1, pos2
            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula:
            dlon, dlat = lon2 - lon1, lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers. Use 3956 for miles
            return c * r


def equirectangular_dist(pos1, pos2):
    """Equirectangular approximation formula.
    Faster than haversine, but less accurate.
    Should be almost OK for small distances, almost as good as haversine.

    Refs:
    * http://www.movable-type.co.uk/scripts/latlong.html
    * https://stackoverflow.com/a/1253545/3241277
    https://gis.stackexchange.com/q/58653 and https://stackoverflow.com/a/23755388/3241277
    """
    # One degree of latitude is about 110 km (approximately, since the earth is not a sphere)
    # One degree of longitude is about 111 km * cos(latitude)  # Make sure cos(latitude) are in compatible units
    y = (pos1[0] - pos2[0]) * 110.574  # lat
    x = (pos1[1] - pos2[1]) * 111.320 * cos((pos1[0]+pos2[0]) * pi/360)  # OK for small distances
    return sqrt(x**2 + y**2)

gps_dist = haversine


def get_heading_str(heading, resolution=2, long_form=False, sep="-"):
    """

    Args:
        heading:
        resolution:
        long_form: Use the long form "North-North-East" rather than "NNE".

    Returns:

    Examples:
        North: 0, East: 90
        North-East: 45
        North-North-East: 22.5
        >>> get_heading_str(40, resolution=1)  # Use one word to describe heading
        "North"
        >>> get_heading_str(40, resolution=2)  # Use two words to describe heading
        "North-East"
        >>> get_heading_str(40, resolution=3)  # Use three words to describe heading
        "North-East"
    """
    if not 0 < resolution < 4:
        raise ValueError("`resolution` must be 1, 2, or 3.")
    if heading < -360:
        raise ValueError("`heading` is %s, but must be above -360 degrees, preferably between 0 and 360." % heading)
    arc = 90 / 2**(resolution-1)  # 90 for resolution of 1, 45 for resolution of 2, etc.
    # print("resolution, arc =", resolution, arc, end=": ")
    # print("heading = %0.02f" % heading, end=" ")
    heading = (heading + 360) % 360  # Ensure heading in range 0..360
    # print("=> %0.02f" % heading, end=" ")
    index = int(((heading + arc/2) % 360) // arc)
    # print(", index =", index, end=" ", flush=True)
    # heading_strs[resolution][index]
    heading_strs = [
        [],  # resolution=0
        ["N", "E", "S", "W"],
        ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ]
    # Alternative approach: Use cos/sin to determine how close to North/South (sin) and East/West (cos) we are.
    assert [len(arr) for arr in heading_strs] == [0, 4, 8, 16]
    corners = {
        "N": "North",
        "E": "East",
        "S": "South",
        "W": "West"
    }
    res = heading_strs[resolution][index]
    if long_form:
        res = sep.join(corners[char] for char in res)
    # print(", res =", res)
    # print(heading_old, heading, index, res)
    return res


def test_get_heading_str():
    assert get_heading_str(22, resolution=1) == "N"
    assert get_heading_str(22, resolution=2) == "N"
    assert get_heading_str(22, resolution=3) == "NNE"
    assert get_heading_str(22, resolution=3, long_form=True, sep="-") == "North-North-East"

    assert get_heading_str(44, resolution=1) == "N"
    assert get_heading_str(44, resolution=2) == "NE"
    assert get_heading_str(44, resolution=3) == "NE"
    assert get_heading_str(44, resolution=3, long_form=True, sep="-") == "North-East"

    assert get_heading_str(46, resolution=1) == "E"
    assert get_heading_str(46, resolution=2) == "NE"
    assert get_heading_str(46, resolution=3) == "NE"
    assert get_heading_str(46, resolution=3, long_form=True, sep="-") == "North-East"

    assert get_heading_str(180+22, resolution=1) == "S"
    assert get_heading_str(180+22, resolution=2) == "S"
    assert get_heading_str(180+22, resolution=3) == "SSW"
    assert get_heading_str(180+22, resolution=3, long_form=True, sep="-") == "South-South-West"

    assert get_heading_str(180+44, resolution=1) == "S"
    assert get_heading_str(180+44, resolution=2) == "SW"
    assert get_heading_str(180+44, resolution=3) == "SW"
    assert get_heading_str(180+44, resolution=3, long_form=True, sep="-") == "South-West"

    assert get_heading_str(180+46, resolution=1) == "W"
    assert get_heading_str(180+46, resolution=2) == "SW"
    assert get_heading_str(180+46, resolution=3) == "SW"
    assert get_heading_str(180+46, resolution=3, long_form=True, sep="-") == "South-West"

    for resolution in range(1, 4):
        assert get_heading_str(0, resolution=resolution) == "N"
        assert get_heading_str(90, resolution=resolution) == "E"
        assert get_heading_str(180, resolution=resolution) == "S"
        assert get_heading_str(270, resolution=resolution) == "W"

        assert get_heading_str(0,   resolution=resolution, long_form=True) == "North"
        assert get_heading_str(90,  resolution=resolution, long_form=True) == "East"
        assert get_heading_str(180, resolution=resolution, long_form=True) == "South"
        assert get_heading_str(270, resolution=resolution, long_form=True) == "West"

    for origin, bearing in (0, "North"), (90, "East"), (180, "South"), (270, "West"):
        for heading in range(origin-45, origin+45):
            assert get_heading_str(heading, resolution=1) == bearing[0]
        for heading in np.linspace(origin-45/2, origin+45/2-0.1, 20):
            assert get_heading_str(heading, resolution=2) == bearing[0]
        for heading in np.linspace(origin-45/4, origin+45/4-0.1, 20):
            assert get_heading_str(heading, resolution=3) == bearing[0]

    for i in range(-60, 390):
        print("Heading %3s => %3s (%s) or %03s (%s)" % (
            i, get_heading_str(i), get_heading_str(i, long_form=True),
            get_heading_str(i, resolution=3), get_heading_str(i, long_form=True, resolution=3),
        ))

if __name__ == '__main__':
    test_get_heading_str()
