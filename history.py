from utils import StatusDecorator, format_seconds
import time

class History:
    def __init__(self, backend, filter, days):
        self.backend  = backend
        self.max_days = days
        self.filter   = filter

    def run(self):

        max_category, max_name, items = self.backend.history()

        prev_date = None
        days = -1
        for item in (item for item in items if self.filter.match(item)):

            status = StatusDecorator(item)
            date = time.strftime('%Y-%m-%d', item.get_start_time())
            
            if prev_date != date:
                days += 1
                if self.max_days is not None and days == self.max_days:
                    break

                print date
                prev_date = date

            desc = "  %*s:%*s - %8s" % (max_category, status.get_category(), max_name, status.get_name(), status.get_timespan()) 
            
            if status.is_running():
                print desc, "(running)"
            else:
                print desc

