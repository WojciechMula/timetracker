import time

from command_line import CommandLine
from backend import Backend, NoActiveTask, TaskAlreadyActive

TIME_FORMAT = '%H:%M:%S (%Y-%m-%d)'

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

        n = self.status.get_timespan()

        s = n % 60
        m = n / 60

        if m < 60:
            return '%d:%02d' % (m, s)
        else:
            h = m / 60
            m = m % 60
            return '%d:%02d:%02d' % (h, m, s)


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


if __name__ == '__main__':

    from sys import argv

    cmd = CommandLine(argv[1:])
    bkn = Backend()

    bkn.init()

    app = Application(cmd, bkn)
    app.run()
