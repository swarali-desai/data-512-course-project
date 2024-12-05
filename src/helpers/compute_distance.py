from pyproj import Transformer, Geod


def convert_ring_to_epsg4326(ring_data=None):
    """
    Convert a list of coordinates from ESRI:102008 projection to EPSG:4326 (WGS84) coordinate system.

    Args:
        ring_data (list): A list of tuples, where each tuple contains x, y coordinates 
            in the ESRI:102008 projection.

    Returns:
        list: A list of tuples, where each tuple contains latitude and longitude 
            in the EPSG:4326 (WGS84) coordinate system.

    Notes:
        - The conversion is performed using a PyProj `Transformer` object.
        - ESRI:102008 is typically used for North America Albers Equal Area projections, 
          and EPSG:4326 represents the WGS84 geographic coordinate system.
        - Each coordinate in `ring_data` is transformed and appended to the output list.

    """
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


def shortest_distance_from_place_to_fire_perimeter(place=None,ring_data=None):
    """
    Calculate the shortest distance (in miles) and the corresponding point on the fire perimeter
    from a given location.

    Args:
        place (tuple): A tuple representing the latitude and longitude of the place 
            in the format (latitude, longitude).
        ring_data (list): A list of coordinate pairs (latitude, longitude) representing 
            the vertices of the fire perimeter polygon.

    Returns:
        list: A list containing two elements:
            - float: The shortest distance from the given location to the fire perimeter, in miles.
            - tuple: The latitude and longitude of the closest point on the fire perimeter.

    Notes:
        - The function converts the ring data to the WGS84 coordinate system using 
          the `convert_ring_to_epsg4326` function.
        - Distance calculations are performed using the geodesic distance on the WGS84 ellipsoid.
        - The fire perimeter is assumed to be a closed polygon, and the calculation 
          considers all points in the perimeter.

    """
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


def average_distance_from_place_to_fire_perimeter(place=None,ring_data=None):
    """
    Calculate the average distance (in miles) from a given location to the perimeter of a fire, represented as a polygon.

    Args:
        place (tuple): A tuple representing the latitude and longitude of the place 
            in the format (latitude, longitude).
        ring_data (list): A list of coordinate pairs (latitude, longitude) representing 
            the vertices of the fire perimeter polygon.

    Returns:
        float: The average distance from the given location to the fire perimeter, in miles.

    Notes:
        - The function converts the ring data to the WGS84 coordinate system using 
          the `convert_ring_to_epsg4326` function.
        - Distance calculations are performed using the geodesic distance on the WGS84 ellipsoid.
        - The fire perimeter is assumed to be a closed polygon, and the duplicate endpoint is 
          excluded from the average distance calculation to avoid bias.

    """
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