from utils import StatusDecorator, format_seconds
import time

class Record:
    def __init__(self, category, name):
        self.category = category
        self.name = name
        self.time = 0
        self.running = False

class Report:
    def __init__(self, backend, filter):
        self.backend  = backend
        self.filter   = filter

    def run(self):

        def get_key(item):
            return item.get_category() + ":" + item.get_name()

        max_category, max_name, items = self.backend.history()
        items = [item for item in items if self.filter.match(item)]
        data = {}
        for item in items:
            key = get_key(item)

            if key not in data:
                record = Record(item.get_category(), item.get_name())
                data[key] = record
            else:
                record = data[key]

            record.time += item.get_timespan()
            record.running = record.running or item.is_running()

        records = list(data.values())
        records.sort(key=lambda rec: rec.time, reverse=True)

        for record in records:
            desc = "%*s:%*s - %12s" % (max_category, record.category, max_name, record.name, format_seconds(record.time))
            
            if record.running:
                print(desc, "(running)")
            else:
                print(desc)
