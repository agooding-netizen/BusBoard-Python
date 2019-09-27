
from urllib.request import urlopen
from Departure import *
from Stop import *
import json

class Request:
    def __init__(self, api_code, api_key, limit=5):
        self.api_code = api_code
        self.api_key = api_key
        self.limit = limit

    def get_nearby_stops(self):
        link = f"http://transportapi.com/v3/uk/places.json?app_id={self.api_code}&app_key={self.api_key}&lat={self.latitude}&lon={self.longitude}&limit={self.limit}&type=bus_stop"
        page = urlopen(link)
        json_data = page.read()
        print("Reading " + link)

        data = json.loads(json_data.decode("utf-8"))

        stop_data = data["member"]
        stops = []

        for stop in stop_data:
            stops.append(Stop(stop))

        return stops

    def set_postcode(self, postcode):
        self.postcode = postcode
        return self.set_coords()

    def set_coords(self):
        link = f"http://api.postcodes.io/postcodes/{self.postcode}"
        status = 200

        try:
            page = urlopen(link)
            json_data = page.read()
            data = json.loads(json_data.decode("utf-8"))
        except:
            status = 404

        if status == 200:
            self.longitude = data['result']['longitude']
            self.latitude = data['result']['latitude']
            return status
        else:
            return status

    def set_atcocode(self, atcocode):
        self.atcocode = atcocode

    def read_atcocode(self):
        self.atcocode = input("Enter an atcocode: ")

    def read_postcode(self):
        self.postcode = input("Enter a postcode: ")
        self.set_coords()

    def set_limit(self, limit):
        self.limit = limit

    def process_response(self, json_data):
        data = json.loads(json_data.decode("utf-8"))

        departures_data = data["departures"]
        departures = []

        for bus_number in departures_data:
            for bus_info in departures_data[bus_number]:
                departures.append(Departure(bus_info))

        return departures

    def get_departures(self):
        link = f"https://transportapi.com/v3/uk/bus/stop/{self.atcocode}/live.json?app_id={self.api_code}&app_key={self.api_key}&group=no&limit={self.limit}&nextbuses=no"
        page = urlopen(link)
        data = page.read()
        print("Reading " + link)

        departures = self.process_response(data)

        if len(departures) > self.limit:
            return departures[:self.limit]

        return departures

    def get_route(self, departure, atcocode):
        link = f"https://transportapi.com/v3//uk/bus/route/{departure.operator_code}/{departure.number}/{departure.direction}/{atcocode}/timetable.json?app_id={self.api_code}&app_key={self.api_key}&stops=all"
        print(link)
        page = urlopen(link)
        data = page.read()

        upcoming_stops = self.process_stops(data)

        return upcoming_stops

    def process_stops(self, json_data):
        data = json.loads(json_data.decode("utf-8"))

        stops_data = data["stops"]
        upcoming_stops = []

        for stop in stops_data:
            upcoming_stops.append(Stop(stop))

        return upcoming_stops
