from utils import StatusDecorator, format_seconds
import time

class Report:
    def __init__(self, backend, filter):
        self.backend  = backend
        self.filter   = filter

    def run(self):

        max_category, max_name, items = self.backend.history()
        items = [item for item in items if self.filter.match(item)]
        sum = {}
        running_key = None
        for item in items:
            key = item.get_category() + ":" + item.get_name()

            sum[key] = sum.get(key, 0) + item.get_timespan()
            if item.is_running():
                assert running_key is None
                running_key = key

        for item in items:
            status = StatusDecorator(item)
            key = item.get_category() + ":" + item.get_name()
            
            try:
                time = sum.pop(key)
            except KeyError:
                continue

            desc = "%*s:%*s - %8s" % (max_category, status.get_category(), max_name, status.get_name(), format_seconds(time))
            
            if key == running_key:
                print(desc, "(running)")
            else:
                print(desc)
