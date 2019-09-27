class Departure:
    def __init__(self, bus_info):
        self.bus_info = bus_info
        self.date = bus_info["date"]
        self.number = bus_info["line"]
        self.final_destination = bus_info["direction"]
        self.departure_time_aimed = bus_info["aimed_departure_time"]
        self.departure_time_expected = bus_info["expected_departure_time"]
        self.departure_time_best_estimate = bus_info["best_departure_estimate"]
        self.operator = bus_info["operator_name"]
        self.operator_code = bus_info["operator"]
        self.direction = bus_info["dir"]
        self.bus_id = f"{self.departure_time_aimed}_{self.departure_time_expected}_{self.number}"

    def __repr__(self):
        return ""

    def get_time(self):
        time = self.departure_time_expected
        if not time:
            time = self.departure_time_best_estimate
            if not time:
                time = self.departure_time_aimed

        self.expected_hours = int(time.split(":")[0])
        self.expected_minutes = int(time.split(":")[1])
        return time

    def get_info(self):
        time = self.get_time()
        return [time, self.number, self.final_destination, self.operator, self.expected_hours, self.expected_minutes, self.bus_id]
