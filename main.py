from Request import *


def main(postcode):
    with open('secrets.txt') as file:
        api_code = file.readline().split("=")[1].strip()
        api_key = file.readline().split("=")[1].strip()

    new_request = Request(api_code, api_key)
    postcode_response = new_request.set_postcode(postcode)

    if postcode_response == 200:
        new_request.set_limit(2)
        stops = new_request.get_nearby_stops()

        data = {}

        for stop in stops:
            print(stop)
            atcocode = stop.get_atcocode()
            new_request = Request(api_code, api_key)
            new_request.set_atcocode(atcocode)
            new_request.set_limit(5)
            departures = new_request.get_departures()

            stop_departures = []

            for departure in departures:
                stop_departures.append(departure.get_info())

            data[stop] = stop_departures

        return data
    return 404

if __name__ == "__main__": main()
