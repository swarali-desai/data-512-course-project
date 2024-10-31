from pyproj import Transformer, Geod

#    Transform feature geometry data
#
#    The function takes one parameter, a list of ESRI:102008 coordinates that will be transformed to EPSG:4326
#    The function returns a list of coordinates in EPSG:4326
def convert_ring_to_epsg4326(ring_data=None):
    converted_ring = list()
    #
    # We use a pyproj transformer that converts from ESRI:102008 to EPSG:4326 to transform the list of coordinates
    to_epsg4326 = Transformer.from_crs("ESRI:102008","EPSG:4326")
    # We'll run through the list transforming each ESRI:102008 x,y coordinate into a decimal degree lat,lon
    for coord in ring_data:
        lat,lon = to_epsg4326.transform(coord[0],coord[1])
        new_coord = lat,lon
        converted_ring.append(new_coord)
    return converted_ring

#    The function takes two parameters
#        A place - which is coordinate point (list or tuple with two items, (lat,lon) in decimal degrees EPSG:4326
#        Ring_data - a list of decimal degree coordinates for the fire boundary
#
#    The function returns a list containing the shortest distance to the perimeter and the point where that is
#
def shortest_distance_from_place_to_fire_perimeter(place=None,ring_data=None):
    # convert the ring data to the right coordinate system
    ring = convert_ring_to_epsg4326(ring_data)    
    # create a epsg4326 compliant object - which is what the WGS84 ellipsoid is
    geodcalc = Geod(ellps='WGS84')
    closest_point = list()
    # run through each point in the converted ring data
    for point in ring:
        # calculate the distance
        d = geodcalc.inv(place[1],place[0],point[1],point[0])
        # convert the distance to miles
        distance_in_miles = d[2]*0.00062137
        # if it's closer to the city than the point we have, save it
        if not closest_point:
            closest_point.append(distance_in_miles)
            closest_point.append(point)
        elif closest_point and closest_point[0]>distance_in_miles:
            closest_point = list()
            closest_point.append(distance_in_miles)
            closest_point.append(point)
    return closest_point

#    The function takes two parameters
#        A place - which is coordinate point (list or tuple with two items, (lat,lon) in decimal degrees EPSG:4326
#        Ring_data - a list of decimal degree coordinates for the fire boundary
#
#    The function returns the average miles from boundary to the place
#
def average_distance_from_place_to_fire_perimeter(place=None,ring_data=None):
    # convert the ring data to the right coordinate system
    ring = convert_ring_to_epsg4326(ring_data)    
    # create a epsg4326 compliant object - which is what the WGS84 ellipsoid is
    geodcalc = Geod(ellps='WGS84')
    # create a list to store our results
    distances_in_meters = list()
    # run through each point in the converted ring data
    for point in ring:
        # calculate the distance
        d = geodcalc.inv(place[1],place[0],point[1],point[0])
        distances_in_meters.append(d[2])
    #print("Got the following list:",distances_in_meters)
    # convert meters to miles
    distances_in_miles = [meters*0.00062137 for meters in distances_in_meters]
    # the esri polygon shape (the ring) requires that the first and last coordinates be identical to 'close the region
    # we remove one of them so that we don't bias our average by having two of the same point
    distances_in_miles_no_dup = distances_in_miles[1:]
    # now, average miles
    average = sum(distances_in_miles_no_dup)/len(distances_in_miles_no_dup)
    return average

def process_fire_feature(wf_feature, place, unique_id):
    """Processes a single fire feature.

    Args:
        wf_feature: A single feature from the GeoJSON data.
        place: A dictionary containing the place's latitude and longitude.
        unique_id: A unique identifier for the fire.

    Returns:
        A tuple of the key and the processed fire information, or None if an error occurs.
    """

    # Get the relevant metadata for the wildfire
    wf_year = wf_feature['attributes']['Fire_Year']
    wf_name = wf_feature['attributes']['Listed_Fire_Names'].split(',')[0]
    wf_size = wf_feature['attributes']['GIS_Acres']
    wf_type = wf_feature['attributes']['Assigned_Fire_Type']
    wf_circle = wf_feature['attributes']['Circleness_Scale']

    # Creating dictionary with fire information
    fire = {
        'year': wf_year,
        'name': wf_name,
        'size': wf_size,
        'type': wf_type,
        'circleness_scale': wf_circle
    }
    # Create a unique key for each fire information to store it in the fires_info dictionary
    key = f'{wf_year}-{unique_id}-{wf_name}'

    try:
        # Determines whether the fire's geometry is represented by `rings` or `curveRings`. It extracts the relevant ring data.
        if 'rings' in wf_feature['geometry']:
            ring_data = wf_feature['geometry']['rings'][0]
        elif 'curveRings' in wf_feature['geometry']:
            ring_data = wf_feature['geometry']['curveRings'][0]
        else:
            raise Exception("No compatible geometry in this fire data!!!")

        # Compute using the shortest distance to any point on the perimeter
        shortest_distance = shortest_distance_from_place_to_fire_perimeter(place['latlon'], ring_data)
        fire["distance_shortest"] = shortest_distance
        # print(f"The closest distance of fire '{wf_name}' ({wf_size:1.2f} acres) from {wf_year} was {shortest_distance[0]:1.2f} miles to {place['city']}")
        # print(f"\tThe cloest perimiter point lat,lon {shortest_distance[1][0]},{shortest_distance[1][1]}")

        # Compute using the average distance to all points on the perimeter
        avg_distance = average_distance_from_place_to_fire_perimeter(place['latlon'], ring_data)
        fire["avg_distance"] = avg_distance
        # print(f"Fire '{wf_name}' ({wf_size:1.2f} acres) from {wf_year} was an average {avg_distance:1.2f} miles to {place['city']}")

        # Get a location to print thats on the ring (perimeter)
        ring = convert_ring_to_epsg4326(ring_data)
        perimeter_start = ring[0]
        fire["perimeter_start"] = perimeter_start
        # print(f"\tOne perimiter point lat,lon {perimeter_start[0]},{perimeter_start[1]}")
        
        # # Store the information
        # fires_info[key] = fire

        return key, fire
    except Exception as e:
        print(f"Error in processing the wildfire data for {wf_name} from {wf_year}. (Key - {key}")
        print(e)
        return key, e