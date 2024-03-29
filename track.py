#!/usr/bin/env python3

import time
import os

from command_line import CommandLine
from backend import Backend, NoActiveTask, TaskAlreadyActive
from history import History
from report import Report
from utils import StatusDecorator, format_seconds


class Filter:
    def __init__(self, category, name, year, month):
        self.category = category
        self.name     = name
        self.year     = year
        self.month    = month

    def match(self, item):
        if self.category is not None:
            if item.category != self.category:
                return False

        if self.name is not None:
            if item.name != self.name:
                return False

        if self.year is not None:
            if item.start.tm_year != self.year:
                return False

        if self.month is not None:
            if item.start.tm_mon != self.month:
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

        elif cmd == "last":
            self.handle_last()

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
        args = cmd.arguments
        filter  = Filter(args.category, args.name, args.year, args.month)
        maxdays = 365*10
        history = History(self.backend, filter, maxdays)
        history.run()


    def handle_report(self):
        args = cmd.arguments
        filter  = Filter(args.category, args.name, args.year, args.month)
        report = Report(self.backend, filter)
        report.run()


    def handle_config(self):
        print("database location is %s" % self.backend.dir)


    def handle_last(self):
        try:
            last = self.backend.last()
        except ValueError:
            print("No previous task")
        else:
            if last.category:
                name = f'{last.category}:{last.name}'
            else:
                name = last.name
        
            if last.is_running():
                print(f"Current task '{name}'")
            else:
                print(f"Last task '{name}'")

if __name__ == '__main__':

    from sys import argv

    cmd = CommandLine(argv[1:])
    bkn = Backend(os.path.expanduser('~/.local/tracker'))

    app = Application(cmd, bkn)
    app.run()
