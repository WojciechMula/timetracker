#!/usr/bin/env python3

import time
import os

from command_line import CommandLine
from backend import Backend, NoActiveTask, TaskAlreadyActive
from history import History
from report import Report
from utils import StatusDecorator, format_seconds

class Filter:
    def __init__(self):
        self.category = None
        self.name     = None
        self.min_date = None
        self.max_date = None

    def match(self, item):
        if self.category is not None and item.category != self.category:
            return False

        if self.name is not None and item.name != self.name:
            return False

        if self.min_date is not None and item.name < self.min_date:
            return False

        if self.max_date is not None and item.name < self.max_date:
            return False

        return True       


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
            self.handle_history()

        elif cmd == "report":
            self.handle_report()

        elif cmd == "config":
            self.handle_config()

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
            print("Task %s is running for %s (started at %s)" % param)
        else:
            print("No active task")


    def handle_start(self):
        cmd = self.cmdline
        try:
            previous, status = self.backend.start(cmd.get_category(), cmd.get_name())

            if previous:
                previous = StatusDecorator(previous)
                print("Stopped task %s after %s" % (previous, previous.get_timespan()))

            status = StatusDecorator(status)
            print("Task %s has started at %s" % (status, status.get_start_time()))

        except TaskAlreadyActive:
            print("Task %s is already running" % StatusDecorator(self.backend.get_status()))


    def handle_stop(self):
        try:
            status = StatusDecorator(self.backend.stop())

            print("Task %s was stopped. It lasted for %s since %s" % (
                status,
                status.get_timespan(),
                status.get_start_time()
            ))
        except NoActiveTask:
            print("No active task")


    def handle_continue(self):
        try:
            status = StatusDecorator(self.backend.continue_last())

            print("Continuing task %s" % status)
        except TaskAlreadyActive:
            print("Task %s is already running" % StatusDecorator(self.backend.get_status()))


    def handle_history(self):
        filter  = Filter()
        maxdays = 5
        history = History(self.backend, filter, maxdays)
        history.run()


    def handle_report(self):
        filter = Filter()
        report = Report(self.backend, filter)
        report.run()


    def handle_config(self):
        print("database location is %s" % self.backend.dir)
        

if __name__ == '__main__':

    from sys import argv

    cmd = CommandLine(argv[1:])
    bkn = Backend(os.path.expanduser('~/.local/tracker'))

    app = Application(cmd, bkn)
    app.run()
      
