class Event:
    def __init__(self, name, date, start_time, end_time, location):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def to_dict(self):
        return {
            'name': self.name,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location
        }

    def __str__(self):
        return f'{self.name}, {self.date}, {self.start_time} - {self.end_time}, {self.location}'
