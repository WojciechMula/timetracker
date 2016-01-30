from utils import StatusDecorator, format_seconds
import time

class History:
    def __init__(self, backend, filter, days):
        self.backend  = backend
        self.max_days = days
        self.filter   = filter

        self.total_time  = 0.0
        self.total_count = 0

    def run(self):

        self.max_category, self.max_name, items = self.backend.history()

        prev_date = None
        days = -1


        for item in (item for item in items if self.filter.match(item)):

            status = StatusDecorator(item)
            date = time.strftime('%Y-%m-%d', item.get_start_time())
            
            if prev_date != date:

                self.print_total()

                days += 1
                if self.max_days is not None and days == self.max_days:
                    break

                print date
                prev_date = date

            
            self.print_item(status)
            self.total_count += 1
            self.total_time  += item.get_timespan()
            

        self.print_total()


    def print_item(self, status):
        desc = "  %*s %*s - %8s" % (
            self.max_category,
            status.get_category(),
            self.max_name,
            status.get_name(),
            status.get_timespan()
        )

        if status.is_running():
            print desc, "(running)"
        else:
            print desc


    def print_total(self):
        if self.total_count > 1:
            indent = self.max_category + self.max_name + 14
            print "%*s total" % (indent, format_seconds(self.total_time))

        self.total_time  = 0.0
        self.total_count = 0
