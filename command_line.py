import argparse

class CommandLine:
    def __init__(self, arguments):
        if not arguments:
            self.command = 'status'
            return

        valid_choices = ("start", "stop", "status", "continue", "history", "report", "config", "last")
        ap = argparse.ArgumentParser(description="Track you activity")
        sp = ap.add_subparsers(dest='command')

        parser_start = sp.add_parser('start', help="start activity")
        parser_start.add_argument("name",
                                  metavar="NAME",
                                  nargs='+',
                                  help="name of task")
        sp.add_parser('stop', help="stop the current activity")
        sp.add_parser('status', help="show current status")
        sp.add_parser('last', help="show last activity")
        sp.add_parser('continue', help="continue last activity")
        parser_history = sp.add_parser('history', help="show history")
        parser_report = sp.add_parser('report', help="show reports")
        sp.add_parser('config', help="show the current configuration")

        for p in [parser_history, parser_report]:
            p.add_argument("--category",
                           help="activity category")
            p.add_argument("--name",
                           help="activity name")
            p.add_argument("--year",
                           type=int,
                           help="year of an event")
            p.add_argument("--month",
                           type=int,
                           help="month of an event")

        args = ap.parse_args(arguments)
        if args.command == 'start':
            tmp = ' '.join(args.name)
            try:
                self.category, self.name = tmp.split(':', 1)
            except ValueError:
                self.category = ""
                self.name     = tmp


        self.command   = args.command
        self.arguments = args


    def get_command(self):
        return self.command

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name
