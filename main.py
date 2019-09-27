from Request import *

def main(postcode):
    with open('secrets.txt') as file:
        api_code = file.readline().split("=")[1].strip()
        api_key = file.readline().split("=")[1].strip()
        gmaps_api = file.readline().split("=")[1].strip()

    new_request = Request(api_code, api_key)
    postcode_response = new_request.set_postcode(postcode)

    if postcode_response == 200:
        new_request.set_limit(2)
        stops = new_request.get_nearby_stops()

        data = {}
        routes = []

        for stop in stops:
            #print(stop)
            atcocode = stop.get_atcocode()
            new_request = Request(api_code, api_key)
            new_request.set_atcocode(atcocode)
            new_request.set_limit(5)
            departures = new_request.get_departures()

            stop_departures = []

            for departure in departures[:1]:
                stop_departures.append(departure.get_info())
                new_request = Request(api_code, api_key)
                upcoming_stops = new_request.get_route(departure, atcocode)

                lat_long = []
                for upcoming_stop in upcoming_stops:
                    lat_long.append([upcoming_stop.get_latitude(), upcoming_stop.get_longitude()])

                route = [departure.bus_id, lat_long]
                routes.append(route)

            data[stop] = stop_departures
            print(routes)
        return [data, routes, gmaps_api]

    return 404

if __name__ == "__main__": main()
