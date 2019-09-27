from Request import *

def main(postcode):
    with open('secrets.txt') as file:
        api_code = file.readline().split("=")[1].strip()
        api_key = file.readline().split("=")[1].strip()
        mapquest_key = file.readline().split("=")[1].strip()

    new_request = Request(api_code, api_key)
    postcode_response = new_request.set_postcode(postcode)

    if postcode_response == 200:
        new_request.set_limit(2)
        stops = new_request.get_nearby_stops()

        data = {}
        routes = {}

        for stop in stops:
            atcocode = stop.get_atcocode()
            lat = stop.get_latitude()
            long = stop.get_longitude()
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

                routes[departure.bus_id] = lat_long

                url = "https://www.mapquestapi.com/staticmap/v5/map?key=" + api_key + "&scale=1&start=" + str(routes[departure.bus_id][0][0]) + ", " + str(routes[departure.bus_id][0][1]) + "&end=" + str(routes[departure.bus_id][-1][0]) + ", " + str(routes[departure.bus_id][-1][0]) + "&locations=" + str(lat) + ", " + str(long) + "&size=800,300"

            data[stop] = stop_departures
        return [data, routes, mapquest_key, lat, long]

    return 404


if __name__ == "__main__": main()
