
class Stop:
    def __init__(self, stop_info):
        self.name = stop_info["name"]
        #self.location = stop_info["description"]
        self.latitude = stop_info["latitude"]
        self.longitude = stop_info["longitude"]
        self.atcocode = stop_info["atcocode"]

    def __repr__(self):
        return f"Stop: {self.name}"

    def get_atcocode(self):
        return self.atcocode

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude
