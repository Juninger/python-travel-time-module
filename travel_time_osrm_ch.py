"""
__authors__: Marcus Juninger & Nicholas Narvell
__date of creation__: 2023-04-04
__last modified__: 2023-05-26
"""

import sys
import json
from collections import deque
import requests as httpclient


class TravelTimeOSRMCH:
    '''
    Class used to query OpenSourceRoutingMachine Docker Container (server) for travel time calculations.
    Provides three methods depending on use case:

    * MANY-TO-ONE
    * ONE-TO-MANY
    * ONE-TO-ONE

    :var (str) ip_address: Input ip address of OSRM server (e.g. 127.0.0.1 if it is running on the same computer)
    :var (str) port: Input port of OSRM server (e.g. 5001, same port as your instance of OSRM server)
    '''

    ip_address = "127.0.0.1"
    port = "5001"

    # String that combines ip address and port to form correct url to call OSRM server
    url = "http://" + ip_address + ":" + port + "/table/v1/driving/"
    # Required header to make call to OSRM server
    headers = {'Content-Type': 'application/json'}

    def get_travel_time_many_to_one(self, sources_longlats, destination_longlat):
        """
        Used for MANY-TO-ONE scenarios such as: "ambulances to patient"
        :param sources_longlats: Array of (MANY) longitude + latitude combinations. Represents starting
            locations (e.g. ambulance garages) in format --> [[longitude, latitude], [longitude, latitude], ...]
        :param destination_longlat: Array of (ONE) longitude + latitude combination. Represents
            destination (e.g. a patient) in format --> [longitude, latitude]
        :return:
            1. travel_time: Travel time in HOURS
            2. source: Array object with longitude + latitude of source that has the shortest travel time to the destination
                in format --> [longitude, latitude]
            3. destination_longlat: Array object with longitude + latitude of destination
                in format --> [longitude, latitude]
        """

        # List of all locations (source + destinations), uses deque to be able to use appendleft-method
        locations = deque(sources_longlats)
        locations.appendleft(destination_longlat)

        # Prepares string for request with matrix coordinates
        data = ""
        for obj in locations:
            long_lat = str(obj[0]) + "," + str(obj[1]) + ";"
            data += long_lat

        # Removes trailing semicolon
        data_obj = data.rstrip(';')

        # Builds final string for GET request
        ending_url = "?destinations=0&skip_waypoints=true"
        request = self.url + data_obj + ending_url

        # Sends request to server
        response = httpclient.get(request)

        """
        Only used for debugging HTTP request errors
        """
        # print(response.text)
        # print(response.status_code, response.reason)

        # Converts response from json to object-structure
        response_json = json.loads(response.text)

        travel_time = sys.maxsize
        saved_idx = -1

        # Finds the shortest travel time and saves index of source
        for idx, obj in enumerate(response_json['durations']):
            duration = obj[0]
            if 0 < duration < travel_time:
                travel_time = duration
                saved_idx = idx - 1

        # Converts travel time to HOURS (to fit simulation framework standards)
        travel_time = travel_time / 3600

        # Fetches coordinate pair from source that has the shortest travel time to the destination
        source = sources_longlats[saved_idx]

        """
        Only used for debugging return values
        """
        # print("travel_time: ", travel_time)
        # print("source: ", source)
        # print("destination_longlat: ", destination_longlat)

        return travel_time, source, destination_longlat

    def get_travel_time_one_to_many(self, source_longlat, destinations_longlats):
        """
        Used for ONE-TO-MANY scenarios such as: "patient to hospital"
        :param source_longlat: Array of (ONE) longitude + latitude combination. Represents starting
            location (e.g. patient) in format --> [longitude, latitude]
        :param destinations_longlats: Array of (MANY) longitude + latitude combinations. Represents
            destinations (e.g. hospitals) in format --> [[longitude, latitude], [longitude, latitude], ...]
        :return:
            1. travel_time: Travel time in HOURS
            2. destination: Array object with longitude + latitude of destination that has the shortest travel time from the source
                in format --> [longitude, latitude]
            3. source_longlat: Array object with longitude + latitude of source
                in format --> [longitude, latitude]
        """

        # List of all locations (source + destinations), uses deque to be able to use appendleft-method
        locations = deque(destinations_longlats)
        locations.appendleft(source_longlat)

        # Prepares string for request with matrix coordinates
        data = ""
        for obj in locations:
            long_lat = str(obj[0]) + "," + str(obj[1]) + ";"
            data += long_lat

        # Removes trailing semicolon
        data_obj = data.rstrip(';')

        # Builds final string for GET request
        ending_url = "?sources=0&skip_waypoints=true"
        request = self.url + data_obj + ending_url

        # Sends request to server
        response = httpclient.get(request)

        """
        Only used for debugging HTTP request errors
        """
        # print(response.text)
        # print(response.status_code, response.reason)

        # Converts response from json to object-structure
        response_json = json.loads(response.text)

        travel_time = sys.maxsize
        saved_idx = -1

        # Finds the shortest travel time and saves index of destination
        for idx, obj in enumerate(response_json['durations'][0]):
            duration = obj
            if 0 < duration < travel_time:
                travel_time = duration
                saved_idx = idx - 1

        # Converts travel time to HOURS (to fit simulation framework standards)
        travel_time = travel_time / 3600

        # Fetches coordinate pair from destination that has the shortest travel time from the source
        destination = destinations_longlats[saved_idx]

        """
        Only used for debugging return values
        """
        # print("travel_time: ", travel_time)
        # print("source: ", source)
        # print("destination_longlat: ", destination_longlat)

        return travel_time, destination, source_longlat

    def get_travel_time_one_to_one(self, source_longlat, destination_longlat):
        """
        Used for ONE-TO-ONE scenarios such as: "hospital to ambulance garage"
        :param source_longlat: Array of (ONE) longitude + latitude combination. Represents starting
            location (e.g. hospital) in format --> [longitude, latitude]
        :param destination_longlat: Array of (ONE) longitude + latitude combination. Represents
            destination (e.g. ambulance garage) in format --> [longitude, latitude]
        :return:
            1. travel_time: Travel time in HOURS
            2. source_longlat: rray object with longitude + latitude of source
                in format --> [longitude, latitude]
            3. destination_longlat: Array object with longitude + latitude of destination
                in format --> [longitude, latitude]
        """

        # Object with source + destination
        locations = [source_longlat] + [destination_longlat]

        # Prepares string for request
        data = ""
        for obj in locations:
            long_lat = str(obj[0]) + "," + str(obj[1]) + ";"
            data += long_lat

        # Removes trailing semicolon
        data_obj = data.rstrip(';')

        # Builds final string for GET request
        ending_url = "?sources=0&destinations=1&skip_waypoints=true"
        request = self.url + data_obj + ending_url

        # Sends request to server
        response = httpclient.get(request)

        """
        Only used for debugging HTTP request errors
        """
        # print(response.text)
        # print(response.status_code, response.reason)

        # Converts response from json to object-structure
        response_json = json.loads(response.text)

        # Converts travel time to HOURS (to fit simulation framework standards)
        travel_time = response_json['durations'][0][0] / 3600

        """
        Only used for debugging return values
        """
        # print("travel_time: ", travel_time)
        # print("source: ", source_longlat)
        # print("destination_longlat: ", destination_longlat)

        return travel_time, source_longlat, destination_longlat
