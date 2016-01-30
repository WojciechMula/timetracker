import time

TIME_FORMAT = '%H:%M:%S (%Y-%m-%d)'

def format_seconds(seconds):

    s = seconds % 60
    m = seconds / 60

    if m < 60:
        return '%d:%02d' % (m, s)
    else:
        h = m / 60
        m = m % 60
        return '%d:%02d:%02d' % (h, m, s)

class StatusDecorator:
    def __init__(self, status):
        self.status = status

    def __str__(self):
        cat  = self.status.get_category()
        name = self.status.get_name()

        if cat:
            return "'%s' (%s)" % (name, cat)
        else:
            return "'%s'" % name


    def get_start_time(self):
        return time.strftime(TIME_FORMAT, self.status.get_start_time())


    def get_timespan(self):
        return format_seconds(self.status.get_timespan())


    def __getattr__(self, attr):
        return getattr(self.status, attr)

