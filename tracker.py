import time

from command_line import CommandLine
from backend import Backend, NoActiveTask, TaskAlreadyActive

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


class Application:

    def __init__(self, cmdline, backend):
        self.cmdline = cmdline
        self.backend = backend

    def run(self):

        cmd = self.cmdline.get_command()

        if cmd == "status":
            self.handle_status()

        elif cmd == "start":
            self.handle_start()

        elif cmd == "stop":
            self.handle_stop()

        elif cmd == "continue":
            self.handle_continue()

        elif cmd == "history":

            if self.cmdline.get_name() == "group":
                self.handle_report()
            else:
                self.handle_history()

        else:
            raise ValueError("Unhandled command %s" % cmd)


    def handle_status(self):
        status = self.backend.get_status()
        if status and status.is_running():
            status = StatusDecorator(self.backend.get_status())
            param = (
                status,
                status.get_timespan(),
                status.get_start_time()
            )
            print "Task %s is running for %s (started at %s)" % param
        else:
            print "No task active"


    def handle_start(self):
        cmd = self.cmdline
        try:
            previous, status = self.backend.start(cmd.get_category(), cmd.get_name())

            if previous:
                previous = StatusDecorator(previous)
                print "Stopped task %s after %s" % (previous, previous.get_timespan())

            status = StatusDecorator(status)
            print "Task %s has started at %s" % (status, status.get_start_time())

        except TaskAlreadyActive:
            print "Task %s is already running" % StatusDecorator(self.backend.get_status())


    def handle_stop(self):
        try:
            status = StatusDecorator(self.backend.stop())

            print "Task %s was stopped. It lasted for %s since %s" % (
                status,
                status.get_timespan(),
                status.get_start_time()
            )
        except NoActiveTask:
            print "No active task"


    def handle_continue(self):
        try:
            status = StatusDecorator(self.backend.continue_last())

            print "Continuing task %s" % status
        except TaskAlreadyActive:
            print "Task %s is already running" % StatusDecorator(self.backend.get_status())


    def handle_history(self):
        
        max_category, max_name, items = self.backend.history()

        for item in items:
            status = StatusDecorator(item)
            
            desc = "%*s:%*s - %8s" % (max_category, status.get_category(), max_name, status.get_name(), status.get_timespan()) 
            
            if status.is_running():
                print desc, "(running)"
            else:
                print desc


    def handle_report(self):
        
        max_category, max_name, items = self.backend.history()
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
                print desc, "(running)"
            else:
                print desc

if __name__ == '__main__':

    from sys import argv

    cmd = CommandLine(argv[1:])
    bkn = Backend()

    bkn.init()

    app = Application(cmd, bkn)
    app.run()
